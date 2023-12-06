import re
from urllib.parse import urlparse
from pydantic import BaseModel
from my_scraper.database import ScraperRepository
from my_scraper.scrapy import WebSpider
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
  

    def __init__(self, scraper: Scraper,scraper_repository: ScraperRepository,webspider: WebSpider):
        self.scraper = scraper
        self.webspider = webspider
        self.scraper_repository = scraper_repository
        self.scheduler = BackgroundScheduler()
      
    def scrape(self):
          scraper_data = {
              "name": self.scraper.name,
              "email": self.scraper.email,
              "password": self.scraper.password,
              "url": self.scraper.url,
          }
          self.scraper_repository.add_scraper(scraper_data)
          result = self.webspider.start_request(self.scraper.url)
          
          if not self.scheduler.running:
            user_timezone = pytz.timezone('america/paramaribo')
            scheduled_time = datetime.now(user_timezone).replace(hour=12, minute=0, second=0, microsecond=0)
            if scheduled_time < datetime.now(user_timezone):
              scheduled_time += timedelta(days=1)
          
          self.scheduler.add_job(
                self.webspider.start_request,
                trigger="cron",
                args=[self.scraper.url],
                year = scheduled_time.year,
                month = scheduled_time.month,
                day = scheduled_time.day,
                hour = scheduled_time.hour,     
                minute = scheduled_time.minute,
                second = scheduled_time.second,
                timezone = user_timezone,

          )
          self.scheduler.start()
          

          if result == "scrapin_complete":
                 email_subject = "scrapin complete"
                 email_body = "The scrapin process is complete"
                 self.send_email(self.scraper.get_email(),email_subject, email_body)
              

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

         
                 
  