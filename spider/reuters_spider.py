import scrapy

class ReutersNewsSpider(scrapy.Spider):
    name = 'reutersnews'

    start_urls = [
    	'http://www.reuters.com/news/archive/marketsNews?view=page&pageSize=10&page={page}'.format(page=page) for page in range(1, 10)
    ] + [
    	'http://www.reuters.com/news/archive/businessNews?view=page&pageSize=10&page={page}'.format(page=page) for page in range(1, 10)
    ] + [
     	'http://www.reuters.com/news/archive/mcBreakingviews?view=page&pageSize=10&page={page}'.format(page=page) for page in range(1, 10)
    ] + [
    	'http://www.reuters.com/news/archive/technologyNews?view=page&pageSize=10&page={page}'.format(page=page) for page in range(1, 10)
    ]

    def parse(self, response):
        for news in response.css('div.story-content'):
            yield {
                'title': news.css('h3.story-title::text').extract()[0],
                'content': news.css('p::text').extract()[0],
                'date': news.css('span.timestamp::text').extract()[0],
            }
