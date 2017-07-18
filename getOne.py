#!/usr/bin/python3

import os
from bs4 import BeautifulSoup
from Download import mRequest
import re
import pymysql
import time
from git import *

head ="\
---\n\
layout: post\n\
title: One_Vol.%d\n\
category: One\n\
keywords: One,%d\n\
---\n\
"

urls = "http://wufazhuce.com/"
desPath = r'F:\one'
workspace = r'F:\myGitHub\Dexter0218.github.io\_posts\one一个'



class page:
    def __init__(self):
        self.title = ''     # 名称
        self.currnetUrl = ''     # 链接


class ImageInfo:
    def __init__(self):
        self.type = ''     # 名称
        self.url = ''     # 链接
        self.content = ''  # 句子
        self.VOL = ''     # 期
        self.day = 0     # 天
        self.month =0
        self.year =0
        self.mDate =''
class getOne():

    def getFirstPage(self, url):
        mPage = page()  # 定义结构对象

        html = mRequest.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        result = soup.find('div', class_="fp-one-cita").find('a')
        mPage.url = result.get('href')
        mPage.title = result.get_text()

        print("starturl:  %s" % mPage.url)
        print("starttitle:%s" % mPage.title)
        return mPage

    def getPic(self, url):
        print("+++++++++++++++++++++++++++++++++++++++")
        imgInfo = ImageInfo()
        html = mRequest.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('div', class_="one-imagen") == None:
            return None
        result = soup.find('div', class_="one-imagen").find('img')
        imgInfo.url = result.get('src')
        print("imgURL:%s" % imgInfo.url)
        result = soup.find('div', class_="one-imagen-leyenda")
        imgInfo.type = result.get_text().strip()
        print("imgType:%s" % imgInfo.type)

        result = soup.find('div', class_="one-cita")
        imgInfo.content = result.get_text().strip()
        print("content:%s" % imgInfo.content)

        result = soup.find('div', class_="one-titulo")
        imgInfo.VOL = int(re.sub("\D", "", result.get_text().strip()))
        print("VOL:%d" % imgInfo.VOL)

        result = soup.find('p', class_="dom")
        imgInfo.day = int(result.get_text().strip())
        print("day:%d" % imgInfo.day)

        result = soup.find('p', class_="may")
        mTime = result.get_text().strip()
        t=time.strptime(mTime,"%b %Y")
        imgInfo.month=t.tm_mon
        imgInfo.year=t.tm_year
        print("month:%s" % imgInfo.month)
        print("year:%s" % imgInfo.year)

        imgInfo.mDate = "%d-%d-%d" %(imgInfo.year,imgInfo.month,imgInfo.day)
        
        return imgInfo

    def gotoDir(self, dir):
        if os.path.exists(dir):  # Checks if the dir exists
            print("The directory: %s exists" % dir)
        else:
            print("No directory found for " + dir)  # Output if no directory
            print
            os.makedirs(dir)  # Creates a new dir for the given name
            print("Directory created for " + dir)
        os.chdir(dir)
    
    def write2File(self,Vol,Url,Type,content,PageTime):
        print("开始生成md文件************")
        # start = time.strftime("%Y-%m-%d", time.localtime())
        tempFile = open('%s-Vol_%d.md' %(PageTime,Vol),'w',encoding='utf8')
        tempFile.write(head %(Vol,int(PageTime[:4])))
        tempFile.write("# One 一个 #\n")

        tempFile.write("### %s ###\n" %PageTime)

        tempFile.write("![%s](%s)\n" %(Type,Url))

        tempFile.write("> %s \n" %content)

        tempFile.close()


repo = Repo( r'F:\myGitHub\Dexter0218.github.io')
mgit = repo.git()
mgit.pull()


# 打开数据库连接
db = pymysql.connect("localhost", "dexter0218", "1234", "abccs")
db.set_charset('utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
cursor.execute("USE abccs")

# 使用 execute() 方法执行 SQL，如果表存在则删除
# cursor.execute("DROP TABLE IF EXISTS PAGE")

# 使用预处理语句创建表
sql = """CREATE TABLE IF NOT EXISTS PAGE (
         Vol INT(10) NOT NULL,
         PageURL TEXT NOT NULL,
         ImgURL  TEXT NOT NULL,
         ImageType  TEXT,
         Content TEXT,
         PageTime DATE  
         )"""

cursor.execute(sql)


one = getOne()
one.gotoDir(workspace)
# 从网站首页获取最新一期
starUrl = one.getFirstPage(urls).url
num = int(starUrl.split('/')[-1])

# 从数据库里找上次保存到的期数，如果没有就默认0
curSql = """SELECT PageURL FROM abccs.page Order by Vol DESC Limit 1;"""
cursor.execute(curSql)
results = cursor.fetchall()

if len(results) > 0:
    for result in results:
        currentURL=result[0]
    print(currentURL)
    databaseNUm =int(currentURL.split('/')[-1])
else:
    databaseNUm = 0

while(num > databaseNUm):
    url = "http://wufazhuce.com/one/" + str(num)
    print("page:%s" % url)
    num = num - 1
    info = one.getPic(url)
    if info == None:
        continue
    msql = "INSERT INTO Page(Vol,PageURL, ImgURL,\
       ImageType, Content,PageTime) \
       VALUES ('%d','%s','%s', '%s', '%s', '%s')" % \
        (info.VOL, url, info.url, info.type.replace("'", "''"), info.content,info.mDate )
    cursor.execute(msql)
    db.commit()
    one.write2File(info.VOL,info.url,info.type,info.content,info.mDate)
# 关闭数据库连接
db.close()


mgit.add(".")
locTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
mgit.commit('-m','%s,日常更新' %locTime)
mgit.push()