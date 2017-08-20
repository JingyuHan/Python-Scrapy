# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from ITcast.items import ItcastItem

class ItcastSpider(scrapy.Spider):
    # 爬虫名，启动爬虫时需要，必须
    name = 'itcast'
    # 爬取域名范围，可选
    allowed_domains = ['http://www.itcast.cn']
    # qishiurl列表，爬虫执行后的第一批请求，从这个列表获取
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        node_list = response.xpath("//div[@class='li_txt']")
        #用来存储所有item字段
        items = []
        for node in node_list:
            # 创建item字段对象
            item = ItcastItem()

            item['name'] = node.xpath("./h3/text()").extract()[0]
            item['title'] = node.xpath("./h4/text()").extract()[0]
            item['info'] = node.xpath("./p/text()").extract()[0]
            items.append(item)
        return items