import sqlite3
from datetime import datetime

from .create import createResultsTable
from .heplers import (getNextIndexOfData, parseCSV, parseTableName,
                      stripEmptyCells)


def insertResultsValues(data, tableName, con):
    insertSQL = f'''INSERT INTO {tableName} values {tuple(data)}'''

    cur = con.execute(insertSQL)
    con.commit()


def insertStudentValues(rollno, name, con):
    insertSQL = f'INSERT INTO students values ("{rollno}", "{name}")'

    cur = con.cursor()
    try:
        cur.execute(insertSQL)
        con.commit()
    except:
        # Already exists
        pass


def insertSubjectValues(subjectCode, subjectName, con):
    insertSQL = f'''INSERT INTO subjects VALUES (
        "{subjectCode}", "{subjectName}")'''

    cur = con.cursor()
    try:
        cur.execute(insertSQL)
        con.commit()
    except:
        # Already exists
        pass


def insertMetadataValues(tableName, con):
    cur = con.cursor()
    countSQL = 'SELECT sno FROM metadata ORDER BY sno DESC LIMIT 1'
    cur.execute(countSQL)
    count = cur.fetchone()
    count = count[0] + 1 if count else 1

    date = datetime.now().strftime(r'%d-%m-%Y')
    insertSQL = f'''INSERT INTO metadata VALUES (
        "{count}", "{date}", "{tableName}")'''
    cur = con.cursor()
    cur.execute(insertSQL)
    con.commit()


def insertResultsData(data: list, tableName, con):
    subjects = set()

    index = getNextIndexOfData(data)
    while index < len(data):
        row = stripEmptyCells(data[index])
        name, rollno = row[1], row[3]

        insertStudentValues(rollno, name, con)

        j = index + 2
        while data[j][0] != 'SGPA':
            subjects.add((data[j][0], data[j][1]))
            row = data[j][:9]
            row = [rollno] + row[:1] + row[2:]
            insertResultsValues(row, tableName, con)
            j += 1

        index = getNextIndexOfData(data, j)

    if len(subjects):
        addSubjects(subjects, con)


def insertNewCSV(course, year, sem, regulation, regOrSup, examMonth, examYear,
                 fileName):
    tableName = f't_{course}_{year}_{sem}_{regulation}_{regOrSup}_{examMonth}_{examYear}'

    con = sqlite3.connect('results.db')
    createResultsTable(tableName, con)
    insertResultsData(parseCSV(fileName), tableName, con)
    insertMetadataValues(tableName, con)

    return parseTableName(tableName)


def addSubjects(data, con):
    for subjectCode, subjectName in data:
        insertSubjectValues(subjectCode, subjectName, con)
