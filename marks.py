import sqlite3


def getName(con, rollno):
    cur = con.cursor()
    SQL = f'SELECT name FROM students WHERE rollno="{rollno}"'

    cur.execute(SQL)
    return cur.fetchone()[0]


def getSubjectName(con, subjectCode):
    cur = con.cursor()
    SQL = f'SELECT subject_name FROM subjects WHERE subject_code="{subjectCode}"'

    cur.execute(SQL)
    return cur.fetchone()[0]


def getMarks(con, rollno):
    cur = con.cursor()
    SQL = f'''SELECT
        subject_code,
        internal,
        external,
        pass_or_fail,
        credits,
        grade,
        grade_points,
        max_marks,
        max_credits,
        reg_or_sup FROM marks WHERE rollno="{rollno}"'''

    index = 1
    for row in cur.execute(SQL):
        res = [index]
        res.append(row[0])
        res.append(getSubjectName(con, row[0]))
        res.extend(row[1:])
        yield res
        index += 1
