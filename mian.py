from fastapi import FastAPI
from my_scraper.database import ScraperRepository
from my_scraper.scraper import Scraper, ScraperController


app = FastAPI()

controller = ScraperController()
@app.post("/scrape")
async def scrape(scraper: Scraper):
    return controller.scrape(scraper)
