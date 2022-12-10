#---------------------------讀取模組---------------------------------------------------------------------#
from flask import *
from flask import Blueprint, render_template, abort
# from ..pool import conpool
import sys
sys.path.append('../')
from pool import conpool
#---------------------------Blueprint---------------------------------------------------------------------#
categories = Blueprint('categories', __name__, static_folder='static',template_folder='templates',url_prefix='')
#---------------------------取得景點分類名稱列表   /api/categories methods=['GET']---------------------------------------------------------------------#
#@simple_page.route('/<page>')
@categories.route("/api/categories",methods=["GET"])
def api_categories():
    try:
        connection = conpool.get_connection()
        cursor = connection.cursor(dictionary=True)
        #開始連結資料庫，抓出需要的欄位部分的所有資料 
        cursor.execute("SELECT DISTINCT CAT FROM attractions;")#過濾掉相同的值
        categoriesResult = cursor.fetchall()
        categoriesCount= len(categoriesResult)
        categorieslist=[]
        for i in range(categoriesCount):
            newcategoriesResult=categoriesResult[i]['CAT']
            categorieslist.append(newcategoriesResult)

        #如果有categories相關資料的話
        if categoriesCount >0:
            json_categoriesdata={                        
                            "data": categorieslist
            }				
            return jsonify(json_categoriesdata),200

        else:
            return jsonify({
                "error": True,
                "message": "無分類資料"
            }),500
    finally:
        cursor.close()
        connection.close()
