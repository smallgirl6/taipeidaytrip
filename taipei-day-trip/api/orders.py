#---------------------------讀取模組---------------------------------------------------------------------#
from flask import *
from flask import Blueprint, render_template, abort
from flask import Flask, make_response
from flask import request 
import requests
import jwt  #JSON Web Token
from flask_bcrypt import Bcrypt 
from datetime import datetime
from datetime import date
import sys
sys.path.append('../')
import os
from dotenv import load_dotenv
load_dotenv()
from pool import conpool
#---------------------------Blueprint---------------------------------------------------------------------#
orders = Blueprint('orders', __name__, static_folder='static',template_folder='templates',url_prefix='')
order = Blueprint('order', __name__, static_folder='static',template_folder='templates',url_prefix='')
#---------------------------Bcrypt---------------------------------------------------------------------#
#處理訂單
@orders.route("/api/orders",methods=["POST"])
def api_orders():
    token = request.cookies.get("token")
    if token != None: #有token
        #從前端接收資料
        get_front_jsondata= request.get_json()
        if get_front_jsondata["prime"]=="":
            return jsonify({  #前端資料不完整
                "error": True,
                "message": "訂單建立失敗，請確認信用卡資料是否填寫完整"
            }), 400
        elif get_front_jsondata["order"]["contact"]["name"]=="" or get_front_jsondata["order"]["contact"]["email"]=="" or get_front_jsondata["order"]["contact"]["phone"]=="":  
            return jsonify({  #前端資料不完整
                "error": True,
                "message": "訂單建立失敗，請確認所有聯絡資料都已填入"
            }), 400
        else:#有token且前端資料也完整即建立訂單編號和資料，紀錄訂單付款狀態為【未付款】。
            try:
            #連接資料庫
                connection = conpool.get_connection()
                cursor = connection.cursor(dictionary=True)
                #解TOKEN並記錄使用者編號
                decoded_jwt = jwt.decode(token, "secret", algorithms=['HS256'])  #解開TOKEN
                #防止異常或重複訂單
                cursor.execute('''SELECT payment_time FROM orders
                                WHERE attraction_id=%s and reserved_date=%s and reserved_time=%s and contact_name=%s and contact_email=%s and contact_phone=%s and payment_price=%s and payment_status=%s;'''
                                ,(get_front_jsondata["order"]["trip"]["attraction"]["id"],get_front_jsondata["order"]["trip"]["date"],get_front_jsondata["order"]["trip"]["time"],get_front_jsondata["order"]["contact"]["name"],get_front_jsondata["order"]["contact"]["email"],get_front_jsondata["order"]["contact"]["phone"],get_front_jsondata["order"]["price"],True,))
                result = cursor.fetchone()
                if result!=None and (datetime.now() - result['payment_time']).total_seconds()<=30:
                    return jsonify({  
                        "error": True,
                        "message": "請勿重複提交訂單"
                    }), 400
                #做一個獨一無二的訂單編號
                now= datetime.now()
                orderid= str(now.strftime("%Y%m%d%H%M%S")) + str(decoded_jwt["id"])
                #插入資料
                insert_to_ordertable = "INSERT INTO orders (order_id,user_id, attraction_id, attraction_name, attraction_address, attraction_img, reserved_date, reserved_time, contact_name, contact_email, contact_phone, payment_price, payment_status)  VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val_ordertable = (orderid,decoded_jwt["id"], get_front_jsondata["order"]["trip"]["attraction"]["id"], get_front_jsondata["order"]["trip"]["attraction"]["name"], get_front_jsondata["order"]["trip"]["attraction"]["address"], get_front_jsondata["order"]["trip"]["attraction"]["image"], get_front_jsondata["order"]["trip"]["date"], get_front_jsondata["order"]["trip"]["time"],get_front_jsondata["order"]["contact"]["name"],get_front_jsondata["order"]["contact"]["email"],get_front_jsondata["order"]["contact"]["phone"],get_front_jsondata["order"]["price"],False)
                cursor.execute(insert_to_ordertable, val_ordertable)  
                connection.commit() # 確保數據已提交到數據庫
                #付款前先確認數據庫中pricetable中的價錢和orderstable的價錢是否相同
                cursor.execute('''SELECT orders.payment_price,prices.price
                                FROM orders
                                JOIN prices
                                ON reserved_time = item
                                WHERE orders.order_id=%s;''',(orderid,))
                result = cursor.fetchone()
                if result['payment_price']!=result['price']:#價格有可能被修改過或發生其他錯誤
                    cursor.execute("DELETE FROM booking WHERE user_id = %s ORDER BY booking.order_date DESC LIMIT 1;",(decoded_jwt["id"],))
                    connection.commit() # 確保數據已提交到數據庫
                    return jsonify({  
                        "error": True,
                        "message": "伺服器內部錯誤，請重新訂購"
                    }), 500
                #呼叫 TapPay 提供的付款 API ，提供必要付款資訊，完成付款動作(非3D交易)。
                url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"#測試環境 
                headers={
                        "Content-Type": "application/json",
                        "x-api-key": os.getenv("partner_key")
                }
                body={
                    "prime": get_front_jsondata["prime"],
                    "partner_key": os.getenv("partner_key"),
                    "merchant_id": "hyggenini_TAISHIN",#非3D交易
                    "details":"TapPay Test",
                    "amount": result['payment_price'], #交易金額
                    "cardholder": {
                        "phone_number": "+886923456789",
                        "name": "王小明",
                        "email": "LittleMing@Wang.com",
                        "zip_code": "100",
                        "address": "台北市天龍區芝麻街1號1樓",
                        "national_id": "A123456789"
                    },
                    "remember": True
                }
                
                response = requests.post(url,json=body,headers=headers)
                response_data = response.json()

                if response_data['status'] == 0: #付款成功更改訂單付款狀態為【已付款】並消除booking訂單導入tankyou頁面。
                    update_name_ordertable = "UPDATE orders SET payment_status = %s WHERE order_id = %s"
                    val_update_order = (True,orderid)
                    cursor.execute(update_name_ordertable, val_update_order)
                    connection.commit() # 確保數據已提交到數據庫
                    #消除booking訂單
                    cursor.execute("DELETE FROM booking WHERE user_id = %s ORDER BY booking.order_date DESC LIMIT 1;",(decoded_jwt["id"],))
                    connection.commit() # 確保數據已提交到數據庫
                    return jsonify({
                            "data": {
                            "number": orderid,
                            "payment": {
                                "status": response_data['status'],#0
                                "message": "付款成功"
                            }
                        }
                    }), 200
                if response_data['status']!= 0: #付款失敗
                    return jsonify({
                        "data": {
                            "number": orderid,
                            "payment": {
                                "status": response_data['status'],#0以外
                                "message": "付款失敗，請重新輸入您的信用卡資訊或向信用卡公司聯繫"
                            }
                        }
                    }), 200
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

#根據訂單編號取得訂單資料 /api/order/{orderNumber}  methods=['GET']
@order.route("/api/order/<orderNumber>",methods=["GET"])
def api_order(orderNumber):
    token = request.cookies.get("token")
    if token != None: #有token
        try:
            #連接資料庫
            connection = conpool.get_connection()
            cursor = connection.cursor(dictionary=True)
            #解TOKEN並記錄使用者編號
            decoded_jwt = jwt.decode(token, "secret", algorithms=['HS256'])  #解開TOKEN
            #依照顧客的ID和訂單編號去抓出訂單資訊
            cursor.execute("SELECT attraction_id,attraction_name,attraction_address,attraction_img,reserved_date,reserved_time,contact_name,contact_email,contact_phone,payment_price,payment_status FROM orders WHERE order_id = %s and user_id= %s;",(orderNumber,decoded_jwt["id"],))
            result = cursor.fetchone()
            if result["payment_status"]==True:  #1 #基本上能串接到這隻API的大部分是付款成功的情況
                return jsonify({
                        "data": {
                            "number":orderNumber,
                            "price": result["payment_price"],
                            "trip": {
                                "attraction": {
                                    "id": result["attraction_id"],
                                    "name": result["attraction_name"],
                                    "address": result["attraction_address"],
                                    "image": result["attraction_img"]
                                },
                                "date": result["reserved_date"],
                                "time": result["reserved_time"]
                            },
                            "contact": {
                                "name": result["contact_name"],
                                "email": result["contact_email"],
                                "phone": result["contact_phone"]
                            },
                            "status": result["payment_status"] #1
                        }               
                }), 200
            else:  #若強制輸入其他未付款的訂單號碼則不會顯示相關付款資訊
                return jsonify({
                        "data": None
                    })
        finally:
                cursor.close()
                connection.close() 
    else: #沒有token
        return jsonify({
            "error": True,
            "message": "未登入"
        }), 403

        
    
