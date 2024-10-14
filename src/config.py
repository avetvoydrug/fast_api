from dotenv import load_dotenv
import os

load_dotenv()

#database
DB_HOST= os.environ.get("DB_HOST")
DB_PORT= os.environ.get("DB_PORT")
DB_NAME= os.environ.get("DB_NAME")
DB_USER= os.environ.get("DB_USER")
DB_PASS= os.environ.get("DB_PASS")

DB_HOST_TEST= os.environ.get("DB_HOST_TEST")
DB_PORT_TEST= os.environ.get("DB_PORT_TEST")
DB_NAME_TEST= os.environ.get("DB_NAME_TEST")
DB_USER_TEST= os.environ.get("DB_USER_TEST")
DB_PASS_TEST= os.environ.get("DB_PASS_TEST")

#Redis
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

#Auth
SECRET_AUTH = os.environ.get("SECRET_AUTH")
TOKEN_AUDIENCE = os.environ.get("TOKEN_AUDIENCE")
TOKEN_ALGORITHM = os.environ.get("TOKEN_ALGORITHM")
VERIFY_TOKEN_AUDIENCE = os.environ.get("VERIFY_TOKEN_AUDIENCE")

#OAuth
GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

#celery e-mail sender
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")