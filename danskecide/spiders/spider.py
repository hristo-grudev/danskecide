import scrapy

from scrapy.loader import ItemLoader

from ..items import DanskecideItem
from itemloaders.processors import TakeFirst


class DanskecideSpider(scrapy.Spider):
	name = 'danskecide'
	start_urls = ['https://danskeci.com/ci/news-and-insights/archive/all-news-and-insights']

	def parse(self, response):
		post_links = response.xpath('//div[@class="news-links"]/ul/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[contains(@class, "article-body") or contains(@class, "article-header")]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="meta"]/span/text()').get()

		item = ItemLoader(item=DanskecideItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
