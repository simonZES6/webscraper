# scraper_views.py

from fastapi import APIRouter, Depends
from my_scraper.models.user import User
from my_scraper.controller.scraper_controller import ScraperController
from dependencies import get_db, get_client

scraper_controller = ScraperController(scraper_repository=get_db(),client=get_client())
router = APIRouter(
    prefix="/scraper",
    tags=["Scraper"],
    responses={404: {"description": "Not found"}},
)

@router.post("/scrape")
def scrape(user: User, db=Depends(get_db), client=Depends(get_client)):
    return scraper_controller.scrape_website(user, db, client)
