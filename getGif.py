import urllib.request
import urllib.parse
import re
import os
import time
import requests
import random

urls="http://joke.4399pk.com/funnyimg/find.html#"

desPath = r'F:\gifPic'
class download:
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def get(self, url):
        UA = random.choice(self.user_agent_list) ##从self.user_agent_list中随机取出一个字符串（聪明的小哥儿一定发现了这是完整的User-Agent中：后面的一半段）
        headers = {'User-Agent': UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
        print(headers) ##打印headers
        response = requests.get(url, headers=headers) ##这样服务器就会以为我们是真的浏览器了
        return response

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
instance = download()

startUrl = getFirstPage(instance.get(urls).text)
# startUrl = 'http://joke.4399pk.com/funnyimg/10529.html'
# mHtml = getHtml(startUrl)
mHtml = instance.get(startUrl).text
nextUrl = getNextPage(mHtml)
while nextUrl != startUrl:
    mHtml = instance.get(nextUrl).text
    getImages(mHtml)
    nextUrl = getNextPage(mHtml)
    print("休眠20s")
    time.sleep(20)