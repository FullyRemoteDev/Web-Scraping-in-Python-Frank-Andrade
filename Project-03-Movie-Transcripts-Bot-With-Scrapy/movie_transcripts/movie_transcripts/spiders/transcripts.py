import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = 'transcripts'
    allowed_domains = ['subslikescript.com']
    # start_urls = ['https://subslikescript.com/movies']

    # Temporarily limiting the number of items to scrape
    start_urls = ['https://subslikescript.com/movies_letter-X']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://subslikescript.com/movies_letter-X', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="scripts-list"]/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='(//a[@rel="next"])[1]'), process_request='set_user_agent'),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')

        yield {
            'Title': article.xpath('./h1/text()').get(),
            'Plot': article.xpath('./p/text()').get(),
            'Transcript': article.xpath('./div[@class="full-script"]/text()').getall(),
            'URL': response.url,
            'User-Agent': response.request.headers['User-Agent'],
        }
