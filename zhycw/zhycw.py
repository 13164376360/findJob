# -*- coding: utf-8 -*-
import scrapy
import re
from .wuyoujob import WuyoujobItem
import urllib as parse


class Wuyoujob1Spider(scrapy.Spider):
    name = 'wuyoujob1'
    allowed_domains = ['search.chinahr.com']

    start_urls = ['http://search.chinahr.com/sh/job/pn1/?key=hrbp']

    def parse(self, response):
        # print response.body
        # 定义workItem用于保存获取的信息,并定义xpath的根节点
        workItem = []
        workname_list = response.xpath('//div[@class="jobList pc_search_listclick"]')
        for each in workname_list:
            item = WuyoujobItem()
            # 使用xpath工具截取需要的信息
            name = each.xpath('./ul[@class="l1"]/li[@class="job-name"]/text()').extract()
            address = each.xpath('./ul[@class="l2"]/li[@class="job-address"]/text()').extract()
            company = each.xpath('./ul[@class="l2"]/li[@class="job-company"]/text()').extract()
            data = each.xpath('./ul[@class="l1"]/li[@class="fabu-date"]/text()').extract()
            money = each.xpath('./ul[@class="l2"]/li[@class="job-salary"]/text()').extract()
            # 保存获取到的信息
            item['name'] = name[0]
            item['company'] = company[0]
            item['address'] = address[0]
            item['data'] = data[0]
            item['money'] = money[0]
            workItem.append(item)
            # 搜索当前的页数
            curpage = re.search('(\d+)', response.url).group(1)
            # 对页数进行加以操作
            page = int(curpage) + 1

            url = re.sub('(\d+)', str(page), response.url, 1)
            # 重新发送请求,并重新调用parse函数实现自动翻页的功能
            yield scrapy.Request(url, callback=self.parse)

            yield item
    # return workItem

