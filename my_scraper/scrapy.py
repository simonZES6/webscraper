from pydantic import BaseModel
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from my_scraper.database import ScraperRepository

class WebSpider(BaseModel):
    web_name : str
    
    text : str
    def start_request(self,url:str):
        yield scrapy.Request(url=url, callback=self.response_parse, cb_kwargs={'web_name': self.web_name})
    
    def response_parse(self, response, web_name):
        for selector in response.html.xpath("//div[@class='a-section a-spacing-small a-spacing-top-small']"):
            yield {
                'web_name': web_name,
                'name': selector.xpath("//span[@class='a-size-base-plus a-color-base a-text-normal']/text()").get(),
                'url': selector.xpath("//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']/@href").get(),
                'text': selector.xpath("//span[@class='a-size-base a-color-secondary']/text()").get(),
            }
        next_page_link = response.html.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href").get()
        if next_page_link:
            next_page_url = response.urljoin(next_page_link)
            yield scrapy.Request(url=next_page_url, callback=self.response_parse)

def web_spider_results(scraper_repository: ScraperRepository):
  

    def crawler_results(item):
        scraper_repository.add_scraper(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(WebSpider,url = scraper_repository.get_url("webscraper"))
    crawler_process.start()
    crawler_process.join()
    return scraper_repository


