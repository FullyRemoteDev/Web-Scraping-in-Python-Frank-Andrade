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

    # For MongoDB no need to join transcripts as it can be stored as an array
    # def parse_item(self, response):
    #     article = response.xpath('//article[@class="main-article"]')
    #
    #     yield {
    #         'Title': article.xpath('./h1/text()').get(),
    #         'Plot': article.xpath('./p/text()').get(),
    #         'Transcript': article.xpath('./div[@class="full-script"]/text()').getall(),
    #         'URL': response.url,
    #     }

    # For SQLite the transcripts have to be joined to store as Text as SQlite does not store arrays
    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')
        transcript_list = article.xpath('./div[@class="full-script"]/text()').getall()
        transcript_string = ' '.join(transcript_list)

        yield {
            'Title': article.xpath('./h1/text()').get(),
            'Plot': article.xpath('./p/text()').get(),
            'Transcript': transcript_string,
            'URL': response.url,
        }
