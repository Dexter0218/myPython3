import urllib.request
import urllib.parse
import re
import os

url="http://www.gratisography.com/"
req = urllib.request.Request(url)
# 添加headers 使之看起来像浏览器在访问
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
response = urllib.request.urlopen(req)
    # 得到网页内容，注意必须使用decode()解码
html = response.read().decode('utf-8')

#print(html)

pattern = re.compile('<img class="lazy" src=".*?.jpg',re.S)

#pattern = re.compile('<img src=".*?"')
result = re.findall(pattern, html)
os.chdir(r'F:\pythonWork')
for item in result:
    imagepattern = re.compile('data-original=".*?.jpg',re.S)
    image = re.findall(imagepattern, item)
    path = image[0].replace("data-original=\"","")
    if not path.startswith('http'):
        filename = path.replace("/","")
        path = url + path
    else :
       p,f=os.path.split(path) 
       a,b= os.path.split(p)
       filename = b+f
      
    if not os.path.exists(filename):
        print("dir is:" + path)  
        print("file is:" + filename) 
        urllib.request.urlretrieve(path, filename)
    else:
        print("已经存在"+filename)


