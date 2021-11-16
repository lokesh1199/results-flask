import sqlite3


def createStudentsTable(con):
    cur = con.cursor()
    createSQL = '''CREATE TABLE students (
        rollno text,
        name text
    )'''

    cur.execute(createSQL)
    con.commit()


def parseCSV(filename):
    with open(filename) as file:
        for line in file.readlines()[1:]:
            yield list(map(str.strip, line.split(',')))


def insertStudentsValues(con, filename):
    cur = con.cursor()
    insertSQL = 'INSERT INTO students values("{}", "{}")'

    for row in parseCSV(filename):
        cur.execute(insertSQL.format(*row))

    con.commit()


def createSubjectsTable(con):
    cur = con.cursor()

    createSQL = '''CREATE TABLE subjects (
        subject_code text,
        subject_name text
    )'''

    cur.execute(createSQL)
    con.commit()


def insertSubjectsValues(con, filename):
    cur = con.cursor()
    insertSQL = 'INSERT INTO subjects values("{}", "{}")'

    for row in parseCSV(filename):
        cur.execute(insertSQL.format(*row))

    con.commit()


def createMarksTable(con):
    cur = con.cursor()
    createSQL = '''CREATE TABLE marks (
        subject_code text,
        internal integer,
        external integer,
        pass_or_fail text,
        credits integer,
        grade text,
        grade_points integer,
        rollno text,
        max_marks integer,
        max_credits integer,
        reg_or_sup text
    )'''

    cur.execute(createSQL)
    con.commit()


def insertMarksValues(con, filename):
    cur = con.cursor()
    insertSQL = '''INSERT INTO marks VALUES (
        "{}", "{}", "{}", "{}", "{}", "{}",
        "{}", "{}", "{}", "{}", "{}"
    )'''

    for row in parseCSV(filename):
        cur.execute(insertSQL.format(*row))

    con.commit()


def main():
    con = sqlite3.connect('marks.db')
    cur = con.cursor()

    createStudentsTable(con)
    insertStudentsValues(con, 'static/marks/student18-3.csv')

    createSubjectsTable(con)
    insertSubjectsValues(con, 'static/marks/subject1.csv')

    createMarksTable(con)
    insertMarksValues(con, 'static/marks/marks1.csv')


if __name__ == '__main__':
    main()
