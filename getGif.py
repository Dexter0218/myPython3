import urllib.request
import urllib.parse
import re
import os
import time

urls="http://joke.4399pk.com/funnyimg/find.html#"

desPath = r'F:\gifPic'


def gotoDir(dir):

    if os.path.exists(dir):#Checks if the dir exists
        print("The directory: %s exists"%dir)
    else:
        print("No directory found for "+dir) #Output if no directory
        print
        os.makedirs(dir)#Creates a new dir for the given name
        print("Directory created for "+dir)
    os.chdir(dir)

def getHtml(url):
    req = urllib.request.Request(url)
    # 添加headers 使之看起来像浏览器在访问
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                                    '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
    response = urllib.request.urlopen(req)
    # 得到网页内容，注意必须使用decode()解码
    html = response.read().decode('utf-8')
    return html


def getFirstPage(html):
    pattern = re.compile('<a class="img".*?href="[^\s]*.html"',re.S)
    Allhtml = re.findall(pattern, html)
    htmlpattern = re.compile('href="[^\s]*.html')
    html = re.findall(htmlpattern, Allhtml[0])
    result = html[0].replace("href=\"","")
    print(result)
    return result

def getNextPage(html):
    pattern = re.compile('class="next-pic".*?href="[^\s]*.html"',re.S)
    Allhtml = re.findall(pattern, html)
    htmlpattern = re.compile('href="[^\s]*.html')
    html = re.findall(htmlpattern, Allhtml[0])
    result = html[0].replace("href=\"","")
    print(result)
    return result

def getImages(html):
    pattern = re.compile('big_src="[^\s]*"',re.S)
    AllImage = re.findall(pattern, html)
    print(AllImage)
    for item in AllImage:
        time.sleep(1)
        imagepath = item.split('"')[1]
        print(imagepath)
        p,filename=os.path.split(imagepath)
        if not os.path.exists(filename):
            if not (filename.endswith("150x150.jpg")):
                print("下载链接:" + imagepath)  
                print("文件名:" + filename) 
                print("下载小图中，请耐心等待...")
                urllib.request.urlretrieve(imagepath, filename)
                time.sleep(2)
        else:
            print("已经存在"+filename) 


gotoDir(desPath)
# startUrl = getFirstPage(getHtml(urls))
startUrl = 'http://joke.4399pk.com/funnyimg/10529.html'
mHtml = getHtml(startUrl)
nextUrl = getNextPage(mHtml)
while nextUrl != startUrl:
    mHtml = getHtml(nextUrl)
    getImages(mHtml)
    time.sleep(200)
    nextUrl = getNextPage(mHtml)