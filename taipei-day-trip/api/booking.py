#---------------------------讀取模組---------------------------------------------------------------------#
from flask import *
from flask import Blueprint, render_template, abort
from flask import Flask, make_response
from flask import request 
import jwt  #JSON Web Token
from flask_bcrypt import Bcrypt 
from datetime import datetime
from datetime import date
import sys
sys.path.append('../')
from pool import conpool
#---------------------------Blueprint---------------------------------------------------------------------#
booking = Blueprint('booking', __name__, static_folder='static',template_folder='templates',url_prefix='')
#---------------------------Bcrypt---------------------------------------------------------------------#
#預定行程
@booking.route("/api/booking",methods=["GET","POST","DELETE"])
def api_booking():
#建立新的預定行程
    if request.method=="POST": 
            token = request.cookies.get("token")
            if token != None: #有token
                #從前端接收資料
                get_front_jsondata= request.get_json()
                date_object = datetime.strptime(get_front_jsondata["date"], "%Y-%m-%d").date()
                if get_front_jsondata["date"]=="":
                    return jsonify({  #前端資料不完整
                        "error": True,
                        "message": "預定失敗，請確認所有選項都已填入"
                    }), 400
                elif date_object<=date.today():
                    return jsonify({  #使用者輸入過去或當天日期
                        "error": True,
                        "message": "無法預定過去時間或當天行程"
                    }), 400
                else:#有token且前端資料也完整
                    try:
                        #連接資料庫
                        connection = conpool.get_connection()
                        cursor = connection.cursor(dictionary=True,buffered=True)
                        #解TOKEN並記錄使用者編號
                        decoded_jwt = jwt.decode(token, "secret", algorithms=['HS256'])  #解開TOKEN
                        #先看看資料庫有沒有預訂的行程，有的話就先刪掉
                        cursor.execute("SELECT * FROM booking WHERE user_id =%s",(decoded_jwt["id"],))
                        result = cursor.fetchone()
                        if result!=None:
                            cursor.execute("DELETE FROM booking WHERE user_id = %s",(decoded_jwt["id"],))
                            connection.commit() # 確保數據被刪除
                        #將前端資料插入資料庫
                        insert_to_bookingtable = "INSERT INTO booking (user_id, attraction_id, date, time, price)  VALUES (%s, %s,%s, %s, %s)"
                        val_bookingtable = (decoded_jwt["id"], get_front_jsondata["attraction_id"], get_front_jsondata["date"], get_front_jsondata["time"], get_front_jsondata["price"][4:8])
                        cursor.execute(insert_to_bookingtable, val_bookingtable)  
                        connection.commit() # 確保數據已提交到數據庫
                        return jsonify({
                            "ok": True,
                        }),200
                    finally:
                        cursor.close()
                        connection.close()
                    
            elif token == None:#沒有token
                return jsonify({
                    "error": True,
                    "message": "未登入"
                }), 403
            else: 
                return jsonify({
                    "error": True,
                    "message": "伺服器內部錯誤"
                }), 500
#取得尚未下單的預定行程
    if request.method=="GET": 
        token = request.cookies.get("token")
        if token == None: #沒有token
            return jsonify({
                "error": True,
                "message": "未登入"
            }), 403
        else:
            try:
                #連接資料庫
                connection = conpool.get_connection()
                cursor = connection.cursor(dictionary=True)
                #解TOKEN並記錄使用者編號
                decoded_jwt = jwt.decode(token, "secret", algorithms=['HS256'])  #解開TOKEN
                #利用得到的TOKEN去查詢使用者的預訂資料，以及其他表內的相關資料
                cursor.execute('''SELECT booking.user_id, booking.order_date, booking.attraction_id, attractions.name,attractions.address,attractions.file, booking.date,booking.time,booking.price 
                                FROM booking 
                                JOIN attractions 
                                ON attraction_id = _id   
                                WHERE booking.user_id= %s
                                ORDER BY booking.order_date DESC
                                LIMIT 1;''',(decoded_jwt["id"],))
                result = cursor.fetchone()
                if result !=None: #有相關預定資料
                    return jsonify({
                        "data": {
                            "attraction": {
                                "id": result["attraction_id"],
                                "name": result["name"],
                                "address": result["address"],
                                "image": result["file"].split(",")[0]
                            },
                            "date": result["date"].strftime("%Y-%m-%d"),
                            "time": result["time"],
                            "price": result["price"]
                        }
                        }), 200
                else:#沒有預定資料
                    return jsonify({
                            "data":None
                        }), 200
            finally:
                cursor.close()
                connection.close() 
#刪除目前的預定行程
    if request.method=="DELETE":
        token = request.cookies.get("token")
        if token == None: #沒有token
            return jsonify({
                "error": True,
                "message": "未登入"
            }), 403
        else:
            try:
                #連接資料庫
                connection = conpool.get_connection()
                cursor = connection.cursor(dictionary=True)
                #解TOKEN並記錄使用者編號
                decoded_jwt = jwt.decode(token, "secret", algorithms=['HS256'])  #解開TOKEN
                #利用得到的TOKEN去查詢使用者的預訂資料，以及其他表內的相關資料    
                cursor.execute("DELETE FROM booking WHERE user_id = %s ORDER BY booking.order_date DESC LIMIT 1;",(decoded_jwt["id"],))
                connection.commit() # 確保數據已提交到數據庫
                return jsonify({
                    "ok": True,
                }),200
            finally:
                cursor.close()
                connection.close()
        