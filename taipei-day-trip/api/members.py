#---------------------------讀取模組---------------------------------------------------------------------#
from flask import *
from flask import Blueprint, render_template, abort
from flask import Flask, make_response
from flask import request 
from datetime import datetime
from datetime import date
import jwt  #JSON Web Token
from flask_bcrypt import Bcrypt # 密碼雜湊化Hash函式庫 https://medium.com/seaniap/python-web-flask-如何雜湊化使用者密碼-b6dec03c3332
import sys
sys.path.append('../')
from pool import conpool
import re
# import boto3  # S3
#---------------------------Blueprint---------------------------------------------------------------------#
member = Blueprint('member', __name__, static_folder='static',template_folder='templates',url_prefix='')
member_upload_pic = Blueprint('member_upload_pic', __name__, static_folder='static',template_folder='templates',url_prefix='')
#---------------------------Bcrypt---------------------------------------------------------------------#
#根據使用者的編號取得訂單資料 /api/member  methods=['GET']
@member.route("/api/member",methods=["GET"])
def api_member():
    token = request.cookies.get("token")
    if token != None: #有token
        try:
            #連接資料庫
            connection = conpool.get_connection()
            cursor = connection.cursor(dictionary=True)
            #解TOKEN並記錄使用者編號
            decoded_jwt = jwt.decode(token, "secret", algorithms=['HS256'])  #解開TOKEN
            #依照顧客的ID去抓出訂單資訊
            cursor.execute("SELECT order_id,+attraction_id,attraction_name,attraction_address,attraction_img,reserved_date,reserved_time,contact_name,contact_email,contact_phone,payment_price FROM orders WHERE payment_status = %s and user_id= %s ORDER BY payment_time DESC LIMIT 5;",(True,decoded_jwt["id"],))
            result = cursor.fetchall()
            if len(result)!=0:
                datalist=[] #頁面要呈現的5筆資料
                for i in range(len(result)):  
                    data= {
                        "number":result[i]["order_id"],
                        "price": result[i]["payment_price"],
                        "trip": {
                            "attraction": {
                                "id": result[i]["attraction_id"],
                                "name": result[i]["attraction_name"],
                                "address": result[i]["attraction_address"],
                                "image": result[i]["attraction_img"]
                            },
                            "date": result[i]["reserved_date"].strftime("%Y-%m-%d"),
                            "time": result[i]["reserved_time"]
                        },
                        "contact": {
                            "name": result[i]["contact_name"],
                            "email": result[i]["contact_email"],
                            "phone": result[i]["contact_phone"]
                        }
                    }
                    datalist.append(data)
                json_data={
                            "data":datalist
                }                         
                return jsonify(
                        json_data             
                ), 200
            else:  
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

#接收使用者傳送的圖片將照片傳送到到AWS S3存儲桶    /api/member/upload-pic  methods=['POST']  
# 設置S3連接
    # s3 = boto3.client(
    #     's3',
    #     aws_access_key_id='AKIAZX5ENUOBPO67LGQZ', # 獲取AWS訪問密鑰和密鑰ID
    #     aws_secret_access_key='qDOnFFNeWZk3NyApuiSUO9GAwdzHWVr8tLzh4U8t'
    # )
# @member_upload_pic.route("/api/member/upload-pic",methods=["POST"])
# def api_member_pic():
#     #從前端接收資料
#     formData = request.files["formData"]
#     try:
#         filename = secure_filename(formData.filename)
#         acl="public-read"
#         s3.upload_fileobj(
#             file,
#             'bucket-name',
#             file.filename,
#             ExtraArgs={
#                 "ACL": acl,
#                 "ContentType":  file.content_type
#             }
#         )
        
#     except Exception as e:
#             resp = jsonify(e)
#             resp.status_code =200
#             return resp


    # # 上傳照片到S3存儲桶
    # s3.upload_file('/path/to/local/image.jpg', 'smallgirl6', 'image.jpg')
    # picture_url = s3.generate_presigned_url(
    #         ClientMethod = "get_object",
    #         Params = {
    #             "Bucket": os.getenv("BUCKET_NAME"),
    #             "Key": picture_name
    #         }
    #     )
