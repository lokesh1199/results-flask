def parseCSV(filename):
    with open(filename) as file:
        res = []
        for line in file:
            res.append(list(map(str.strip, line.split(','))))
        return res


def stripEmptyCells(row: list):
    return [i for i in row if i]


def getBranchName(roll):

    branches = {
        '01': 'Civil Engineering',
        '02': 'Electrical and Electronics Engineering',
        '03': 'Mechanical Engineering',
        '04': 'Electronics and Communication Engineering',
        '05': 'Computer Science and Engineering',
        '12': 'Information Technology',
        '33': 'Artificial Intelligence & Machine Learning',
        '06': 'Data Science',
        '07': 'Cyber Security',
    }

    branchCode = roll[6:8]
    return branches[branchCode]


def parseTableName(name):
    name = name.split('_')[1:]
    res = f'{name[0].upper()} Year {name[1].upper()} Semester '
    res += f'({name[2].title()}) {name[3].title()} Examinations, '
    res += f'{name[4].title()} {name[5]}'
    return res
