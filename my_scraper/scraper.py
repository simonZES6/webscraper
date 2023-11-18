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
    _name: str
    _email: str
    _password: str
    _url: str
   
    def get_name(self):
            return self._name
    def get_email(self,email:_email):
            if not email:
                raise ValueError("Invalid email address")
            email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if not re.fullmatch(email_regex, email):
                raise ValueError("Invalid email address")
            return self._email
           
    def get_password(self):
            return self._password
    def get_url(self,url:_url):
           if not url:
                 raise ValueError("Incomplete url address")
           parsed_url = urlparse(url)
           if parsed_url.scheme and parsed_url.netloc:
                if not any(url.lower().endswith(i) for i in ['.docx', '.pdf', '.mp4', '.mp3']):
                 raise ValueError("Invalid url address")
                return self._url
    def set_name(self, name):
            self._name = name
    def set_email(self, email):
            self._email = email
    def set_password(self, password):
            self._password = password
    def set_url(self, url):
            self._url = url


class ScraperController:
    
    def __init__(self, scraper: Scraper,scraper_repository: ScraperRepository,webspider: WebSpider):
        self.scraper = scraper
        self.webspider = webspider
        self.scraper_repository = scraper_repository
        self.scheduler = BackgroundScheduler()
      
    def scrape(self):
          scraper_data = {
              "name": self.scraper.get_name(),
              "email": self.scraper.get_email(),
              "password": self.scraper.get_password(),
              "url": self.scraper.get_url(),
          }
          self.scraper_repository.add_scraper(scraper_data)
          result = self.webspider.start_request(self.scraper.get_url())
          user_timezone = pytz.timezone('south_america/paramaribo')
          scheduled_time = datetime.now(user_timezone).replace(hour=12, minute=0, second=0, microsecond=0)
          if scheduled_time < datetime.now(user_timezone):
              scheduled_time += timedelta(days=1)
          self.scheduler.add_job(
                self.webspider_results,
                trigger="cron",
                args=[self.scraper_repository],
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
         
                 
   