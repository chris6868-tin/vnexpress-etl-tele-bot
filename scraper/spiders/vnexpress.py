import scrapy


class VnexpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net"]

    def parse(self, response):
        links = response.css('h3.title-news a::attr(href)').getall()
                
        for link in links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(url=absolute_url, callback=self.parse_detail)
    
    def parse_detail(self, response):
        title = response.css('h1.title-detail::text').get()

        paragraphs = response.css('article.fck_detail p.Normal::text').getall()
        publish_date=response.css('span.date::text').get()
        full_text = " ".join(paragraphs).strip()

        if title and full_text:
            yield {
                'title': title.strip(),
                'date': publish_date,
                'url': response.url,
                'content': full_text
            }