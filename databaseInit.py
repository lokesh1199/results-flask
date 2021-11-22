import sqlite3
from datetime import datetime


def parseCSV(filename):
    with open(filename) as file:
        res = []
        for line in file:
            res.append(list(map(str.strip, line.split(','))))
        return res


def stripEmptyCells(row: list):
    return [i for i in row if i]


def createResultsTable(tableName, con):
    cur = con.cursor()
    createSQL = f'''CREATE TABLE {tableName} (
        rollno text,
        subject_code text,
        internal integer,
        external integer,
        total integer,
        result_status text,
        credits integer,
        grades text,
        grade_points integer
    )'''
    cur.execute(createSQL)
    con.commit()


def insertResultsValues(data, tableName, con):
    insertSQL = f'''INSERT INTO {tableName} values {tuple(data)}'''

    cur = con.execute(insertSQL)
    con.commit()


def createStudentTable(con):
    createSQL = '''CREATE TABLE students (
        rollno text PRIMARY KEY,
        name text
    )'''

    cur = con.cursor()
    cur.execute(createSQL)
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


def createSubjectTable(con):
    createSQL = '''CREATE TABLE subjects (
        subject_code text PRIMARY KEY,
        subject_name text
    )'''

    cur = con.cursor()
    cur.execute(createSQL)
    con.commit()


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


def addSubjects(data, con):
    for subjectCode, subjectName in data:
        insertSubjectValues(subjectCode, subjectName, con)


def createMetadataTable(con):
    createSQL = '''CREATE TABLE metadata(
        sno integer PRIMARY KEY,
        date text,
        name text
    )'''
    cur = con.cursor()
    cur.execute(createSQL)
    con.commit()


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

    index = 8
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

        index = j+2

    if len(subjects):
        addSubjects(subjects, con)
        insertMetadataValues(tableName, con)


def createBranchesTable(con):
    createSQL = '''CREATE TABLE branches (
        branch_code text PRIMARY KEY,
        branch_name text
    )'''

    cur = con.cursor()
    cur.execute(createSQL)
    con.commit()


def insertBranchValues(con):
    branches = {
        '01': 'Civil Engineering',
        '02': 'Electrical and Electronics Engineering',
        '03': 'Mechanical Engineering',
        '04': 'Electronics and Communication Engineering',
        '05': 'Computer Science and Engineering',
        '12': 'Information Technology',
        '33': 'Artificial Intelligence & Machine learning'
    }

    insertSQL = 'INSERT INTO branches VALUES ("{}", "{}")'
    cur = con.cursor()

    for branchCode in branches:
        cur.execute(insertSQL.format(branchCode, branches[branchCode]))

    con.commit()


def createAllTables():
    con = sqlite3.connect('results.db')

    createStudentTable(con)
    createSubjectTable(con)
    createMetadataTable(con)
    createBranchesTable(con)
    insertBranchValues(con)


def insertNewCSV(year, sem, regulation, regOrSup, examMonth, examYear,
                 fileName):
    tableName = f't_{year}_{sem}_{regulation}_{regOrSup}_{examMonth}_{examYear}'

    con = sqlite3.connect('results.db')
    createResultsTable(tableName, con)
    insertResultsData(parseCSV(fileName), tableName, con)


if __name__ == '__main__':
    createAllTables()
