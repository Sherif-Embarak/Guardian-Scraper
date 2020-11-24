import scrapy
from guardian.items import GuardianItem


class Guardian_Spider(scrapy.Spider):
    name = "guardian"

    start_urls = "https://www.theguardian.com/international"

    # start_requests method
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_front, dont_filter = True)

    # First, Parsing main page categories
    def parse_front(self, response):
        categories = response.xpath('//li[contains(@class,"pillars__item")]')
        categories_links = categories.xpath('./a/@href').extract()
        categories_name = self.clean_text(categories.css('a::text').extract(), join=0)
        cnt = 0
        for url, category in zip(categories_links, categories_name):
            if category == "News":
                print(str(url) +" "+str(category))
                if cnt > 2:
                    break
                #cnt = cnt + 1
                yield response.follow(url=url,
                                      meta={"category": category},
                                      callback=self.parse_subcat)

    # Second, Parsing sub-categories
    def parse_subcat(self, response):
        print(response.meta["category"])
        subcat_links = response.xpath('//li[contains(@class,"subnav__item")]')
        cnt = 0
        for url in subcat_links:
            if cnt > 2:
                break
            #cnt = cnt + 1
            subcat_name = self.clean_text(url.css('a::text').extract_first(), 2)
            subcat_link = url.css('a::attr(href)').extract_first()
            yield response.follow(url=subcat_link,
                                  meta={"subcat_name": subcat_name, "category": response.meta["category"]},
                                  callback=self.parse_pages)

    # Third, Parsing sub-categories page and get articles
    def parse_pages(self, response):
        pages = response.xpath('//a[contains(@data-link-name,"article")]')
        cnt = 0
        for page in pages:
            if cnt > 2:
                break
            #cnt = cnt + 1
            pages_name = self.clean_text(page.css('a *::text').extract(), 1)
            pages_link = page.css('a::attr(href)').extract_first()
            yield response.follow(url=pages_link,
                                  meta={"subcat_name": response.meta["subcat_name"],
                                        "category": response.meta["category"],
                                        "page_name": pages_name
                                        },
                                  callback=self.article_parse)

    # Forth, Parsing article, title and writer
    def article_parse(self, response):
        item = GuardianItem()
        article_txt = response.xpath('//div[contains(@itemprop,"articleBody")]//text()').extract()
        #article_txt = article_div.css('p *::text').extract()
        article_caption = response.xpath('//*[contains(@class,"caption--main")]//text()').extract()
        article_title = response.xpath('//h1[contains(@class,"headline")]//text()').extract_first()
        article_writer = response.xpath('//span[contains(@itemprop,"name")]//text()').extract_first()
        article_time = response.xpath('//time[contains(@class,"dateline")]/@datetime').extract_first()
        article_title = self.clean_text(article_title, join=2)
        article_txt = self.clean_text(article_txt, join=1)
        article_caption = self.clean_text(article_caption)
        article_writer = self.clean_text(article_writer, join=2)
        item['category'] = response.meta["category"]
        item['subcat_name'] = response.meta["subcat_name"]
        item['page_name'] = response.meta["page_name"]
        item['article_url'] = response.request.url
        item['article_writer'] = article_writer
        item['article_time'] = article_time
        item['article_title'] = article_title
        item['article_caption'] = article_caption
        item['article_txt'] = article_txt
        yield item

    def clean_text(self, txt, join=1):
        if (join == 0):
            txt = [t.strip() for t in txt]
        elif (join == 1):
            txt = [t.strip() for t in txt]
            txt = ' '.join(txt).strip()
        else:
            txt = txt.strip()
        return txt
