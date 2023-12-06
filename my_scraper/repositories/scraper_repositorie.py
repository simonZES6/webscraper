from pymongo import MongoClient


class ScraperRepository:
    def __init__(self,db_name,db_url):
        self.db = MongoClient(db_url)[db_name]
        

        

    def add_scraper(self, scraper_data):
                   
        self.db["scrapers"].insert_one(scraper_data)
        