from flask import Flask, render_template, request, redirect

from check import checkRoll
from marks import getMarks

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/marks')
def marks():
    roll = request.args.get('roll')
    if not checkRoll(roll):
        return redirect('error')

    marksSheet = getMarks(roll)

    return render_template('marks.html', marksSheet=marksSheet)


@app.route('/error')
def error():
    return render_template('error.html'), 400


if __name__ == '__main__':
    app.run(debug=True)
