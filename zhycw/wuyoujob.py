import scrapy


class WuyoujobItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    money = scrapy.Field()
    data = scrapy.Field()