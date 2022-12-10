import os
from dotenv import load_dotenv
import mysql.connector   #載入MSQL
from mysql.connector import pooling
load_dotenv()
connection = {
    "host":os.getenv("MYSQL_HOST"),
    "user":os.getenv("MYSQL_USER"),
    "passwd":os.getenv("MYSQL_PASSWORD"),
    "db":os.getenv("MYSQL_DATABASE"),
    "charset":os.getenv("charset") #加這一行(utf8)可以不會讓中文變亂碼
}
conpool=pooling.MySQLConnectionPool(pool_name="conpool",
                                    pool_size=10,
                                    pool_reset_session=True,
                                    **connection)