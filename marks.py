from openpyxl import load_workbook


def getMarks(roll):
    a = load_workbook('static/data/marks.xlsx').active
    return a
