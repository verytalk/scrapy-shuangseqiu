#coding=utf-8
import scrapy
import re
import os
import urllib
import MySQLdb
import sys
import datetime
import time
import calendar

from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request

from webCrawler_scrapy.date import getBetweenMonth
from webCrawler_scrapy.dbhelper import DBHelper
from webCrawler_scrapy.items import WebcrawlerScrapyItem

class SpiderRunner(scrapy.spiders.Spider):
    name="webCrawler_scrapy"    #定义爬虫名，要和settings中的BOT_NAME属性对应的值一致

    allowed_domains=["kaijiang.zhcw.com"] #搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    start_urls=["http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html"]   #开始爬取的地址
    #该函数名不能改变，因为Scrapy源码中默认callback函数的函数名就是parse
    def parse(self, response):
        print "-------------- start spider --------------"
        se = Selector(response) #创建查询对象，HtmlXPathSelector已过时
        #print se.xpath("//html").extract()
       # print response.url
        #print "======----=-=-=-=-=-=-="

        print "response url: ",response.url

        matchURL = re.match(r"http://kaijiang.zhcw.com/zhcw/html/ssq/list_(.*).html", response.url)
        print matchURL
        if(matchURL): #如果url能够匹配到需要爬取的url，就爬取
            page_code = matchURL.group(1)
            print "page code is : " , page_code
            print "--------------start analysis--------------"

            src = se.xpath("//table[@class='wqhgt']")

            print "src is: ",src

            print "weather list size : ",range(len(src))

            # print src[1].xpath('li//text()').extract()
            # print src[2].xpath('li//text()').extract()
            srcCount = range(len(src))

            data = src.xpath("tr")  # 依次抽取所需要的信息

            dataCount = range(len(data))

            print "--------------start dataCount--------------",dataCount,data

            #print data[0].xpath('div//text()').extract()

            page = se.xpath("//p[@class='pg']/strong//text()").extract()

            for j in dataCount:

                #dateWeater = data[j].xpath('td//text()').extract()
                dateList = data[j].xpath('td')

                print dateList
                dataListCountRange = range(len(dateList))
                dataListCount = len(dateList)

                #print dateList[0],dateList[1],dateList[2],dateList[3],dateList[4],dateList[5]
                print "=======-------",dataListCountRange,len(dateList)

                if dataListCount == 7:
                    openDate = dateList[0].xpath('text()').extract()[0]
                    issueDate = dateList[1].xpath('text()').extract()[0]
                    issueNo = dateList[2].xpath('em//text()').extract()
                    issueNo_1 = issueNo[0]
                    issueNo_2 = issueNo[1]
                    issueNo_3 = issueNo[2]
                    issueNo_4 = issueNo[3]
                    issueNo_5 = issueNo[4]
                    issueNo_6 = issueNo[5]
                    issueNo_blue = issueNo[6]
                    issueAmountTotal = dateList[3].xpath('strong//text()').extract()[0]
                    firstPrize = dateList[4].xpath('strong//text()').extract()[0]
                    secondPrize = dateList[5].xpath('strong//text()').extract()[0]
                    print openDate, issueDate, issueNo,issueAmountTotal,firstPrize,secondPrize
                    item = WebcrawlerScrapyItem()
                    item['openDate'] = openDate
                    item['issueDate'] = issueDate
                    item['issueNo_1'] = issueNo_1
                    item['issueNo_2'] = issueNo_2
                    item['issueNo_3'] = issueNo_3
                    item['issueNo_4'] = issueNo_4
                    item['issueNo_5'] = issueNo_5
                    item['issueNo_6'] = issueNo_6
                    item['issueNo_blue'] = issueNo_blue
                    item['issueAmountTotal'] = issueAmountTotal
                    item['firstPrize'] = firstPrize
                    item['secondPrize'] = secondPrize
                    item['remark'] = page_code
                    yield item

            totalPage = page[0]

            # if 1 <= int(page_code) <= int(totalPage):
            #
            #     time.sleep(5)
            #     print "----request----","http://kaijiang.zhcw.com/zhcw/html/ssq/list_" + str(int(page_code) + 1) + ".html"
            #     yield Request("http://kaijiang.zhcw.com/zhcw/html/ssq/list_" + str(int(page_code) + 1) + ".html", callback=self.parse)

            print "--------totalPage-------", totalPage, page_code

            for num in range(2, int(totalPage)+1):
                yield Request("http://kaijiang.zhcw.com/zhcw/html/ssq/list_" + str(num) + ".html",callback=self.parse)
                print num

