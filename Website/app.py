from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from datetime import date
from gensim import corpora, matutils
from gensim.models import LsiModel
import numpy as np
import MySQLdb.cursors

import sys
sys.path.append("..")
import database as db

sys.path.append("../Model")
import string_split

app = Flask(__name__)
Bootstrap(app)
datepicker(app)
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
    
    cursor.execute('SELECT id, name, startdate, enddate FROM primeministers')
    primeministers = cursor.fetchall()
    
    return render_template('search.html', primeministers=primeministers)
    
@app.route("/results", methods=['POST'])
def results():
    pm_id = request.form[list(request.form.to_dict().keys())[0]]
    datefrom = date.fromisoformat(request.form['from'])
    dateto = date.fromisoformat(request.form['to'])

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT id, name FROM primeministers WHERE id=%s', [pm_id])
    pm = cursor.fetchone()
    
    cursor.execute('SELECT AVG(answer_relevance) AS Average FROM qa_pairs WHERE pm=%s and date >= %s and date <= %s', (pm_id, datefrom, dateto))
    average = f"{cursor.fetchone()['Average']:.2%}"
    
    cursor.execute('SELECT author, date, question, answer, answer_relevance FROM qa_pairs WHERE pm=%s and date >= %s and date <= %s', (pm_id, datefrom, dateto))
    data = cursor.fetchall()
    
    for items in data:
        items['answer_relevance'] = f"{items['answer_relevance']:.2%}"
    
    return render_template('results.html', average=average, pm=pm, data=data, datefrom=datefrom.strftime("%A %d %B %Y"), dateto=dateto.strftime("%A %d %B %Y"))

@app.route("/compare")
def compare():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, name, startdate, enddate FROM primeministers')
    primeministers = cursor.fetchall()
    return render_template('compare.html', primeministers=primeministers)
        
@app.route("/comparison", methods=['POST'])
def comparison():
    pm1_id = request.form['pm1']
    pm2_id = request.form['pm2']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, name, startdate, enddate FROM primeministers WHERE id = %s', [pm1_id])
    pm1 = cursor.fetchone()
    cursor.execute('SELECT AVG(answer_relevance) as Average FROM qa_pairs WHERE pm = %s', [pm1_id])
    pm1_relevance = f"{cursor.fetchone()['Average']:.2%}"
    pm1.update({'Average': pm1_relevance})

    cursor.execute('SELECT id, name, startdate, enddate FROM primeministers WHERE id = %s', [pm2_id])
    pm2 = cursor.fetchone()
    cursor.execute('SELECT AVG(answer_relevance) as Average FROM qa_pairs WHERE pm = %s', [pm2_id])
    pm2_relevance = f"{cursor.fetchone()['Average']:.2%}"
    pm2.update({'Average': pm2_relevance})
    return render_template('comparison.html', pm1=pm1, pm2=pm2)
        
@app.route("/upload")
def upload():
    return render_template('upload.html')
    
@app.route("/result", methods=['POST'])
def result():
    lsi = LsiModel.load("../Model/lsi.model")
    dictionary = corpora.Dictionary.load("../Model/dictionary")
    
    question = request.form['question']
    answer = request.form['answer']

    question_split = string_split.split_contribution(question.lower())
    answer_split = string_split.split_contribution(answer.lower())
    question_bow = dictionary.doc2bow(question_split)
    answer_bow = dictionary.doc2bow(answer_split)
    question_lsi = lsi[question_bow]
    answer_lsi = lsi[answer_bow]

    c = matutils.sparse2full(question_lsi, 400)
    d = matutils.sparse2full(answer_lsi, 400)

    try:
        sim = np.dot(c, d) / (np.linalg.norm(c) * np.linalg.norm(d))
    except:
        sim = 0
        
    relevance = f"{round(sim, 4):.2%}"
    
    return render_template('result.html', question=question, answer=answer, relevance=relevance)
    
if __name__ == "__main__":
    app.run()