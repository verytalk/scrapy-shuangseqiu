# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import json
from logging import log

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('info.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class WebcrawlerScrapyPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparams=dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self._handle_error,item,spider)
        return item
    
    def _conditional_insert(self,tx,item):
        #print item['name']
        sql="INSERT INTO `issues_list`(`id`, `open_date`, `issue_date`, `issue_no_1`, `issue_no_2`, `issue_no_3`, `issue_no_4`, `issue_no_5`, `issue_no_6`, `issue_no_blue`, `issue_amount_total`, `first_prize`, `second_prize`, `remark`) VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


        params=( item['openDate'],
                item['issueDate'],
                item['issueNo_1'],
                item['issueNo_2'],
                item['issueNo_3'],
                item['issueNo_4'],
                item['issueNo_5'],
                item['issueNo_6'],
                item['issueNo_blue'],
                item['issueAmountTotal'],
                item['firstPrize'],
                item['secondPrize'],
                item['remark'])
        tx.execute(sql,params)
    
    def _handle_error(self, failue, item, spider):
        print '--------------database operation exception!!-----------------'
        print '-------------------------------------------------------------'
        print failue