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
            
       
       
            result = self.client.get(url = user.url).text

        #  BeautifulSoup-object en geef de parser op
            soup = BeautifulSoup(result, 'html.parser')

        # Extract alle tekst
            all_text = soup.get_text(separator='\n')

        # sla gescrapte gegevens op in de database
            self.scraper_repository.add_scraper({"content": all_text})

            return all_text

       except Exception as e:
         pass
       