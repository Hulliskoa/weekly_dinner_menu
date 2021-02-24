from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os
from smtplib import SMTP
import math
import pandas as pd
sys.path.insert(1, '../')

import settings as settings
settings.load_settings()

class EmailSender:

    def __init__(self):
        self.env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

    def __get_contacts(self, filename):
        names = []
        emails = []
        with open(filename, mode='r', encoding='utf-8') as contacts_file:
            for a_contact in contacts_file:
                names.append(a_contact.split()[0])
                emails.append(a_contact.split()[1])
        return names, emails

    def __send_mail(self, bodyContent, toEmail):
        to_email = toEmail
        from_email = os.getenv("USER")
        subject = 'Ukens oppskrifter!'

        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = from_email
        message['To'] = to_email

        message.attach(MIMEText(bodyContent, "html"))
        msgBody = message.as_string()

        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, os.getenv("PASSWORD"))
        server.sendmail(from_email, to_email, msgBody)
        server.quit()

    def createEmail(self, recipes, shoppingList, basic, serves):
        recipesJson = recipes

        template = self.env.get_template('child.html')

        categories = pd.read_excel("../Oppskrifter.xlsx", 'sorted')
        categories = categories.set_index('sorted-categories')
        categories = categories.to_dict()

        print(categories)
        output = template.render(recipes=recipes[0], shoppingList = shoppingList, basic = basic, unicode = categories["unicode"], serves = serves, math=math)
        names, emails = self.__get_contacts('../mycontacts.txt')
        for name, email in zip(names, emails):
            self.__send_mail(output, email)

        return "Mails sent successfully."
