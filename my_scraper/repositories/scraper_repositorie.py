from pymongo import MongoClient


class ScraperRepository:
    def __init__(self,db_name,db_url):
        try:
            self.db = MongoClient(db_url)[db_name]
        except Exception as e:
            print("Error: db not found")
      
        

        

    def add_scraper(self, scraper_data):
        try:
            self.db["scrapers"].insert_one(scraper_data)
        except Exception as e:
            print("Error: scraper not inserted")       
        self.db["scrapers"].insert_one(scraper_data)
        