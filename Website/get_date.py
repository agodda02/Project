from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb.cursors
import pytest
from datetime import date, datetime, timedelta

# Changes the path, so that the database module can be imported
import sys
sys.path.append("..")
import database as db

def get_nearest_date(datefrom, dateto)
    app = Flask(__name__)
    mysql = MySQL()

    host, user, password, database = db.get_credentials()

    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = database
    mysql = MySQL(app)      
    
    
