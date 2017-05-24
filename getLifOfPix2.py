import os
from bs4 import BeautifulSoup
from Download import mRequest
import re

urls="http://www.lifeofpix.com/"
desPath = r'F:\pythonWork2'
class getLifeOfPix():

    def getTotalPage(self,url):
        html = mRequest.get(url).text
        pattern = re.compile('<div class="total">\d+</div>',re.S)
        #pattern = re.compile('<img src=".*?"')
        result = re.findall(pattern, html)
        num = re.sub(r'\D', "", result[0])
        print("一共需要下载 %s 页的图片"%num)
        return int(num)

    def getPreviewPicBysoup(self,url):
        html = mRequest.get(url).text
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
                        img = mRequest.get(srcPath)
                        mImgFile = open(filename,'ab')
                        mImgFile.write(img.content)
                        mImgFile.close()
                        # urllib.request.urlretrieve(srcPath, filename)
                else:
                    print("已经存在"+filename)

    def gotoDir(self,dir):
        if os.path.exists(dir):#Checks if the dir exists
            print("The directory: %s exists"%dir)
        else:
            print("No directory found for "+dir) #Output if no directory
            print
            os.makedirs(dir)#Creates a new dir for the given name
            print("Directory created for "+dir)
        os.chdir(dir)

mLifeOfPix = getLifeOfPix()
mLifeOfPix.gotoDir(desPath)
mLifeOfPix.getPreviewPicBysoup(urls)