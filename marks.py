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


def getCGPA(creditsList, grades):
    res = 0
    print(grades)
    for i in range(len(creditsList)):
        res += creditsList[i] * grades[i]

    return round(res/sum(creditsList), 2)


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
        reg_or_sup FROM marks WHERE rollno="{rollno}"'''

    index = 1
    totalMarks = 0
    totalCredits = 0

    output = []
    creditsList = []
    gradePoints = []
    for row in cur.execute(SQL):
        res = [
            index,
            row[0],
            getSubjectName(con, row[0]),
            *row[1:3],
            row[1] + row[2],
            *row[3:],
        ]
        creditsList.append(row[4])
        gradePoints.append(row[6])
        output.append(res)
        totalMarks += row[1] + row[2]
        totalCredits += row[4]
        index += 1

    maxMarksSQL = f'SELECT max_marks FROM marks WHERE rollno="{rollno}"'
    maxMarks = cur.execute(maxMarksSQL).fetchone()[0]

    res = {
        'maxMarks': maxMarks,
        'totalMarks': totalMarks,
        'totalCredits': totalCredits,
        'cgpa': getCGPA(creditsList, gradePoints)
    }
    output.append(res)

    return output
