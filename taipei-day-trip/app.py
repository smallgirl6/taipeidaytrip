#---------------------------讀取.env的環境變數---------------------------------------------------------------------#
import os
from dotenv import load_dotenv
import mysql.connector   #載入MSQL
load_dotenv()

connection1 = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DATABASE"),
    charset=os.getenv("charset") #加這一行(utf8)可以不會讓中文變亂碼
)
connection2 = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DATABASE"),
    charset=os.getenv("charset") #加這一行(utf8)可以不會讓中文變亂碼
)
#----------------------python flask網站後端相關設定--------------------------------------------------------------------------#
import json
from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False  #防止Flask jsonify對數據進行排序
# #----------------------python flask網站後端--------------------------------------------------------------------------#

# 取得景點資料列表API         
# /api/attractions?page=${page}&keyword=${keyword} methods=['GET']
@app.route("/api/attractions",methods=["GET"])
def attractions():
    cursor1 = connection1.cursor() # 獲取操作游標，也就是開始操作
    #GET前端頁數或是關鍵字資料
    page=request.args.get("page")
    page=int(page)
    keyword=request.args.get("keyword")

    #分頁設定(開頭)
    pageSize= int(12) #顯示12個景點
    start = page*pageSize #根據使用者輸入頁數判斷要從哪筆資料開始呈現，第0頁為0開始(0...12...24)

    #開始連結資料庫，根據使用者輸入的頁數抓出需要的欄位部分的所有資料(for只輸入頁數的部分)
    cursor1.execute("SELECT _id,name,CAT,description,address,direction,MRT,latitude,langinfo,file FROM attractions LIMIT %s OFFSET %s",(pageSize,start,))#keyword,逗號不可刪
    pageResult = cursor1.fetchall() 
    cursor1.execute("SELECT COUNT(*) FROM attractions")#查看看有幾筆資料
    alldataCount = cursor1.fetchone()
    alldataCount =int(alldataCount[0])
    

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
                                "id":pageResult[i][0],
                                "name": pageResult[i][1],
                                "category": pageResult[i][2],
                                "description": pageResult[i][3],
                                "address": pageResult[i][4],
                                "transport": pageResult[i][5],
                                "mrt": pageResult[i][6],
                                "lat": pageResult[i][7],
                                "lng": pageResult[i][8],
                                "images": pageResult[i][9].split(",")
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
        cursor1.execute("SELECT _id,name,CAT,description,address,direction,MRT,latitude,langinfo,file FROM attractions WHERE name LIKE %s or CAT= %s LIMIT %s OFFSET %s",('%'+keyword+'%',keyword,pageSize,start,))
        keywordResult = cursor1.fetchall()
        keywordResulCount= len(keywordResult)
        #有在資料庫找到相似的keyword的話
        if  keywordResulCount>0:            
            cursor1.execute("SELECT COUNT(*) FROM attractions WHERE name LIKE %s or CAT= %s",('%'+keyword+'%',keyword,))#查看看有幾筆資料
            keywordResultCount = cursor1.fetchone() 
            keywordResultCount =int(keywordResultCount[0])

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
                                    "id":keywordResult[i][0],
                                    "name": keywordResult[i][1],
                                    "category": keywordResult[i][2],
                                    "description": keywordResult[i][3],
                                    "address": keywordResult[i][4],
                                    "transport": keywordResult[i][5],
                                    "mrt": keywordResult[i][6],
                                    "lat": keywordResult[i][7],
                                    "lng": keywordResult[i][8],
                                    "images": keywordResult[i][9].split(",")
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


#根據景點編號取得景點資料 /api/attraction/{attractionId}  methods=['GET']
@app.route("/api/attraction/<attractionId>",methods=["GET"])
def api_attraction(attractionId):
    #如果輸的景點編號是數字
    if attractionId.isdigit()==True :
        #開始連結資料庫，根據使用者輸入的景點編號抓出需要的欄位部分的所有資料
        cursor2 = connection1.cursor() # 獲取操作游標，也就是開始操作
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
    

# 取得景點分類名稱列表   /api/categories methods=['GET']
@app.route("/api/categories",methods=["GET"])
def api_categories():
    cursor3 = connection2.cursor() # 獲取操作游標，也就是開始操作
    #開始連結資料庫，抓出需要的欄位部分的所有資料 
    cursor3.execute("SELECT DISTINCT CAT FROM attractions;")#過濾掉相同的值
    categoriesResult = cursor3.fetchall()
    categoriesCount= len(categoriesResult)
    categorieslist=[]
    for i in range(categoriesCount):
        newcategoriesResult=categoriesResult[i][0]
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

@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


app.run(host="0.0.0.0",port=3000)	

