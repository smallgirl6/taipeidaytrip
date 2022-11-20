#中文顯示
from asyncio.windows_events import NULL
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#---------------------------讀取.env的環境變數---------------------------------------------------------------------#
import os
from dotenv import load_dotenv
import MySQLdb

load_dotenv()
connection = MySQLdb.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DATABASE"),
    charset=os.getenv("charset") #加這一行(utf8)可以不會讓中文變亂碼
)
#連線到MySQL資料庫
cursor = connection.cursor() # 獲取操作游標，也就是開始操作
#---------------------------資料庫作業---------------------------------------------------------------------#
import json
import pymysql

#取得表頭
taipei_json = open(r"taipei-attractions.json", "r",encoding='UTF-8')
taipei = taipei_json.read()
taipei_data = json.dumps(taipei)
taipei_data  = json.loads(taipei)
data = taipei_data ["result"]["results"] #列表
count = len(data)#共有幾筆資料 

#對照每筆key值和Mysql表頭是否一樣 並存放到Mysql中
table_header =[]
for key in data[0]:
    table_header.append(key)

#把每一筆資料一一放入資料庫中
i = 0
while i < count:
    rate =data[i][table_header[0]]
    direction = data[i][table_header[1]]
    name = data[i][table_header[2]]
    date = data[i][table_header[3]]
    longitude = data[i][table_header[4]]
    ref_wp = data[i][table_header[5]]
    avBegin = data[i][table_header[6]]
    langinfo = data[i][table_header[7]]
    mrt = data[i][table_header[8]]
    serial_no = data[i][table_header[9]]
    rowNumber = data[i][table_header[10]]
    cat = data[i][table_header[11]]
    memo_time = data[i][table_header[12]]
    poi = data[i][table_header[13]]
    idpt = data[i][table_header[15]]
    latitude = data[i][table_header[16]]
    description = data[i][table_header[17]]
    id = data[i][table_header[18]]
    avEnd = data[i][table_header[19]]
    address = data[i][table_header[20]]

    #把放圖片的file格內只取出後面是.png和.jpg的檔案
    #先把每個網址都用逗號隔開（把關鍵字http後面加一個逗號，再用split抓到逗號分割每筆資料）
    addcomma =(data[i][table_header[14]].replace("http", ",http")).split(",")
    #每串網址如果後4位是".jpg" or ".png"放到(加到)picstring字串中
    picstring= ""
    for j in addcomma:
        if j[-4::].lower() == (".jpg" or ".png"):
            picstring += j
    #API圖片資料為陣列格式所以在這邊先把每筆圖片用逗號隔開 陣列格式
    picstringSplit= picstring.replace("http",",http")
    picstringSplitN = picstringSplit[1:]
    
    #準備放插入資料庫
    value = [rate,direction, name, date, longitude, ref_wp, avBegin, langinfo, mrt, serial_no, rowNumber, cat, memo_time, poi, picstringSplitN, idpt, latitude, description, id, avEnd, address]
    sql_insert ="insert into attractions values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(sql_insert,value)  
    i = i+1

connection.commit()
connection.close()