from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bett5G0ddard'
app.config['MYSQL_DB'] = 'pmqs'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT AVG(ANSWER_RELEVANCE) FROM QA_PAIRS WHERE DATE = (SELECT DATE FROM QA_PAIRS ORDER BY DATE DESC LIMIT 1)")
    result = cur.fetchone()
    cur.close()
    return str(result[0])

if __name__ == '__main__':
    app.run()