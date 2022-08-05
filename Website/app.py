from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb.cursors

import sys
sys.path.append("..")
import database as db

app = Flask(__name__)
mysql = MySQL()

host, user, password, database = db.get_credentials()

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = database
mysql = MySQL(app)

@app.route("/")
def main():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT name FROM primeministers WHERE enddate IS NULL')     # Query to fetch current PM
    current_pm = cursor.fetchone()

    cursor.execute('SELECT date FROM qa_pairs ORDER BY DATE DESC LIMIT 1')      # Query to fetch most recent date of a PMQ session
    most_recent_session = cursor.fetchone()['date'].strftime("%A %d %B %Y")

    cursor.execute('SELECT AVG(ANSWER_RELEVANCE) as average FROM qa_pairs WHERE date = (SELECT date FROM qa_pairs ORDER BY date DESC LIMIT 1)')
    most_recent_average = f"{cursor.fetchone()['average']:.2%}"

    return render_template('index.html', current_pm=current_pm, session=most_recent_session, average=most_recent_average)

@app.route("/search")
def search():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT name, startdate, enddate FROM primeministers')
    primeministers = cursor.fetchall()
    
    return render_template('search.html', primeministers=primeministers)

@app.route("/compare")
def compare():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT name, startdate, enddate FROM primeministers')
    primeministers = cursor.fetchall()

    return render_template('compare.html', primeministers=primeministers)
        
@app.route("/upload")
def upload():
    return render_template('upload.html')
    
if __name__ == "__main__":
    app.run()