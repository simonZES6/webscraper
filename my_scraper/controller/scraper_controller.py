import logging
from urllib.parse import urlparse
from fastapi import HTTPException
from scraper_api import ScraperAPIClient
from bs4 import BeautifulSoup
from my_scraper.models.user import User
from my_scraper.repositories.scraper_repositorie import ScraperRepository


class ScraperController:
    def __init__(self, scraper_repository:ScraperRepository,client:ScraperAPIClient):
        self.scraper_repository = scraper_repository
        
        self.client = client
        

    def scrape_website(self,user:User):
       try:
        url_str = str(user.url)
        if not url_str.startswith("http://") and not url_str.startswith("https://"):
                raise HTTPException(status_code=400, detail="Invalid url address")
                    
        result = self.client.get(url=user.url).text


        #  BeautifulSoup-object en geef de parser op
        soup = BeautifulSoup(result, 'html.parser')

        
        # Extract alle tekst
        all_text = soup.get_text(separator=' ').strip()
        all_text = ' '.join(all_text.split())  # Verwijder overtollige spaties

        formatted_text = "Gescrapte inhoud van {url}:{content}".format(url=user.url, content=all_text)

        
        # sla gescrapte gegevens op in de database
        self.scraper_repository.add_scraper({"content": all_text})

        return formatted_text
       
       except Exception as se:
            # Afhandeling voor specifieke scraper uitzonderingen
            logging.error(se)
            raise HTTPException(status_code=500, detail="Scraper not inserted")
          