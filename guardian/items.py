# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item


class GuardianItem(Item):
    category = Field()
    article_url = Field()
    page_name = Field()
    subcategory_name = Field()
    article_writer = Field()
    article_time = Field()
    article_title = Field()
    article_caption = Field()
    article_txt = Field()
