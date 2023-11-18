from pydantic import BaseModel
from pymongo import MongoClient



class Scraper(BaseModel):
    url: str
    xpath: str
    name: str
    value: str


if __name__ == '__main__':
    #Maak een nieuwe client aan met de url en port
    mongo_client = MongoClient('mongodb://root:example@localhost', 27017)

    #Maak een nieuwe database aan met de naam my_scraper
    db = mongo_client.get_database('my_scraper')

    #Instantieer een nieuwe class met de constructor
    scraper = Scraper(
        url="https://www.google.com",
        xpath="//div[@id='hplogo']/a/@href",
        name="google",
        value="Google"
    )

    #Sla de scraper op in de database {"url":"https://www.google.com","xpath":"//div[@id='hplogo']/a/@href","name":"google","value":"Google"}
    db.get_collection("scraper").insert_one(scraper.dict())

    #Haal de scraper op uit de database met de naam google
    scraper = db.get_collection("scraper").find_one({"name": "google"})

    #Instantieer een nieuwe class met de constructor
    # scraper = Scraper(name=scraper.get('name'), value=scraper.get('value'), xpath=scraper.get('xpath'), url=scraper.get('url'))

    #Instantieer een nieuwe class met the spread operater **
    scraper = Scraper(**scraper)
    print(scraper.url, scraper.xpath, scraper.name, scraper.value)

    #Haal alle scrapers op uit de database
    db.get_collection("scraper").delete_one({"name": "google"})

    #Update de scraper met de naam google naar google2
    db.get_collection("scraper").update_one({"name": "google"}, {"$set": {"name": "google3"}})

    
