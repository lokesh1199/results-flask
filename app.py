from flask import Flask, render_template, request, redirect

from check import checkRoll
from marks import getMarks, getName
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/marks')
def marks():
    rollno = request.args.get('roll')
    rollno = rollno.upper()
    if not checkRoll(rollno):
        return redirect('error')

    con = sqlite3.connect('marks.db')

    try:
        marks = getMarks(con, rollno)
        name = getName(con, rollno)
        return render_template('marks.html', marks=marks, name=name, rollno=rollno)
    except:
        return redirect('error')


@app.route('/error')
def error():
    return render_template('error.html'), 400


if __name__ == '__main__':
    app.run(debug=True)
