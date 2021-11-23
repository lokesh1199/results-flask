from math import ceil


def getName(con, rollno, tableName):
    cur = con.cursor()
    SQL = f'SELECT name FROM students WHERE rollno="{rollno}"'

    cur.execute(SQL)
    return cur.fetchone()[0]


def getSubjectName(con, subjectCode):
    cur = con.cursor()
    SQL = f'''SELECT subject_name FROM subjects WHERE
            subject_code="{subjectCode}"'''

    cur.execute(SQL)
    return cur.fetchone()[0]


def getSGPA(creditsList, grades):
    res = 0
    for i in range(len(creditsList)):
        res += creditsList[i] * grades[i]
    try:
        return round(res/sum(creditsList), 2)
    except:
        return 0


def getMarks(con, rollno, tableName):
    cur = con.cursor()
    SQL = f'''SELECT
        subject_code,
        internal,
        external,
        total,
        result_status,
        credits,
        grades,
        grade_points from {tableName} WHERE rollno = "{rollno}"'''

    index = 1
    totalMarks = 0
    totalCredits = 0

    output = []
    creditsList = []
    gradePoints = []
    for row in cur.execute(SQL):
        row = list(row)
        row.insert(1, getSubjectName(con, row[0]))
        creditsList.append(row[6])
        gradePoints.append(row[8])

        totalMarks += row[4]
        totalCredits += row[6]

        row.insert(0, index)
        output.append(row)
        index += 1

    res = {
        'maxMarks': (index - 1) * 100,
        'totalMarks': totalMarks,
        'totalCredits': totalCredits,
        'sgpa': getSGPA(creditsList, gradePoints)
    }
    output.append(res)

    if len(output) == 1:
        raise Exception('No result found')

    return output


def parseTableName(name):
    name = name.split('_')[1:]
    res = f'{name[0].upper()} Year {name[1].upper()} Semester '
    res += f'({name[2].title()}) {name[3].title()} Examinations, '
    res += f'{name[4].title()} {name[5]}'
    return res


def getResultsListCount(con):
    sql = 'SELECT COUNT(*) FROM metadata'

    cur = con.cursor()
    cur.execute(sql)
    return cur.fetchone()[0]


def getResultsPageNavList(con, perPage, page):
    pages = ceil(getResultsListCount(con) / perPage)

    res = [1]

    if page > 1:
        res.append(None)
        res.append(page)

    if page + 1 < pages:
        res.append(page+1)

    if res[-1] != pages:
        res.append(None)
        res.append(pages)

    return res if len(res) != 1 else []


def getResultsList(con, page, perPage):
    cur = con.cursor()

    count = getResultsListCount(con)
    pages = count // perPage  # this is the number of pages
    offset = (page-1)*perPage  # offset for SQL query

    sql = f'''SELECT * FROM metadata ORDER BY sno DESC LIMIT {perPage}
             OFFSET {offset}'''

    res = []
    for row in cur.execute(sql):
        res.append([*row[:2], parseTableName(row[2])])
    return res


def getTableName(sno, con):
    sql = f'SELECT name FROM metadata WHERE sno={sno}'
    cur = con.cursor()
    cur.execute(sql)
    return cur.fetchone()[0]


def getBranchName(con, roll):
    branchCode = roll[6:8]
    sql = f'SELECT branch_name FROM branches WHERE branch_code="{branchCode}"'
    cur = con.cursor()
    cur.execute(sql)
    return cur.fetchone()[0]
