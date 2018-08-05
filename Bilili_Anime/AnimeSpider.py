import requests
from bs4 import BeautifulSoup
import re
import os
from selenium import webdriver

class AnimeSpider:
    def __init__(self,target_url):
        #网站入口
        self._service_args = []
        self._service_args.append('--load-images=no')  ##关闭图片加载
        self._service_args.append('--disk-cache=yes')  ##开启缓存
        self._service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
        self.driver = webdriver.PhantomJS(service_args=self._service_args)
        self.driver.get(target_url)

        img_req = requests.get(url=target_url, headers=header)
        img_req.encoding = 'utf-8'
        soup = BeautifulSoup(driver.page_source, 'lxml')
        urls = soup.find_all(attrs={'class': 'episode-item'})

    def get_urls(self):
        while self.mysql.get_unvisiteUrl() is not False:
            #从待访问表中取出url，并添加到已访问列表中
            visitedUrl = self.mysql.get_unvisiteUrl()


            #判断是否是目标网站
            if re.search('html$',visitedUrl):
                self.get_Images(visitedUrl)

            #解析网址元素
            req = requests.get(url=visitedUrl, headers=self.header)
            req.encoding = 'utf-8'
            url_soup = BeautifulSoup(req.text, 'lxml')

            #获取该网站title
            try:
                title = url_soup.title.get_text()
            except:
                title='noTitle'
                continue

            self.mysql.insert_visitedUrls(visitedUrl,title)

            target_urls = url_soup.find_all(attrs={'target': '_blank'})

            for target in target_urls:
                try:
                    temp=target.get('href')
                    if 'http' not in temp:
                        temp = 'http://www.mt366.com' + temp
                    if '.xml' not in temp and 'http://www.mt366.com' in temp:
                        if self.mysql.url_exist(temp):
                            #加入未访问列表
                            self.mysql.insert_unvisitedUrls(temp)
                except:
                    continue

            a,b,c=self.mysql.get_urlCount()
            print("未访问数目—>", a)
            print("已访问数目—>", b)
            print("图片数目—>", c)
            print("-----------------------------------")

    def get_Images(self,target_url):
        service_args = []
        service_args.append('--load-images=no')  ##关闭图片加载
        service_args.append('--disk-cache=yes')  ##开启缓存
        service_args.append('--ignore-ssl-errors=true')  ##忽略https错误

        driver = webdriver.PhantomJS(service_args=service_args)
        driver.get(target_url)


        # img_req = requests.get(url=target_url, headers=header)
        # img_req.encoding = 'utf-8'
        soup = BeautifulSoup(driver.page_source, 'lxml')
        urls = soup.find_all(attrs={'oncontextmenu': 'event.returnValue=false;return false;'})

        for img_url in urls:
            self.mysql.insert_imageUrl(img_url.get('src'))

        driver.quit()



'''
关于队列的创建
'''
class linkQuence:
    def __init__(self):
        # 已访问的url集合
        self.visted = []
        # 待访问的url集合
        self.unVisited = []

    # 获取访问过的url队列
    def getVisitedUrl(self):
        return self.visted

    # 获取未访问的url队列
    def getUnvisitedUrl(self):
        return self.unVisited

    # 添加到访问过得url队列中
    def addVisitedUrl(self, url):
        self.visted.append(url)

    # 移除访问过得url
    def removeVisitedUrl(self, url):
        self.visted.remove(url)

    # 未访问过得队尾的url出队列
    def unVisitedUrlDeQuence(self):
        try:
            return self.unVisited.pop()
        except:
            return None

    # 保证每个url只被访问一次,插入到队首
    def addUnvisitedUrl(self, url):
        if url != "" and url not in self.visted and url not in self.unVisited:
            self.unVisited.insert(0, url)

    # 获得已访问的url数目
    def getVisitedUrlCount(self):
        return len(self.visted)

    # 获得未访问的url数目
    def getUnvistedUrlCount(self):
        return len(self.unVisited)

    # 判断未访问的url队列是否为空
    def unVisitedUrlsEnmpy(self):
        return len(self.unVisited) == 0
