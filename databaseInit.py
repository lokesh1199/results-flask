import sqlite3
from datetime import datetime


def parseCSV(filename):
    with open(filename) as file:
        res = []
        for line in file:
            res.append(list(map(str.strip, line.split(','))))
        return res


def countSubjects(data: list):
    index = 10
    while index < len(data):
        if data[index][0] == 'SGPA':
            return index - 10
        index += 1
    return index - 10


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
    insertSQL = f'INSERT INTO subjects VALUES ("{subjectCode}", "{subjectName}")'

    cur = con.cursor()
    try:
        cur.execute(insertSQL)
        con.commit()
    except:
        # Already exists
        pass


def addSubjects(data: list, subjectCount, con):
    for i in range(10, 10 + countSubjects(data)):
        insertSubjectValues(*data[i][:2], con)


def createMetadataTable(con):
    createSQL = '''CREATE TABLE metadata (
        sno integer,
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
    insertSQL = f'INSERT INTO metadata VALUES ("{count}", "{date}", "{tableName}")'
    cur = con.cursor()
    cur.execute(insertSQL)
    con.commit()


def insertResultsData(data: list, tableName, con):
    count = 0
    subjectCount = countSubjects(data)

    insertMetadataValues(tableName, con)
    addSubjects(data, subjectCount, con)

    index = 8
    while index < len(data):
        row = stripEmptyCells(data[index])
        name, rollno = row[1], row[3]

        insertStudentValues(rollno, name, con)

        j = index + 2
        while j <= index + subjectCount + 1:
            row = data[j][:9]
            row = [rollno] + row[:1] + row[2:]
            insertResultsValues(row, tableName, con)
            j += 1

        index = j+2


def createAllTables():
    con = sqlite3.connect('results.db')

    createStudentTable(con)
    createSubjectTable(con)
    createMetadataTable(con)


# TODO Remove this in production
def main():
    con = sqlite3.connect('results.db')
    # createAllTables()

    tableName = 't_1_1_r20_regular_august_2020'
    createResultsTable(tableName, con)
    insertResultsData(parseCSV('marks/marks.csv'), tableName, con)

    # sql = f'SELECT * FROM {tableName} WHERE rollno="20BF1A3311"'
    # print(sql)
    # sql = 'SELECT tbl_name FROM sqlite_master'
    # sql = f'''SELECT * FROM metadata ORDER BY sno DESC LIMIT 10'''
    # cur = con.cursor()
    # for row in cur.execute(sql):
    # print(row)


if __name__ == '__main__':
    main()
