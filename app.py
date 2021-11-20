import sqlite3

from flask import Flask, redirect, render_template, request, send_from_directory, session

from check import checkRoll
from marks import getMarks, getName, parseTableName, getResultsList, getTableName

app = Flask(__name__)
# TODO Change this in production
app.secret_key = '6d5843bbf5bdc0f249376717e6d32919715b4bd02b89'


@app.route('/')
@app.route('/home')
def home():
    con = sqlite3.connect('results.db')
    resultsList = getResultsList(con)
    return render_template('home.html', resultsList=resultsList)


@app.route('/roll/<table>')
def roll(table):
    return render_template('roll.html', table=table)


@app.route('/results')
def results():
    rollno = request.args.get('roll').strip().upper()
    table = request.args.get('table').strip()
    if not checkRoll(rollno):
        return redirect('/error')

    con = sqlite3.connect('results.db')

    try:
        tableName = getTableName(table, con)
        examName = parseTableName(tableName)
        marks = getMarks(con, rollno, tableName)
        name = getName(con, rollno, tableName)

        return render_template('results.html', marks=marks, name=name, rollno=rollno, examName=examName)
    except Exception as e:
        return redirect('/error')


@app.route('/error')
def error():
    return render_template('error.html'), 400


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect('/admin')
        return render_template('admin_login.html', incorrect=True)
    else:
        if session.get('admin'):
            examMonths = (
                'January',
                'Febraury',
                'March',
                'April',
                'May',
                'June',
                'July',
                'August',
                'September',
                'October',
                'November',
                'December'
            )
            examYears = [year for year in range(2020, 2030)]
            years = ['I', 'II', 'III', 'IV']
            sems = ['I', 'II']

            return render_template('admin_panel.html', examMonths=examMonths, examYears=examYears, years=years, sems=sems)

        return render_template('admin_login.html', incorrect=False)


@app.route('/logout')
def logout():
    if session.get('admin'):
        session.pop('admin', None)
        return redirect('/admin')
    else:
        return redirect('/')


@app.route('/upload')
def upload():
    return redirect('/error')


# TODO Remove this in production
@app.route('/static/<file>')
def staticFiles(file):
    return send_from_directory(file, 'static')


if __name__ == '__main__':
    app.run(debug=True)
