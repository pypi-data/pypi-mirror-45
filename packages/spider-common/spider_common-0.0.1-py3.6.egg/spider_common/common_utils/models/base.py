from scrapy.item import Item, Field


class BaseModel(Item):
    name = Field()
    leads_src = Field()  # 中文 线索渠道的来源站点名称
    channel = Field()  # 英文 线索渠道的业务名称
    crawled_time = Field()
