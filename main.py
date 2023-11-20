from fastapi import FastAPI
from my_scraper.database import ScraperRepository
from my_scraper.scraper import Scraper,ScraperController
from my_scraper.scrapy import WebSpider


app = FastAPI()
scraper_repository = ScraperRepository(db_name = "my_scraper",db_url="mongodb://localhost:27017")
controller = ScraperController(scraper=Scraper(),scraper_repository=scraper_repository,webspider=WebSpider())
@app.post("/scrape")
def scrape(scraper: Scraper):
    return controller.scrape(scraper)



#scraper_controller = ScraperRepository()
#@app.delete("/database")
#def delete_scraper(name: str):
#    return scraper_controller.soft_delete(name)
#@app.get("/database")
#def get_all_scrapers():
#    return scraper_controller.get_all_scrapers()
#@app.get("/database/{name}")
#def get_scraper(name: str):
#    return scraper_controller.get_scraper(name)
#
#@app.put("/database")
#def update(scraper: Scraper):
#        return scraper_controller.update_scraper(scraper) 
#
