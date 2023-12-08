# scraper_views.py

from fastapi import APIRouter, Depends
from my_scraper.models.user import User
from my_scraper.controller.scraper_controller import ScraperController
from dependencies import get_db, get_client

scraper_controller = ScraperController(scraper_repository=get_db(),client=get_client())
router = APIRouter(
    prefix="/scraper",
    tags=["Scraper"],
    responses={404: {"description": "Not found"}, 500: {"description": "Internal Server Error"}, 
               400: {"description": "Bad Request"}, 401: {"description": "Unauthorized"}},

)

@router.post("/scrape")
def scrape(user: User):
    return scraper_controller.scrape_website(user)
