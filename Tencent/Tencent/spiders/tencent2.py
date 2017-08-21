# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ["http://hr.tencent.com/position.php?start=0"]
    
    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        next_url = response.xpath("//a[@id='next']/@href").extract()[0]
        for node in node_list:
            item = TencentItem()
            # 提取每个职位的相关信息并转码为utf-8编码
            item['positionName'] = node.xpath(".//a/text()").extract()[0].encode("utf-8")
            item['positionLink'] = node.xpath(".//a/@href").extract()[0].encode("utf-8")
            if len(node.xpath("./td[2]/text()")):
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0].encode("utf-8")
            else:
                item['positionType'] = ""
            item['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0].encode("utf-8")
            item['workLocation'] = node.xpath("./td[4]/text()").extract()[0].encode("utf-8")
            item['publishTime'] = node.xpath("./td[5]/text()").extract()[0].encode("utf-8")

            yield item
        
        if len(next_url) > 15:
            url = "http://hr.tencent.com/" + next_url
            yield scrapy.Request(url, callback = self.parse)