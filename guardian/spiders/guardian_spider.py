import scrapy
from guardian.items import GuardianItem


def clean_text(txt, join=1):
    if join == 0:
        txt = [t.strip() for t in txt]
    elif join == 1:
        txt = [t.strip() for t in txt]
        txt = ' '.join(txt).strip()
    else:
        txt = txt.strip()
    return txt


class Guardian_Spider(scrapy.Spider):
    name = "guardian"

    start_urls = "https://www.theguardian.com/international"

    # start_requests method
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_front, dont_filter=True)

    # First, Parsing main page categories["News", "Opinion", "Sport", ...]
    def parse_front(self, response):
        categories = response.xpath('//li[contains(@class,"pillars__item")]')
        categories_links = categories.xpath('./a/@href').extract()
        categories_name = clean_text(categories.css('a::text').extract(), join=0)
        for url, category in zip(categories_links, categories_name):
            yield response.follow(url=url,
                                  meta={"category": category},
                                  callback=self.parse_subcategory)

    # Second, Parsing subcategories ["News" : ['Covid, UK, World'], "Opinion" : ['Cartoon','Letter'], ...]
    def parse_subcategory(self, response):
        subcategory_links = response.xpath('//li[contains(@class,"subnav__item")]')
        for url in subcategory_links:
            subcategory_name = clean_text(url.css('a::text').extract_first(), 2)
            subcategory_link = url.css('a::attr(href)').extract_first()
            yield response.follow(url=subcategory_link,
                                  meta={"subcategory_name": subcategory_name, "category": response.meta["category"]},
                                  callback=self.parse_pages)

    # Third, Parsing sub-categories page and get articles
    def parse_pages(self, response):
        pages = response.xpath('//a[contains(@data-link-name,"article")]')
        for page in pages:
            pages_name = clean_text(page.css('a *::text').extract(), 1)
            pages_link = page.css('a::attr(href)').extract_first()
            yield response.follow(url=pages_link,
                                  meta={"subcategory_name": response.meta["subcategory_name"],
                                        "category": response.meta["category"],
                                        "page_name": pages_name
                                        },
                                  callback=self.article_parse)

    # Forth, Parsing article, title and writer
    def article_parse(self, response):
        item = GuardianItem()
        article_txt = response.xpath('//div[contains(@itemprop,"articleBody")]//text()').extract()
        article_caption = response.xpath('//*[contains(@class,"caption--main")]//text()').extract()
        article_title = response.xpath('//h1[contains(@class,"headline")]//text()').extract_first()
        article_writer = response.xpath('//span[contains(@itemprop,"name")]//text()').extract_first()
        article_time = response.xpath('//time[contains(@class,"dateline")]/@datetime').extract_first()
        article_title = clean_text(article_title, join=2)
        article_txt = clean_text(article_txt, join=1)
        article_caption = clean_text(article_caption)
        article_writer = clean_text(article_writer, join=2)
        item['category'] = response.meta["category"]
        item['subcategory_name'] = response.meta["subcategory_name"]
        item['page_name'] = response.meta["page_name"]
        item['article_url'] = response.request.url
        item['article_writer'] = article_writer
        item['article_time'] = article_time
        item['article_title'] = article_title
        item['article_caption'] = article_caption
        item['article_txt'] = article_txt
        yield item
