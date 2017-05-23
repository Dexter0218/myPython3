import urllib.request
import urllib.parse
import re
import os
import requests
import random
from bs4 import BeautifulSoup

urls="http://www.lifeofpix.com/"

desPath = r'F:\pythonWork'

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

def getHtmlformRequests(url):

    # 添加headers 使之看起来像浏览器在访问
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {
    'User-Agent': agent
    }
    r = requests.get(url, headers=headers)
    return r.text

def getTotalPage(html):
    pattern = re.compile('<div class="total">\d+</div>',re.S)
    #pattern = re.compile('<img src=".*?"')
    result = re.findall(pattern, html)
    num = re.sub(r'\D', "", result[0])
    print("一共需要下载 %s 页的图片"%num)
    return int(num)


def getPreviewPic(html):
    pattern = re.compile('<img src="[a-zA-z]+://[^\s]*.jpg"',re.S)
    result = re.findall(pattern, html)
    # print(result)

    gotoDir(desPath)
    for item in result:
        imagepattern = re.compile('src="[^\s]*.jpg',re.S)
        image = re.findall(imagepattern, item)
        # print(image)
        path = image[0].replace("src=\"","")
        # print(path)
        p,filename=os.path.split(path) 
        # print(filename)
        if not os.path.exists(filename):
            
            if not (filename.endswith("150x150.jpg")):
                print("下载链接:" + path)  
                print("文件名:" + filename) 
                print("下载小图中，请耐心等待...") 
                urllib.request.urlretrieve(path, filename)
        else:
            print("已经存在"+filename)


def getPreviewPicBysoup(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_a =soup.find('div',class_="wide-list animated-grid").find_all('img')
    for a in all_a:
        srcPath = a['src']
        if not srcPath.endswith('150x150.jpg') and srcPath.endswith('.jpg'):
            p,filename=os.path.split(srcPath) 
            # print(filename)
            if not os.path.exists(filename):
                if not (filename.endswith("150x150.jpg")):
                    print("下载链接:" + srcPath)  
                    print("文件名:" + filename) 
                    print("下载小图中，请耐心等待...") 
                    urllib.request.urlretrieve(srcPath, filename)
            else:
                print("已经存在"+filename)

def getDownloadPic(html):
    pattern = re.compile('<a download="[a-zA-z]+://[^\s]*.jpg"',re.S)
    result = re.findall(pattern, html)
    print(result)

    for item in result:
        imagepattern = re.compile('download="[^\s]*.jpg',re.S)
        image = re.findall(imagepattern, item)
        # print(image)
        path = image[0].replace("download=\"","")
        # print(path)

        p,filename=os.path.split(path) 
        # print(filename)
        if not os.path.exists(filename):
            if not (filename.endswith("150x150.jpg")):
                print("下载链接:" + path)  
                print("文件名:" + filename) 
                print("下载大图中，请耐心等待...") 
                urllib.request.urlretrieve(path, filename)
        else:
            print("已经存在"+filename)

def getDownloadPicBysoup(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_b =soup.find('div',class_="wide-list animated-grid").find_all('a',class_='download')
    for b in all_b:
        srcPath = b['download']
        if not srcPath.endswith('150x150.jpg') and srcPath.endswith('.jpg'):
            p,filename=os.path.split(srcPath) 
            # print(filename)
            if not os.path.exists(filename):
                if not (filename.endswith("150x150.jpg")):
                    print("下载链接:" + srcPath)  
                    print("文件名:" + filename) 
                    print("下载大图中，请耐心等待...") 
                    urllib.request.urlretrieve(srcPath, filename)
            else:
                print("已经存在"+filename)

def getUserDecesion():
    inputstr = input("请输入你要下载类型，预览图片回“1”，原图回“2”，退出回复“0”:")
    while((inputstr != str(1)) and (inputstr != str(2))):
        if inputstr == str(0):
            break
        inputstr = input ("你输入的内容有误，请重新输入: ")
    if(inputstr == str(1)):
        print ("你选择的是: 预览图片")
        return 1
    elif (inputstr == str(2)):
        print ("你选择的是: 原始图片")
        return 2
    else:
        print("结束")
        exit()


#main method
picVersion = getUserDecesion()
abc = download()

totalPageNumber = getTotalPage(getHtml(urls))

gotoDir(desPath)
i = 0
for i in range(totalPageNumber):
    url = urls+"page/"+str(i+1)
    i = i + 1
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(url)
    if (picVersion == 1):
        # getPreviewPic(getHtml(url))
        getPreviewPicBysoup(abc.get(url).text)
    elif (picVersion == 2):
        getDownloadPic(getHtml(url))
