import logging
from fastapi import HTTPException
from pymongo import MongoClient


class ScraperRepository:
    def __init__(self,db_name,db_url):
        try:
            self.db = MongoClient(db_url)[db_name]
        except Exception as e:
            logging.error("Error: db not found")
            raise HTTPException(status_code=500, detail="db not found")
      
        

        

    def add_scraper(self, scraper_data):
      
        self.db["scrapers"].insert_one(scraper_data)
           
       
        