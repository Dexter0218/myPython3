# coding: utf-8
from os import path
import numpy as np
import matplotlib.pyplot as plt
# matplotlib.use('qt4agg')
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import jieba


class WordCloud_CN:
    '''
    use package wordcloud and jieba
    generating wordcloud for chinese character
    '''

    def __init__(self, stopwords_file):
        self.stopwords_file = stopwords_file
        self.text_file = text_file

    @property
    def get_stopwords(self):
        self.stopwords = {}
        f = open(self.stopwords_file, 'r', encoding='UTF-8')
        line = f.readline().rstrip()
        while line:
            self.stopwords.setdefault(line, 0)
            self.stopwords[line] = 1
            line = f.readline().rstrip()
        f.close()
        return self.stopwords

    @property
    def seg_text(self):
        with open(self.text_file,'r', encoding='UTF-8') as f:
            text = f.readlines()
            text = r' '.join(text)

            seg_generator = jieba.cut(text)
            self.seg_list = [
                i for i in seg_generator if i not in self.get_stopwords]
            self.seg_list = [i for i in self.seg_list if i != u' ']
            self.seg_list = r' '.join(self.seg_list)
        return self.seg_list

    def show(self):
        # wordcloud = WordCloud(max_font_size=40, relative_scaling=.5)
        wordcloud = WordCloud(font_path=u'./static/simheittf/simhei.ttf',
                              background_color="white", width=1800, height=800)
        # mask = np.array(Image.open(mask_path))
        # wordcloud = WordCloud(font_path=u'./static/simheittf/simhei.ttf',background_color="black", mask=mask)

        wordcloud = wordcloud.generate(self.seg_text)
        wordcloud.to_file('hlm.jpg')
        plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

if __name__ == '__main__':
    mask_path = u'./static/zte_watermark.png'
    stopwords_file = u'./static/stopwords.txt'
    # text_file = u'./demo/测试.txt'
    text_file = u'./句子.txt'
    generater = WordCloud_CN(stopwords_file)
    generater.show()