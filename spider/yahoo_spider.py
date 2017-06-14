import scrapy

class YahooStockSpider(scrapy.Spider):
    name = 'yahoostocks'

    def start_requests(self):
        urls = [
            'https://finance.yahoo.com/screener/predefined/top_mutual_funds?offset=0&count=1000'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for stock in response.css('tr.BdT'):
            yield {
                'symbol': stock.css('.data-col0 a::text').extract()[0],
                'company': stock.css('.data-col1::text').extract()[0],
                'change': stock.css('.data-col3 span::text').extract()[1],
            }

        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
