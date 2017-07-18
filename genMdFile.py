import os
import time

head = '<font size="12" color="Blue"><center><b> %d</b></center ></font>\n\n'
content = '<font size="5" color="Black"><center> %s </center ></font>\n\n'
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):  
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)  
    return fileList
 
def GetFileName(dir):
    fileNameList=[]
    list = GetFileList(dir, [])
    for filePath in list:
        fileName = filePath.split('\\')[-1].split('.')[0]
        fileNameList.append(fileName)
        print(fileName)
    return fileNameList

def write2File(fileNameList):
    
    start = time.strftime("%Y-%m-%d", time.localtime())
    tempFile = open('%s.md' %(start),'w',encoding='utf8')
    num=1;
    for file in fileNameList:
        tempFile.write(head %(num))
        num+=1
        tempFile.write(content %file)
        tempFile.write("---\n")
    tempFile.close()

fileList = GetFileName(u'F:\pythonWork2')
write2File(fileList)
