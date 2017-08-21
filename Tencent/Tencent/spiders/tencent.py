# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    baseURL = "http://hr.tencent.com/position.php?start="
    offset = 0
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

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
        if self.offset <= 2270:
            self.offset += 10
            url = self.baseURL + str(self.offset)
            yield scrapy.Request(url, callback = self.parse)