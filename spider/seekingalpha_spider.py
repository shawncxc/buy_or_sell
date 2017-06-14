import scrapy

class SeekingAlphaStockSpider(scrapy.Spider):
    name = 'seekingalpha_reviews'

    def start_requests(self):
        page_count = 10;
        url_prefix = 'https://seekingalpha.com/stock-ideas/short-ideas?page='
        for page in range(page_count):
            url = url_prefix + str(page + 1);
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for review in response.css('li.article.media'):
            yield {
                'title': review.css('div.media-body a::text').extract()[0],
                'symbol': review.css('div.a-info span a::text').extract()[0],
                'company': review.css('div.a-info span a::attr(title)').extract()[0],
                'time': review.css('div.a-info span:nth-child(3)::text').extract(),
            }

        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
