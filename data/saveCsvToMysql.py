# coding:utf8
import MySQLdb
import os
import csv
import time
import logging
import sys

logging.basicConfig(
    filename='saveCsvToMysql.log',
    filemode='w',
    level=logging.ERROR,
    format='%(asctime)s[line:%(lineno)d] %(levelname)s %(message)s',
)

MYSQL = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '644839',
    'db': 'BookSystem',
}

failedInLend = []
failedInLendCount = 0
failedInUser = []
failedInUserCount = 0
failedInBook = []
failedInBookCount = 0
sqlList = []

# 返回csv信息
def getCsv(filePath):
    print os.path.isfile(filePath)
    with open(filePath, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        for line in reader:
            yield line

# 保存借用情况
def saveLend(filePath):
    try:
        with MySQLdb.connect(**MYSQL) as cursor:
            csvFile = getCsv(filePath)
            print csvFile.next()
            for line in csvFile:
                try:
                    bookid = line[1]
                    userid = line[0]
                    value = [userid, bookid, 0, str(time.strftime("%Y-%m-%d %H:%I:%S ", time.localtime(time.time()))), \
                             str(time.strftime("%Y-%m-%d %H:%I:%S ", time.localtime(time.time())))]
                    value = ['"%s"' % str(item).replace('"', '\'') for item in value]
                    sql = 'INSERT INTO book_lend (user_id, book_id, renew, createdAt, returnAt) ' \
                          'VALUES (%s,%s,%s,%s,%s)' % tuple(value)
                    print sql
                    cursor.execute(sql)
                except Exception, e:
                    logging.error(e)
            cursor.close()
    except Exception, e:
        logging.error(e)

# 保存用户数据
def saveUserData(filePath):
    try:
        with MySQLdb.connect(**MYSQL) as cursor:
            csvFile = getCsv(filePath)
            print csvFile.next()
            i = 0
            for line in csvFile:
                try:
                    value = line + ['111111', 0, str(time.strftime("%Y-%m-%d %H:%I:%S ", time.localtime(time.time())))]
                    value = ['"%s"' % str(item).replace('"', '\'') for item in value]
                    if 'NULL' in line:
                        value[2] = 'null'
                    sql = 'INSERT INTO book_user (id, username, age, password, status, createdAt) ' \
                          'VALUES (%s,%s,%s,%s,%s,%s)' % tuple(value)
                    print sql
                    cursor.execute(sql)
                except Exception, e:
                    logging.error(e)
            cursor.close()
    except Exception, e:
        logging.error(e)

# 保存书本数据
def saveBookData(filePath):
    try:
        with MySQLdb.connect(**MYSQL) as cursor:
            csvFile = getCsv(filePath)
            print csvFile.next()
            for line in csvFile:
                try:
                    value = line + ['50', '3', 'Havn\'t information', str(time.strftime("%Y-%m-%d %H:%I:%S ", time.localtime(time.time())))]
                    value = ['"%s"'%item.replace('"','\'') for item in value]
                    sql = 'INSERT INTO book_book (id,title,author,publicYear,publisher,pic_s,pic_m,pic_b,price,count,pos,createdAt) ' \
                          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'%tuple(value)
                    print sql
                    cursor.execute(sql)
                except Exception, e:
                    logging.error(e)
            cursor.close()
    except Exception, e:
        print e
        logging.error(e)

# 运行整个脚本
def run():
    saveBookData(r'BX-Books.csv')
    # saveUserData(r'BX-Users.csv')
    # saveLend(r'BX-Book-Ratings.csv')

if __name__=='__main__':
    start = ''
    while start != 'y' and start != 'n' and start != 'Y' and start != 'N':
        start = raw_input('是否对数据库进行初始化(Y/N):>')

    if 'N' in start or 'n' in start:
        print u'取消数据库初始化'
        sys.exit(0)

    try:
        with MySQLdb.connect(**MYSQL) as db :
            comm = 'drop database BookSystem;'
            db.execute(comm)
            print u'成功删除数据库BookSystem'
    except Exception,e:
        pass

    with MySQLdb.connect(host=MYSQL['host'], user=MYSQL['user'], passwd=MYSQL['passwd']) as conn:
        conn.execute('create database BookSystem character set utf8 collate utf8_general_ci;')

    comm = 'rm ./book/migrations/*_initial.py'
    os.system(comm)
    comm = 'python manage.py makemigrations'
    os.system(comm)
    comm = 'python manage.py migrate'
    os.system(comm)

    run()
    print u'%s条图书数据插入失败' % len(failedInBook)
    print u'%s条用户数据插入失败' % len(failedInUser)
    # 借阅数据原本就存在一些缺失
    print u'%s条借阅数据插入失败' % len(failedInLend)

    # for item in range(len(failedInLend)):
    #     print failedInLend.pop()
    #     print sqlList.pop()
    #     print '='*50

