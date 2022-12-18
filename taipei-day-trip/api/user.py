#---------------------------讀取模組---------------------------------------------------------------------#
from flask import *
from flask import Blueprint, render_template, abort
from flask import Flask, make_response
from flask import request 
import jwt  #JSON Web Token
from flask_bcrypt import Bcrypt # 密碼雜湊化Hash函式庫 https://medium.com/seaniap/python-web-flask-如何雜湊化使用者密碼-b6dec03c3332
import sys
sys.path.append('../')
from pool import conpool
#---------------------------Blueprint---------------------------------------------------------------------#
user = Blueprint('user', __name__, static_folder='static',template_folder='templates',url_prefix='')
user_auth = Blueprint('user_auth', __name__, static_folder='static',template_folder='templates',url_prefix='')
#---------------------------Bcrypt---------------------------------------------------------------------#
bcrypt = Bcrypt() #建立Bcrypt實體並指定給變數bcrypt
#-------------------------取得景點資料列表API  /api/attractions?page=${page}&keyword=${keyword} methods=['GET']---------------------------------------------------------------------# 
#會員註冊/signup功能
@user.route("/api/user",methods=["POST"])
def api_user():
    #從前端接收資料
    get_front_jsondata = request.get_json()
    signup_name =get_front_jsondata["name"]
    signup_email=get_front_jsondata["email"]
    signup_password =get_front_jsondata["password"]
    #檢查member表中email欄位是否有相同email的資料
    try:
        connection = conpool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM member WHERE email = %s",(signup_email,))#username,逗號不可刪
        result = cursor.fetchone() 
        #如果找到相同email的話，顯示帳號已經被註冊
        if result != None:
            return jsonify({
                "error": True,
                "message": "此信箱已經被註冊"
            }),400    
        #姓名、email、密碼不可以空白
        if (len(signup_name)== 0) or (len(signup_email)== 0) or (len(signup_password)== 0):
            return jsonify({
                "error": True,
                "message": "請輸入姓名、信箱、密碼"
            }),400
        #如果沒有找到相同email的話，則將資料插入資料庫完成註冊
        if result == None:
            #加密使用者輸入的密碼
            hashed_signup_password = bcrypt.generate_password_hash(password=signup_password)
            insert_to_membertable = "INSERT INTO member (name, email, password)  VALUES ( %s, %s, %s)"
            val_membertable = (signup_name,signup_email,hashed_signup_password)
            cursor.execute(insert_to_membertable, val_membertable)  
            connection.commit() # 確保數據已提交到數據庫
            return jsonify({
                "ok": True,
            }),200
        else:
            return jsonify({
                "error": True,
                "message": "伺服器內部錯誤"
            }),500
    finally:
        cursor.close()
        connection.close()


# 會員登入/signin 取得當前登入的會員資訊/member 登出/signup
@user_auth.route("/api/user/auth",methods=["GET","PUT","DELETE"])
def api_user_auth():

    if request.method=="PUT": #會員登入/signin
        #從前端接收資料
        get_front_jsondata = request.get_json()
        signin_email=get_front_jsondata["email"]
        signin_password =get_front_jsondata["password"] 
        #根據接收到的資料跟資料庫作互動
        try:
            connection = conpool.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM member WHERE email = %s ",(signin_email,))
            email_result = cursor.fetchone()
            #如果找不到對應資料將導向錯誤頁面
            if (len(signin_email) or len(signin_password)) == 0:
                return jsonify({
                    "error": True,
                    "message": "請輸入信箱、密碼" #沒輸入信箱或密碼
                }),400
            if (email_result == None) and (len(signin_email) or len(signin_password) > 0):
                return jsonify({
                    "error": True,
                    "message": "信箱或是密碼錯誤" #無此信箱
                }),400
            cursor.execute("SELECT password FROM member WHERE email = %s ",(signin_email,))
            password_result = cursor.fetchone()
            check_password = bcrypt.check_password_hash(password_result["password"],signin_password)#比對密碼是否正確
            if (check_password == False) and (len(signin_email) or len(signin_password) > 0):
                return jsonify({
                    "error": True,
                    "message": "信箱或是密碼錯誤" #密碼錯誤
                }),400
            if (check_password == True) and (len(signin_email) or len(signin_password) > 0):
                encoded_jwt = jwt.encode(email_result, "secret")  #做一個TOKEN
                content = jsonify({
                    "ok": True,
                })
                response = make_response(content)
                response.set_cookie(key="token",value=encoded_jwt,max_age=604800)
                return response,200
            else:
                return jsonify({
                    "error": True,
                    "message": "伺服器內部錯誤"                
                }),500
        finally:
            cursor.close()
            connection.close()

    if request.method=="GET":
        token = request.cookies.get("token")
        if token != None:
            decoded_jwt = jwt.decode(token, "secret", algorithms=['HS256'])  #解開TOKEN
            return jsonify({ #將解密後的結果回傳給前端
                "data": {
                    "id": decoded_jwt["id"],
                    "name": decoded_jwt["name"],
                    "email": decoded_jwt["email"]
                }
            }),200
        else:    
            return jsonify({
                "data":None
            })
            
    if request.method=="DELETE":
        content = jsonify({
                    "ok": True,
                })
        response = make_response(content)
        response.set_cookie(key="token",value="",max_age=-1,expires=0)
        return response,200
      
