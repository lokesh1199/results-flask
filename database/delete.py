from .query import getTableName
from .heplers import parseTableName


def deleteResultsTable(con, tableSno):
    tableName = getTableName(tableSno, con)
    dropSQL = f'DROP TABLE {tableName}'
    deleteSQL = f'DELETE FROM metadata WHERE sno={tableSno}'

    cur = con.cursor()
    cur.execute(dropSQL)
    cur.execute(deleteSQL)
    con.commit()

    return parseTableName(tableName)
