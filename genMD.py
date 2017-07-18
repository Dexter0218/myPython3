#! usr/bin/python #coding=utf-8 //
import os
import pymysql
import time

Vol=1712
Type ="摄像"
Url ="http://image.wufazhuce.com/FskUP2AkXfUGIiW3jJOZSMeTQ2vs"
content = "你所以为的巧合，不过是另一个人用心的结果。"
PageTime ='2017-02-18'

head ="\
---\n\
layout: post\n\
title: One_Vol.%d\n\
category: One\n\
keywords: One,%d\n\
---\n\
"
def gotoDir(dir):

    if os.path.exists(dir):#Checks if the dir exists
        print("The directory: %s exists"%dir)
    else:
        print("No directory found for "+dir) #Output if no directory
        print
        os.makedirs(dir)#Creates a new dir for the given name
        print("Directory created for "+dir)
    os.chdir(dir)

def write2File(Vol,Url,Type,content,PageTime):
    # start = time.strftime("%Y-%m-%d", time.localtime())
    tempFile = open('%s-Vol_%d.md' %(PageTime,Vol),'w',encoding='utf8')
    tempFile.write(head %(Vol,PageTime.year))
    tempFile.write("# One 一个 #\n")

    tempFile.write("### %s ###\n" %PageTime)

    tempFile.write("![%s](%s)\n" %(Type,Url))

    tempFile.write("> %s \n" %content)

    tempFile.close()

gotoDir(r'F:\test\one')

# 打开数据库连接
db = pymysql.connect("localhost", "dexter0218", "1234", "abccs")
db.set_charset('utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
cursor.execute("USE abccs")

sql = """SELECT Vol,ImgURL,ImageType,Content,PageTime FROM abccs.page order by Vol desc;"""
cursor.execute(sql)
results = cursor.fetchall()
for result in results:
    Vol=result[0]
    Url=result[1]
    Type=result[2]
    content=result[3]
    PageTime = result[4]
    write2File(Vol,Url,Type,content,PageTime)
cursor.close()