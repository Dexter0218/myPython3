import urllib.request
import urllib.parse
import re
import os

urls=["http://www.lifeofpix.com/",]

desPath = r'F:\pythonWork'

def gotoDir(dir):

    if os.path.exists(dir):#Checks if the dir exists
        print("The directory exists")
    else:
        print("No directory found for "+dir) #Output if no directory
        print
        os.makedirs(dir)#Creates a new dir for the given name
        print("Directory created for "+dir)
    os.chdir(dir)

for url in urls :
    print(url)
    req = urllib.request.Request(url)
    # 添加headers 使之看起来像浏览器在访问
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                                    '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
    response = urllib.request.urlopen(req)
    # 得到网页内容，注意必须使用decode()解码
    html = response.read().decode('utf-8')

    #print(html)

    pattern = re.compile('<img src="[a-zA-z]+://[^\s]*.jpg"',re.S)

    #pattern = re.compile('<img src=".*?"')
    result = re.findall(pattern, html)
    print(result)

    gotoDir(desPath)
    for item in result:
        imagepattern = re.compile('src="[^\s]*.jpg',re.S)
        image = re.findall(imagepattern, item)
        print(image)
        path = image[0].replace("src=\"","")
        print(path)

        p,f=os.path.split(path) 
        filename = f
        print(filename)
        if not os.path.exists(filename):
            print("dir is:" + path)  
            print("file is:" + filename) 
            urllib.request.urlretrieve(path, filename)
        else:
            print("已经存在"+filename)



