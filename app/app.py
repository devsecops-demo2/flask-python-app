from flask import Flask, abort, redirect, url_for, request
from markupsafe import escape # This is important to avoid Cross Site Scripting (XSS) attacks.
import mysql.connector
import json
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/welcome/<name>')
def welcome(name):
    return 'welcome %s' % name

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('welcome', name=user))
    else:
        user = request.args.get('name')
        return redirect(url_for('welcome', name=user))

@app.route('/logout/')
def logout():
    return '<h1> You are kicked off</h1>'

@app.route('/about/')
def about():
    return '<h3>This is a Flask web application.</h3>'

#Dynamic routes
@app.route('/capitalize/<word>/')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))

@app.route('/users/<int:user_id>/')
def greet_user(user_id):
    users = ['Raj', 'Piyu', 'Aarohi']
    try:
        return '<h2>Hi {}</h2>'.format(users[user_id])
    except IndexError:
        abort(404)

@app.route('/widgets')
def get_widgets():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password=os.environ.get('DB_PASSWORD'),
        database="inventory"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM widgets")
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()
    return json.dumps(json_data)

@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password=os.environ.get('DB_PASSWORD')
    )
    cursor = mydb.cursor()
    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password=os.environ.get('DB_PASSWORD'),
        database="inventory"
    )
    cursor = mydb.cursor()
    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    
    sql = "INSERT INTO widgets (name, description) VALUES (%s, %s)"
    val = ("Apple iPhone", "The iPhone is a smartphone made by Apple that combines a computer, iPod, digital camera and cellular phone into one device with a touchscreen interface.")
    cursor.execute(sql, val)
    sql = "INSERT INTO widgets (name, description) VALUES (%s, %s)"
    val = ("OnePlus SmartPhones", "OnePlus models are unlocked Android smartphones with quad-core Snapdragon CPUs and up to 8GB RAM that initially ran the Cyanogen version of Android (Cyanogen was later replaced with the company's own Android-based OxygenOS).")
    cursor.execute(sql, val)
    sql = "INSERT INTO widgets (name, description) VALUES (%s, %s)"
    val = ("Samsung SmartPhones", "Samsung Galaxy devices use the Android operating system produced by Google, with a custom user interface called One UI (with previous versions being known as Samsung Experience and TouchWiz).")
    cursor.execute(sql, val)
    cursor.close()
    mydb.commit()

    return 'init database'