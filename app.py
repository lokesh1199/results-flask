import sqlite3

from flask import Flask, redirect, render_template, request, send_from_directory

from check import checkRoll
from marks import getMarks, getName, parseTableName, getResultsList, getTableName

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    con = sqlite3.connect('results.db')
    resultsList = getResultsList(con)
    return render_template('home.html', resultsList=resultsList)


@app.route('/roll/<table>')
def roll(table):
    return render_template('roll.html', tableSno=table)


@app.route('/results')
def results():
    rollno = request.args.get('roll').strip()
    tableSno = request.args.get('tableSno').strip()
    rollno = rollno.upper()
    if not checkRoll(rollno):
        return redirect('error')

    con = sqlite3.connect('results.db')

    try:
        tableName = getTableName(tableSno, con)
        examName = parseTableName(tableName)
        marks = getMarks(con, rollno, tableName)
        name = getName(con, rollno, tableName)

        return render_template('results.html', marks=marks, name=name, rollno=rollno, examName=examName)
    except Exception as e:
        return redirect('error')


@app.route('/error')
def error():
    return render_template('error.html'), 400


# TODO Remove this in production
@app.route('/static/<file>')
def staticFiles(file):
    return send_from_directory(file, 'static')


if __name__ == '__main__':
    app.run(debug=True)
