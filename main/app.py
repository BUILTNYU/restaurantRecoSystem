from flask import Flask, render_template, request, session, url_for, redirect,make_response,jsonify
import pymysql.cursors
import main
import json
from flask_cors import CORS,cross_origin

from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

# initiate flask framework and allow cross origin resource sharing
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = '2y14ZhoB0P'

#connect to database
conn = pymysql.connect(host='localhost',
                    port = 8889,
                    user='root',
                    password='root',
                    db='UrbanConnector',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)


# update the RecommendationsSevenDays once every morning at 5 am
scheduler = BackgroundScheduler()
start_time = datetime(2019, 8, 2, 5, 00, 00)
scheduler.add_job(main.update_database, "interval", days=1, start_date=start_time, args=[conn])
scheduler.start()



__ALPHA__ = 1
@app.route('/')
def default():
    return "Urban Connector"


@app.route('/getRecommendation:<user_profile>+<user_id>+<local_time>+<longitude>+<latitude>+<radius>+<price>', methods=['GET'])
def make_recommendation(user_profile, user_id, local_time, longitude, latitude, radius, price):
    longitude = float(longitude)
    latitude = float(latitude)
    radius = int(radius)
    price = int(price)
    return main.make_recommendation(user_profile, user_id, local_time, longitude, latitude, radius, price, __ALPHA__, conn)

@app.route('/feedback:<user_profile>+<user_id>+<local_time>+<restaurant_id>+<recommendation_time>+<reward>',methods=['GET'])
def feedback(user_profile, user_id, local_time, restaurant_id, recommendation_time, reward):
    # reward = int(reward)
    reward = float(reward)
    main.update_reward(user_profile, user_id, local_time, restaurant_id, recommendation_time, reward, __ALPHA__, conn)
    response = make_response(jsonify({"statusCode": 200}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'

    return response

if __name__ == "__main__":
    app.run('127.0.0.1', 8000, debug = True)
