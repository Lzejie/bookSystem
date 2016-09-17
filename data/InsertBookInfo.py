# coding=utf8
import os, sys
import csv
import MySQLdb
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookSystem.settings')
import logging
logging.basicConfig(
    level=logging.ERROR,
    filename='insertInfo.log',
    filemode='a',
    format='%(asctime)s[line:%(lineno)d] %(levelname)s %(message)s',
)

import django
import codecs
django.setup()

from book.models import Book, User, Lend

MYSQL = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '644839',
    'db': 'BookSystem',
}


# 返回csv信息
def getCsv(filePath):
    # print os.path.isfile(filePath)
    try:
        with open(filePath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            for line in reader:
                yield line
    except Exception, e:
        print e
        sys.exit(1)

# 插入图书信息
def insertBookInfo(filePath='newBooks.csv'):
    try:
        bookData = getCsv(filePath)
        # print bookData.next()
        bookList = []
        id = set()
        for item in bookData:
            try:
                if item[0] == '002542730x' or item[0] == '014062080x':
                    print item
                    continue
                if item[0] in id:
                    print item[0]
                    print 'it had been add'
                    continue
                else:
                    book = Book(id=item[0], title=item[1], author=item[2],
                                publicYear=item[3], publisher=item[4], pic_s=item[5],
                                pic_m=item[6], pic_b=item[7])
                    bookList.append(book)
                    id.add(item[0])
            except Exception, e:
                print item
                print 'len is %s' % len(item)
                print '-'*100
                print e
                raw_input()
        print 'now save to mysql~'
        Book.objects.bulk_create(bookList)
    except Exception, e:
        print e
        logging.error(e)


# 插入用户信息
def insertUserInfo(filePath='BX-Users.csv'):
    pass


# 插入借阅关系
def insertLendInfo(filePath='BX-Book-Ratings.csv'):
    pass


# 修复错误数据
def resver(filePath):
    data = getCsv(filePath)
    data.next()
    with open('newBooks.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=';')
        for item in data:
            if len(item) < 8:
                if r';' in item[1]:
                    item[1] = item[1].replace('"', '')
                    tmp = item.pop(1)
                    tmp = tmp.split(r';')
                    tmp.reverse()
                    for i in tmp:
                        item.insert(1, i)
            while len(item) > 8:
                item[1] = item[1]+item[2]
                item.pop(2)
            if len(item) == 8:
                writer.writerow(item)
            else :
                print '-'*100
                print item
                raw_input()


def run():
    # resver('BX-Books.csv')
    insertBookInfo()
    # insertUserInfo()
    # insertLendInfo()


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

    comm = 'rm ../book/migrations/*_initial.py'
    os.system(comm)
    comm = 'python ../manage.py makemigrations'
    os.system(comm)
    comm = 'python ../manage.py migrate'
    os.system(comm)

    run()
