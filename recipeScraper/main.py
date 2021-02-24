from matprat import MatpratScraper
from emailreader import EmailReader
import sys
import settings as settings


settings.load_settings()

matprat = MatpratScraper()
emailReader = EmailReader()

#website, url = emailReader.readMessages()
#if website == "matprat":
 #   matprat.scrape(url)

def main(argv):
    matprat.scrape(argv[0])


if __name__ == "__main__":
   main(sys.argv[1:])
