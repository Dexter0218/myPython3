import urllib.request
import urllib.parse
import re
import os

urls="http://www.lifeofpix.com/"

desPath = r'F:\pythonWork'


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



def getUserDecesion():
    inputstr = input("请输入你要下载类型，预览图片回“1”，原图回“2”:")
    while((inputstr != str(1)) and (inputstr != str(2))):
        inputstr = input ("你输入的内容有误，请重新输入: ")
    if(inputstr == str(1)):
        print ("你选择的是: 预览图片")
        return 1
    elif (inputstr == str(2)):
        print ("你选择的是: 原始图片")
        return 2
    else:
        print("出现异常")
        return 0

#main method
picVersion = getUserDecesion()
totalPageNumber = getTotalPage(getHtml(urls))
gotoDir(desPath)
i = 0
for i in range(totalPageNumber):
    url = urls+"page/"+str(i+1)
    i = i + 1
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(url)
    if (picVersion == 1):
        getPreviewPic(getHtml(url))
    elif (picVersion == 2):
        getDownloadPic(getHtml(url))