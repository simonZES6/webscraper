# dependencies.py

from fastapi import Depends
from my_scraper.repositories.scraper_repositorie import ScraperRepository
from scraper_api import ScraperAPIClient

def get_db():
    return ScraperRepository(db_name="my_scraper", db_url='mongodb://root:example@localhost:27017')

def get_client():
    return ScraperAPIClient(api_key="f27e7da6e8592cd57a6766518b276625")
