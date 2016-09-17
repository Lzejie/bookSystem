# coding:utf8
import csv
import MySQLdb

MYSQL = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '644839',
}

FIRST_NAME = [u'赵', u'钱', u'孙', u'李', u'张',
              u'林', u'陈', u'郑', u'周', u'施',
              u'徐', u'王', u'康', u'杨', u'曾']

SECOND_NAME = u'abcdefghijklmnopqrstuvwxyz'


# 返回csv信息
def getCsv(filePath):
    with open(filePath, 'rb') as f:
        reader = csv.reader(f)
        return reader

# 保存借用情况
def saveLend(filePath):
    pass


# 保存用户数据
def saveUserData(filePath):
    pass


# 保存书本数据
def saveBookData(filePath):
    try:
        with MySQLdb.connect(**MYSQL) as db:
            cursor = db.cursor()
            csvFile = getCsv(filePath)
            print csvFile.next()
            for line in csvFile:
                sql = 'INSERT INTO mysql () VALUES (值1, 值2,....)'
                cursor.execute()
            cursor.close()
    except Exception, e:
        print e
        

# 运行整个脚本
def run():
    saveBookData(./)


if __name__=='__main__':
    run()

