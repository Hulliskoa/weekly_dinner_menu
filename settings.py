# settings.py
from dotenv import load_dotenv
import os

def load_settings():
    load_dotenv()

# OR, explicitly providing path to '.env'
#from pathlib import Path  # Python 3.6+ only
#env_path = Path('.') / '.env'
#load_dotenv(dotenv_path=env_path)
