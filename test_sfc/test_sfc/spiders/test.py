import scrapy


class TestSpider(scrapy.Spider):

    name = 'test'
    start_url = 'https://trud.ua/jobs/list/q/{}/filter_show/state.html'
    start_urls = []

    def start_requests(self):
        keywords = ['python', 'java', 'водитель']
        for keyword in keywords:
            url = self.start_url.format(keyword)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        blocks = response.css('.result-unit')
        for block in blocks:
            table_block = block.css('div.table-view')
            title_block = block.css('div.titl-r')

            data = {
                'title': title_block.css('a::text').get(),
                'uploaded_date': table_block.css('div.date::text').get(),
                'company_url': table_block.css('div.institution a').attrib['href']
            }
            yield data

        all_pages = response.css('.page').css('a')
        yield from response.follow_all(all_pages, callback=self.parse)


