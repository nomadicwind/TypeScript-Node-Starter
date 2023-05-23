import scrapy


class HNDailySpider(scrapy.Spider):
    name = "hndaily"

    def start_requests(self):
        urls = ["https://www.daemonology.net/hn-daily/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        print(page)
