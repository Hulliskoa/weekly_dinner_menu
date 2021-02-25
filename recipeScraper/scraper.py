

from .matprat import MatpratScraper
from .emailReader import EmailReader
import sys
sys.path.insert(1, '../')
import settings as settings
settings.load_settings()


class RecipeScraper:
    def __init__(self):
        self.matprat = MatpratScraper()
        self.emailReader = EmailReader()

    def readNewEmails(self):
        try:
            website, url = self.emailReader.readMessages()
            if website == "matprat":
                self.matprat.scrape(url)
        except:
            print("No new messages")
