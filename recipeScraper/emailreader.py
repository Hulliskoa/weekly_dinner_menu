import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from imap_tools import MailBox, AND
#https://github.com/ikvk/imap_tools#email-attributes

class EmailReader:

    def readMessages(self):
        with MailBox('imap.gmail.com').login(os.getenv("USER"), os.getenv("PASSWORD")) as mailbox:
            for msg in mailbox.fetch(AND(seen=False)):
                print(msg)
                code = msg.subject.split(":", 1)
                if code[0].lower() == "matprat":
                    print("matprat")
                    return code[0].lower(),  code[1]
                else:
                    return "none"

