#  -*-  codeing  =  utf-8  -*-
#  @Time  :2022/1/19  16:47
#  @Author:旁观者
#  @File  :  connect_db.py
#  @Software:  PyCharm
import sqlite3
import os
dbUrl = "F:\workspace\PyCharm_workspace\zongheng\db\zongheng.db"

class DBOperate:
    def __init__(self,dbPath = os.path.join(os.getcwd(),"zongheng.db")):
        self.dbPath = dbPath
        self.connect=sqlite3.connect(self.dbPath)

    def Query(self, sql: str) -> list:
        """传统查询语句"""
        print(f"query sql is\n{sql}")
        queryResult = self.connect.cursor().execute(sql).fetchall()
        return queryResult if queryResult else []

    def QueryAsDict(self, sql: str) -> dict:
        """调用该函数返回结果为字典形式"""
        self.connect.row_factory = self.dictFactory
        cur = self.connect.cursor()
        queryResult = cur.execute(sql).fetchall()
        return queryResult if queryResult else {}

    def Insert(self, sql: str):
        print(f"执行的sql语句为\n{sql}")
        self.connect.cursor().execute(sql)
        self.connect.commit()

    def InsertWithParams(self,sql:str,paraList:list):
        self.connect.cursor().execute(sql,paraList)
        self.connect.commit()
        return self.connect.total_changes

    def Update(self, sql: str):
        self.connect.cursor().execute(sql)
        self.connect.commit()

    def Delete(self, sql: str):
        self.connect.cursor().execute(sql)
        self.connect.commit()

    def CloseDB(self):
        self.connect.cursor().close()
        self.connect.close()

    def dictFactory(self, cursor, row):
        """将sql查询结果整理成字典形式"""
        d = {}
        for index, col in enumerate(cursor.description):
            d[col[0]] = row[index]
        return d

# 执行select语句,不会commit
def select(sql, para={}):
    connector = sqlite3.connect(dbUrl)
    cursor = connector.cursor()
    if len(para) > 0:
        resultMap = cursor.execute(sql, para)
    else:
        resultMap = cursor.execute(sql)
    result = resultMap.fetchall()
    cursor.close()
    connector.close()
    return result


#执行需要commit的sql命令
def executeUpdate(sql, para):
    connector = sqlite3.connect(dbUrl)
    cursor = connector.cursor()
    try:
        cursor.execute(sql, para)
        connector.commit()
        r = connector.total_changes
    finally:
        cursor.close()
        connector.close()

    return r


def executeUpdateList(sql, paraList):
    connector = sqlite3.connect(dbUrl)
    cursor = connector.cursor()
    try:
        for para in paraList:
            cursor.execute(sql, para)
        connector.commit()
        i = connector.total_changes
    except UnboundLocalError as e:
        connector.rollback()
        print(e.with_traceback())
    finally:
        cursor.close()
        connector.close()
    return i


def createZongHengTable():
    sql = '''
        create table zongheng(
        id integer PRIMARY KEY autoincrement not null,
        url varchar(255) not null,
        img_src varchar(255) not null,
        name VARCHAR(255) not null,
        author varchar(255),
        type varchar(255) not null,
        status varchar(255) not null,
        time varchar(255) not null,
        itroduce text
        );
    '''
    db = DBOperate()
    db.Query(sql)
    db.CloseDB()


def insertToZongheng(dataList):
    sql = "insert into zongheng values(null,:url,:img_src,:name,:author,:type,:status,:time,:itroduce);"
    paraList = []
    for data in dataList:
        paraList.append({"url": data[0], "img_src": data[1], "name": data[2], "author": data[3], "type": data[4],
                         "status":data[5],"time": data[6], "itroduce": data[7]})
    db = DBOperate()
    result = db.InsertWithParams(sql, paraList)
    db.CloseDB()
    return result



def selectFromZonghengByPage(begin=0,count=50):
    sql = f"select * from zongheng order by id limit {count} offset {begin*count};"
    print(sql)
    db = DBOperate()
    result = db.QueryAsDict(sql)
    db.CloseDB()
    return result


def getCount():
    sql = "select count(id) from zongheng ;"
    db = DBOperate()
    result = db.Query(sql)
    db.CloseDB()
    return result


def getOnlyCount(columnName='type'):
    sql = "select count(distinct "+columnName+") from zongheng;"
    db = DBOperate()
    result = db.Query(sql)
    db.CloseDB()
    return result[0]


def getAllBooks(columnName='*'):
    sql = f"select {columnName} from zongheng;"
    db = DBOperate()
    result = db.Query(sql)
    db.CloseDB()
    return result

def getDataByColumn(columnName='type'):
    sql = f"select distinct {columnName} from zongheng"
    db = DBOperate()
    result = db.Query(sql)
    db.CloseDB()
    return result

def getCountByType(type="科幻游戏"):
    sql = f"select count(type) from zongheng where type = '{type}';"
    db = DBOperate()
    result = db.Query(sql)
    db.CloseDB()
    return result

def main():
    # print(getDataByColumn())
    createZongHengTable()


if __name__=="__main__":
    main()
