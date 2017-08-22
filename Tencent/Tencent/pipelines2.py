# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html  
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class TencentPipeline(object):
    def __init__(self):  
        try:  
            self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="******", port=3306, db="python",  charset="utf8")  
            self.cursor = self.db.cursor()  
            print "Connect to db successfully!"  

        except:  
            print "Fail to connect to db!" 

    def process_item(self, item, spider):
        param = (0, item['positionName'], item['positionLink'], item['positionType'],item['peopleNumber'],item['workLocation'],item['publishTime'])  
        sql = "insert into tencent (id,pname,plink,ptype,pnum,wloca,ptime) values(%c,%s,%s,%s,%s,%s,%s)"  
        self.cursor.execute(sql, param)
        return item

    def close_spider(self,spider):
        self.db.commit() 
        self.db.close 
        print("Done")