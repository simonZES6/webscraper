from pymongo import MongoClient


class ScraperRepository:
    def __init__(self,db_name,db_url):
        self.db_name = db_name
        self.db_url = db_url
        self.client = MongoClient(self.db_url)
        self.db = self.client[self.db_name]
        
    def add_scraper(self, scraper_data):
        self.db["scrapers"].insert_one(scraper_data)
        
    def get_scraper(self, name):
        return self.db["scrapers"].find_one({"name": name})
    def get_url(self, name):
       scraper_data = self.get_scraper(name)
       if scraper_data:
        return scraper_data
    