# #----------------------python flask import模組--------------------------------------------------------------------------#
from flask import *
from flask import Blueprint, render_template, abort
# from yourapplication.simple_page import simple_page
from api.categories import categories
from api.attractions import attractions
from api.attractions import attraction
from api.user import user
from api.user import user_auth
from api.booking import booking
from api.orders import orders
from api.orders import order
#----------------------python flask網站後端相關設定--------------------------------------------------------------------------#
app=Flask(__name__)
# 註冊藍圖
#app.register_blueprint(simple_page, url_prefix='/pages')
app.register_blueprint(categories, url_prefix='')
app.register_blueprint(attractions, url_prefix='')
app.register_blueprint(attraction, url_prefix='')
app.register_blueprint(user, url_prefix='')
app.register_blueprint(user_auth, url_prefix='')
app.register_blueprint(booking, url_prefix='')
app.register_blueprint(orders, url_prefix='')
app.register_blueprint(order, url_prefix='')
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False  #防止Flask jsonify對數據進行排序
# #------------------------------------------------------------------------------------------------#

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
