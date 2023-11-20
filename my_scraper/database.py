
import datetime
from pymongo import MongoClient


class ScraperRepository:
    def __init__(self,db_name,db_url):
        self.db_name = db_name
        self.db_url = db_url
        self.client = MongoClient(self.db_url)
        self.db = self.client[self.db_name]
        
    def add_scraper(self, scraper_data):
        scraper_data['deleted'] = False
        scraper_data['deleted_at'] = None             
        self.db["scrapers"].insert_one(scraper_data)
        
    def get_scraper(self, name):
        return self.db["scrapers"].find_one({"name": name, "deleted": False})
    
    def get_url(self, name):
       scraper_data = self.get_scraper(name)
       if scraper_data:
        return scraper_data
    
    def soft_delete(self,name):
       scraper_data = self.get_scraper(name)
       if scraper_data:
          scraper_data['deleted'] = True
          scraper_data['deleted_at'] = datetime.utcnow()
          self.db["scrapers"].update_one({"_id": scraper_data["_id"]}, {"$set": scraper_data})
       return scraper_data
    
    def get_all_scrapers(self,include_soft_deleted=True):
        if include_soft_deleted:
            return self.db["scrapers"].find()
        else:
            return self.db["scrapers"].find({"deleted": False})
       
    def get_soft_deleted(self):
        return self.db["scrapers"].find({"deleted": True})

    def update_scraper(self, scraper_data):
        self.db["scrapers"].update_one({"_id": scraper_data["_id"]}, {"$set": scraper_data})
        return scraper_data

   
    