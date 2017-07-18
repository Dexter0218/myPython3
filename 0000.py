from PIL import Image, ImageDraw, ImageFont


def addNum(filePath):
    img = Image.open(filePath)
    size = img.size
    fontSize = int(size[1] / 4)
    draw = ImageDraw.Draw(img)
    
    ttFont = ImageFont.truetype(u'./static/simheittf/simhei.ttf', fontSize)
    draw.text((size[0]-fontSize*2, 0), "ZTE",(0,256,256), font=ttFont)
    del draw
    img.save('./result.jpg')
    img.show()


if __name__ == '__main__':
    addNum("hlm.jpg")
