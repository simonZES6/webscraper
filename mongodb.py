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

    class Spider(BaseModel):
    
   
        client = ScraperAPIClient('f27e7da6e8592cd57a6766518b276625')
        result = client.get(url = 'https://codedealers.nl/').text


# Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(self.result,'html.parser')

# Extract all text
        all_text = soup.get_text(separator='\n')
        return all_text
  
client = ScraperAPIClient('f27e7da6e8592cd57a6766518b276625')
result = client.get(url = 'https://codedealers.nl/').text


# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(result,'html.parser')

# Extract all text
all_text = soup.get_text(separator='\n')
print(all_text)


import re
from urllib.parse import urlparse
from pydantic import BaseModel
from my_scraper.database import ScraperRepository
from my_scraper.scrapy import Spider
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta,timezone
import pytz


class Scraper(BaseModel):
    name: str = "default_name"   
    email: str
    password: str
    url: str
   
    def get_name(self):
            return self.name
    def get_email(self):
            return self.email
           
           
    def get_password(self):
            return self.password
    def get_url(self,url:str):
           if not url:
                 raise ValueError("Incomplete url address")
           parsed_url = urlparse(url)
           if not (parsed_url.scheme and parsed_url.netloc) or self.url.lower().endswith() (('.doc', '.docx', '.pdf', '.mp4', '.mp3')):
                 raise ValueError("Invalid url address")
           return self.url
    def set_name(self, name):
            self.name = name
    def set_email(self, email):
            self.email = email
    def set_password(self, password):
            self.password = password
    def set_url(self, url):
            self.url = url
    
    def validate_url(self, url):
        if not url:
            raise ValueError("Incomplete url address")
        parsed_url = urlparse(url)
        if not (parsed_url.scheme and parsed_url.netloc) or self.url.lower().endswith(('.doc', '.docx', '.pdf', '.mp4', '.mp3')):
            raise ValueError("Invalid url address")


class ScraperController:
  

    def __init__(self, scraper: Scraper,scraper_repository: ScraperRepository,spider:Spider ):
        self.scraper = scraper
        self.spider = spider
        self.scraper_repository = scraper_repository
        self.scheduler = BackgroundScheduler()
      
    def scrape(self):
      
          
          
          result = self.spider.scrape_and_save(self.scraper_repository)
         
        
          
          
         #if not self.scheduler.running:
         #  user_timezone = pytz.timezone('america/paramaribo')
         #  scheduled_time = datetime.now(user_timezone).replace(hour=12, minute=0, second=0, microsecond=0)
         #  if scheduled_time < datetime.now(user_timezone):
         #    scheduled_time += timedelta(days=1)
         #
         #self.scheduler.add_job(
         #      self.webspider.start_request,
         #      trigger="cron",
         #      args=[self.scraper.url],
         #      year = scheduled_time.year,
         #      month = scheduled_time.month,
         #      day = scheduled_time.day,
         #      hour = scheduled_time.hour,     
         #      minute = scheduled_time.minute,
         #      second = scheduled_time.second,
         #      timezone = user_timezone,

         #)
         #self.scheduler.start()
         #

         #if result == "scrapin_complete":
         #       email_subject = "scrapin complete"
         #       email_body = "The scrapin process is complete"
         #       self.send_email(self.scraper.get_email(),email_subject, email_body)
         #    

    def send_email(self, email, email_subject, email_body):
        email_sender = self.scraper.get_email()
        email_password = self.scraper.get_password()
        email_receiver = email
        subject = email_subject
        body = email_body
        em = MIMEMultipart()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.attach(MIMEText(body, 'plain'))
        text = em.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, text)
        server.quit()

         


         from pydantic import BaseModel
from scraper_api import ScraperAPIClient
from bs4 import BeautifulSoup
from my_scraper.database import ScraperRepository


class Spider(BaseModel):
    api_key: str
    

    @property
    def client(self):
        return ScraperAPIClient(self.api_key)

    def scrape_and_save(self, repository: ScraperRepository):
        try:
       
            result = self.client.get(url='https://www.wikipedia.org/').text

        #  BeautifulSoup-object en geef de parser op
            soup = BeautifulSoup(result, 'html.parser')

        # Extract alle tekst
            all_text = soup.get_text(separator='\n')

        # sla gescrapte gegevens op in de database
            repository.add_scraper({"content": all_text})

            return all_text

        except Exception as e:
         pass

#instantie van Spider
#spider_instance = Spider(api_key='f27e7da6e8592cd57a6766518b276625')

# instantie van ScraperRepository
#repository_instance = ScraperRepository(db_name="my_scraper", db_url='mongodb://root:example@localhost:27017')

# Roep de scrape_and_save functie aan met de Spider en Repository
#result =spider_instance.scrape_and_save(repository=repository_instance)

                 
  