import sqlite3
from os import remove

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, session, url_for, flash)

from check import checkFile, checkRoll
from databaseInit import insertNewCSV
from marks import (getMarks, getName, getResultsList, getTableName,
                   parseTableName, getBranchName)

app = Flask(__name__)
# TODO Change this in production
app.config['SECRET_KEY'] = '6d5843bbf5bdc0f249376717e6d32919715b4bd02b89'


@app.route('/')
@app.route('/home')
def home():
    con = sqlite3.connect('results.db')
    resultsList = getResultsList(con)
    return render_template('home.html', resultsList=resultsList)


@app.route('/roll/<table>')
def roll(table):
    bgImage = '/static/images/caps.jpg'
    return render_template('roll.html', table=table, bgImage=bgImage)


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
        branch = getBranchName(con, rollno)

        return render_template('results.html', marks=marks, name=name,
                               rollno=rollno, examName=examName, branch=branch)
    except Exception as e:
        raise e
        return redirect('/error')


@app.route('/error')
def error():
    return render_template('error.html'), 400


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    bgImage = '/static/images/panel.jpg'

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(request.url)

        return render_template('admin_login.html', incorrect=True,
                               bgImage=bgImage)
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
            regulations = [f'R{i}' for i in range(10, 21)]

            error = request.args.get('error')
            success = request.args.get('success')

            return render_template('admin_panel.html', examMonths=examMonths,
                                   examYears=examYears, years=years, sems=sems,
                                   regulations=regulations, bgImage=bgImage)

        return render_template('admin_login.html', incorrect=False,
                               bgImage=bgImage)


@app.route('/logout')
def logout():
    if session.get('admin'):
        session.pop('admin', None)
        return redirect('/admin')
    else:
        return redirect('/')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return redirect('/admin')
    elif not session.get('admin'):
        return redirect('/')
    else:
        examMonth = request.form.get('examMonth')
        examYear = request.form.get('examYear')
        year = request.form.get('year')
        sem = request.form.get('sem')
        regulation = request.form.get('regulation')
        regOrSup = request.form.get('regOrSup')

        file = request.files['results']

        if not checkFile(file.filename):
            flash('Invalid File', 'is-danger')
        else:
            fileName = 'results.csv'
            file.save(fileName)

            try:
                insertNewCSV(year, sem, regulation, regOrSup,
                             examMonth, examYear, fileName)
            except:
                flash('Results File Already Exists', 'is-danger')
                return redirect('/admin')
            finally:
                remove(fileName)

            flash('File Uploaded Successfully', 'is-success')

        return redirect('/admin')


# TODO Remove this in production
@app.route('/static/<file>')
def staticFiles(file):
    return send_from_directory(file, 'static')


if __name__ == '__main__':
    app.run(debug=True)
