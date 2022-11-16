'''All configuration data needed in project'''

import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN', 'summy-dummy-token')

CHAT_ID_MODERATE = int(os.environ.get('CHAT_ID_MODERATE', '000'))

DBI_URI = os.environ.get('DBI_URI', 'summy-uri')
DB_TABLE_NAME = os.environ.get('DB_TABLE_NAME', 'summy-tale')
