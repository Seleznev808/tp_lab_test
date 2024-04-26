import os

from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('TOKEN')

SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR')
SCREENSHOT_SIZE = {
    'width': int(os.getenv('SCREENSHOT_WIDTH')),
    'height': int(os.getenv('SCREENSHOT_HEIGHT'))
}
SCREENSHOT_TIMEOUT = int(os.getenv('SCREENSHOT_TIMEOUT'))
SCREENSHOT_SLEEP = float(os.getenv('SCREENSHOT_SLEEP'))

EXECUTION_TIME_ROUND = int(os.getenv('EXECUTION_TIME_ROUND'))

DATE_FORMAT = os.getenv('DATE_FORMAT')

DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE')

URL_WHOIS = os.getenv('URL_WHOIS')
WHOIS_FIELDS = os.getenv('WHOIS_FIELDS')

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
