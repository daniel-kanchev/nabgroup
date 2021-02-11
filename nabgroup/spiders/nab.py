import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from nabgroup.items import Article


class NabSpider(scrapy.Spider):
    name = 'nab'
    start_urls = ['https://news.nab.com.au/']

    def parse(self, response):
        links = response.xpath('//h3/a[@class="box_title"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="post-title"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//b[@class="text-red"]/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%d %b %Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="main-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
