import scrapy

class AosFatosSpider(scrapy.Spider):
    name = 'aosFatos'

    start_urls = ['https://aosfatos.org/']
        
    def parse(self, response):
        links = response.xpath('//nav//ul//li/a[re:test(@href, "checamos")]/@href').getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_category
            )

    def parse_category(self, response):
        news = response.css('a.entry-item-card::attr(href)').getall()
        for new_url in news:
            yield scrapy.Request(
                response.urljoin(new_url),
                callback=self.parse_new
            )
        page= response.css('a.next-arrow::attr(href)').get()
        yield scrapy.Request(
            response.urljoin(page),
            callback=self.parse_category
        )
    
    def parse_new(self, response):
        title = response.css('article h1::text').get()
        date = ' '.join(response.css('.publish-date::text').get().split())
        quotes = response.css('article blockquote')
        
        for quote in quotes:
            quote_text = quote.css('::text').get()
            status = quote.xpath('./preceding-sibling::p/img/@data-image-id').get()
            yield {
                'title':title,
                'date': date,
                'quote-text': quote_text,
                'status': status,
                'url': response.url
            }