#  -*-  codeing  =  utf-8  -*-
#  @Time  :2022/3/10  23:15
#  @Author:旁观者
#  @File  :  db_mysql.py
#  @Software:  PyCharm
import pymysql


class MySqlOption:
    def __init__(self):
        self.connect = pymysql.connect(host='localhost', user='root',
                                       password='xx1602614lpc', database='spider')

    def Query(self, sql: str) -> list:
        """传统查询语句"""
        # print(f"query sql is\n{sql}")
        cur = self.connect.cursor()
        cur.execute(sql)
        queryResult = cur.fetchall()
        return queryResult if queryResult else []

    def QueryAsDict(self, sql: str) -> dict:
        """调用该函数返回结果为字典形式"""
        cur = self.connect.cursor()
        cur.execute(sql)
        queryResult = self.dict_fetchall(cur)
        return queryResult if queryResult else {}

    def QueryWithCommit(self, sql: str):
        cur = self.connect.cursor()
        cur.execute(sql)
        self.connect.commit()
        queryResult = cur.fetchone()
        return queryResult

    def Insert(self, sql: str):
        print(f"执行的sql语句为\n{sql}")
        self.connect.cursor().execute(sql)
        self.connect.commit()

    def InsertWithParams(self, sql: str, paraList: list):
        # cur = self.connect.cursor(cursor=pymysql.connect.cursor().DictCursor)
        cur = self.connect.cursor()
        cur.executemany(sql, paraList)
        self.connect.commit()
        cur.fetchall()
        return cur.rowcount

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
        for index, col in cursor.description:
            d[col[0]] = row[index]
        return d

    def get_index_dict(self, cursor):
        index_dict = dict()
        index = 0
        for desc in cursor.description:
            index_dict[desc[0]] = index
            index = index + 1
        return index_dict

    def dict_fetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def createTableZongheng(db: MySqlOption):
    sql = '''
        create table IF NOT EXISTS `zongheng`(
            `id` int auto_increment not null PRIMARY KEY comment '序号',
            `url` varchar(255) not null,
            `img_src` varchar(255) not null,
            `name` varchar(255) not null,
            `author` varchar(255),
            `type` varchar(255) not null,
            `status` varchar(255) not null,
            `time` varchar(255) not null,
            `introduce` text
        );
    '''
    result = db.QueryWithCommit(sql)
    db.CloseDB()
    print(result)


def insertBooks(bookList: list):
    sql = '''
        insert ignore into `zongheng`(`url`,`img_src`,`name`,`author`,`type`,`status`,`time`,`introduce`,`latest_chapter`) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''
    db = MySqlOption()
    result = db.InsertWithParams(sql, bookList)
    db.CloseDB()
    return result


# 分页查询，page：页码(从 1 开始)，rows：行数
def selectPage(page: int, rows: int, column='*'):
    db = MySqlOption()
    sql = f"select distinct {column} from zongheng limit {page * rows - rows},{rows};"
    result = db.QueryAsDict(sql)
    db.CloseDB()
    return result


def selectCount(columnName="id"):
    sql = f"select count(distinct {columnName}) from zongheng;"
    db = MySqlOption()
    result = db.Query(sql)
    db.CloseDB()
    return result[0][0];


def select(column="*"):
    sql = f"select distinct {column} from zongheng;"
    db = MySqlOption()
    result = db.Query(sql)
    db.CloseDB()
    return result;


def selectAttributeCount(column, value):
    sql = f"select count({column}) from zongheng where {column} like '{value}'"
    db = MySqlOption()
    result = db.Query(sql)
    db.CloseDB()
    return result[0][0]


# 测试
def main():
    print(selectAttributeCount("type", "奇幻玄幻"))


if __name__ == "__main__":
    main()
