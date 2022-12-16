#---------------------------讀取模組---------------------------------------------------------------------#
from flask import *
from flask import Blueprint, render_template, abort
import sys
sys.path.append('../')
from pool import conpool
#---------------------------Blueprint---------------------------------------------------------------------#
attractions = Blueprint('attractions', __name__, static_folder='static',template_folder='templates',url_prefix='')
attraction = Blueprint('attraction', __name__, static_folder='static',template_folder='templates',url_prefix='')
#-------------------------取得景點資料列表API  /api/attractions?page=${page}&keyword=${keyword} methods=['GET']---------------------------------------------------------------------# 
@attractions.route("/api/attractions",methods=["GET"])
def api_attractions():
    try:
        connection = conpool.get_connection()
        cursor = connection.cursor(dictionary=True)
        # cursor1 = connection1.cursor() # 獲取操作游標，也就是開始操作
        #GET前端頁數或是關鍵字資料
        page=request.args.get("page")
        page=int(page)
        keyword=request.args.get("keyword")

        #分頁設定(開頭)
        pageSize= int(12) #顯示12個景點
        start = page*pageSize #根據使用者輸入頁數判斷要從哪筆資料開始呈現，第0頁為0開始(0...12...24)

        #開始連結資料庫，根據使用者輸入的頁數抓出需要的欄位部分的所有資料(for只輸入頁數的部分)
        cursor.execute("SELECT _id,name,CAT,description,address,direction,MRT,latitude,langinfo,file FROM attractions LIMIT %s OFFSET %s",(pageSize,start,))#keyword,逗號不可刪
        pageResult = cursor.fetchall() 
        cursor.execute("SELECT COUNT(*) FROM attractions")#查看看有幾筆資料
        alldataCount = cursor.fetchone()
        alldataCount =int(alldataCount['COUNT(*)'])
        
        #最後一頁的值lastpage，如果總資料數剛好能被12給整除，那跑出的結果會不一樣
        pageCount= alldataCount /pageSize #總共有幾頁  目前為4.833333333333333 　 大約是5頁(第0頁到第4頁)
        if pageCount==int(pageCount): #假設共有60筆/12＝5.0，5.0=5，實際4頁所以取整數4 1
            lastpage=int(pageCount-1)#剛好整除的狀況就pageCount-1
        else:
            lastpage=int(pageCount)  #58/12＝4.8333取整數4 不能被整除的話就取整數部分

        #下一頁的值，如果這一頁剛好是最後一頁，回傳下一頁為NULL
        if page==lastpage:
            nextPage=None
        else:
            nextPage=page+1
        
        #沒有關鍵字的話
        if keyword==None:
            #如果下一頁不是NULL就回傳使用者輸入的頁面的資料
            if page<lastpage+1:
                pageReturnlist=[] #頁面要呈現的12筆資料
                for i in range(len(pageResult)):#遍歷pageResult篩選的的12筆資料
                    pageReturndata={
                                "id":pageResult[i]["_id"],
                                "name": pageResult[i]["name"],
                                "category": pageResult[i]["CAT"],
                                "description": pageResult[i]["description"],
                                "address": pageResult[i]["address"],
                                "transport": pageResult[i]["direction"],
                                "mrt": pageResult[i]["MRT"],
                                "lat": pageResult[i]["latitude"],
                                "lng": pageResult[i]["langinfo"],
                                "images": pageResult[i]["file"].split(",")
                    }                             
                    pageReturnlist.append(pageReturndata)#抓出這一頁(12個景點)的全部資料，放入pageReturnlist中
                json_pagedata={
                            "nextPage": nextPage,
                            "data":pageReturnlist
                }
                return jsonify(json_pagedata),200
            
            else:
                return jsonify({
                    "error": True,
                    "message": "沒有此頁面"
                }),500

        #若是有關鍵字的話，在資料庫搜尋相似關鍵字
        if keyword !=None:
        #開始連結資料庫，根據使用者輸入的keywor抓出需要的欄位部分的所有類似資料 比對景點分類、或模糊比對景點名稱的關鍵字
            cursor.execute("SELECT _id,name,CAT,description,address,direction,MRT,latitude,langinfo,file FROM attractions WHERE name LIKE %s or CAT= %s LIMIT %s OFFSET %s",('%'+keyword+'%',keyword,pageSize,start,))
            keywordResult = cursor.fetchall()
            keywordResulCount= len(keywordResult)
            #有在資料庫找到相似的keyword的話
            if  keywordResulCount>0:            
                cursor.execute("SELECT COUNT(*) FROM attractions WHERE name LIKE %s or CAT= %s",('%'+keyword+'%',keyword,))#查看看有幾筆資料
                keywordResultCount = cursor.fetchone() 
                keywordResultCount =int(keywordResultCount['COUNT(*)'])

                #最後一頁的值lastpage，如果總資料數剛好能被12給整除，那跑出的結果會不一樣
                keywordpageCount= keywordResultCount/pageSize #總共有幾頁  可能可能為小數
                if keywordpageCount==int(keywordpageCount): #假設共有12筆/12＝1.0，1.0=5，實際1頁所以取整數0
                    keywordlastpage=int(keywordpageCount-1)#剛好整除的狀況就pageCount-1
                else:
                    keywordlastpage=int(keywordpageCount)  #8/12＝0.666取整數0 不能被整除的話就取整數部分
                
                #下一頁的值，如果輸入了比最後一頁還要大的值，回傳下一頁為NULL
                if page==keywordlastpage:
                    keywordnextPage=None
                else:
                    keywordnextPage=page+1
                
                #如果判斷關鍵字輸入的頁數不是最後一頁，傳回輸入頁的資料，超過此頁的話傳回沒有此頁
                if page<keywordlastpage+1:
                    keywordReturnlist=[] #頁面要呈現的12筆資料
                    for i in range(len(keywordResult)):#遍歷pageResult篩選的的12筆資料
                        json_keyworddata={
                                    "id":keywordResult[i]["_id"],
                                    "name": keywordResult[i]["name"],
                                    "category": keywordResult[i]["CAT"],
                                    "description": keywordResult[i]["description"],
                                    "address": keywordResult[i]["address"],
                                    "transport": keywordResult[i]["direction"],
                                    "mrt": keywordResult[i]["MRT"],
                                    "lat": keywordResult[i]["latitude"],
                                    "lng": keywordResult[i]["langinfo"],
                                    "images": keywordResult[i]["file"].split(",")
                        }
                        keywordReturnlist.append(json_keyworddata)#抓出keyword(一頁最大12個景點)放入keywordReturnlist中
                    json_keyworddata={
                                "nextPage": keywordnextPage,
                                "data":keywordReturnlist
                    }    
                    return jsonify(json_keyworddata),200
            if  keywordResulCount==0:
                return jsonify({
                    "error": True,
                    "message": "找不到此關鍵字"
                }),500
    finally:
            cursor.close()
            connection.close()

#根據景點編號取得景點資料 /api/attraction/{attractionId}  methods=['GET']
@attraction.route("/api/attraction/<attractionId>",methods=["GET"])
def api_attraction(attractionId):
    try:
        #如果輸的景點編號是數字
        if attractionId.isdigit()==True :
            #開始連結資料庫，根據使用者輸入的景點編號抓出需要的欄位部分的所有資料
            connection = conpool.get_connection()
            cursor2 = connection.cursor(dictionary=True)
            cursor2 = connection.cursor() # 獲取操作游標，也就是開始操作
            cursor2.execute("SELECT _id,name,CAT,description,address,direction,MRT,latitude,langinfo,file FROM attractions WHERE _id = %s",(attractionId,))#keyword,逗號不可刪
            attractionIdResult = cursor2.fetchall()
            attractionIdResultCount= len(attractionIdResult)
            #有在資料庫找到相似的attractionId的話 
            if attractionIdResultCount >0:
                json_attractiondata={
                                "data": {
                                    "id":attractionIdResult[0][0],
                                    "name": attractionIdResult[0][1],
                                    "category": attractionIdResult[0][2],
                                    "description":attractionIdResult[0][3],
                                    "address": attractionIdResult[0][4],
                                    "transport": attractionIdResult[0][5],
                                    "mrt": attractionIdResult[0][6],
                                    "lat": attractionIdResult[0][7],
                                    "lng": attractionIdResult[0][8],
                                    "images": attractionIdResult[0][9].split(",")
                                }					
                }
                return jsonify(json_attractiondata),200

            if  attractionIdResultCount==0:
                    return jsonify({
                        "error": True,
                        "message": "景點編號不正確"
                    }),400
        else:
            return jsonify({
                "error": True,
                "message": "伺服器內部錯誤"
            }),500
    finally:
            cursor2.close()
            connection.close()