from fastapi import FastAPI

from my_scraper.repositories.scraper_repositorie import ScraperRepository
from my_scraper.views.scraper_views import router as scrape_router

app = FastAPI()


app.include_router(scrape_router)




