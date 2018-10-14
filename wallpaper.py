#_*_ coding:utf-8 _*_
#爬取wallhaven上的图片


import os
import requests
import time
import random
from lxml import etree


keyword = raw_input('please import keywords that you want to download:')
class Spider(object):
    def __init__(self):
        self.header = {"User_Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        self.filePath = (r'/users/zhouhui/壁纸/'+keyword+'/')

    def create_file(self):
        filePath = self.filePath
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    def get_pageNum(self):
        total = ''
        url = ('https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc'.format(keyword))
        response = requests.get(url)
        html = etree.HTML(response.text)
        pageInfo = html.xpath('//header[@class="listing-header"]/h1/text()')
        string = str(pageInfo[0])
        numlist = list(filter(str.isdigit, string))
        for item in  numlist:
            total += item
        totalPagenum = int(total)
        return totalPagenum
    def main_function(self):
        self.create_file()
        count = self.get_pageNum()
        print('we have found:{} images!'.format(count))
        times = int(count/24+1)
        j = 1
        for i in range(times):
            pic_Urls = self.getLinks(i+1)
            for item in pic_Urls:
                self.download(item, j)
                j += 1
    def getLinks(self,number):
        url = 'https://alpha.wallhaven.cc/search?q={}&search_image=&page={}'.format(keyword, number)
        try:
            response = requests.get(url)
            html = etree.HTML(response.text)
            pic_Linklist = html.xpath('//a[@class="preview"]/@href')
        except Exception as e:
            print(repr(e))
        return pic_Linklist

    def download(self,url,count):
        string = url.strip("https://alpha.wallhaven.cc/wallpaper/")
        html = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-'+string+'.jpg'
        pic_path = (self.filePath+keyword+str(count)+'.jpg')
        try:
            pic = requests.get(html,headers = self.header)
            with open(pic_path,'wb') as f:
                f.write(pic.content)
            print 'Images:{} has been download!'.format(count)
            time.sleep(random.uniform(0,2))
        except Exception as e:
            print repr(e)

if __name__ == "__main__":
    spider = Spider()
    spider.main_function()









