import os
import requests

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_DEFAULT_SENDER = 'whatsup.doctor.website@gmail.com'
MAIL_USERNAME = 'whatsup.doctor.website@gmail.com'
email_passw = os.os.getenv("EMAIL_PASSWORD")
MAIL_PASSWORD = os.environ.get("HEROKU_EMAIL_PASSWORD", email_passw)
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# Required to use Flask sessions and the debug toolbar
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "ABC")

# Government API /extract from secret.sh
doc_app_token = os.getenv['DOC_APP_TOKEN3']
SECRET_TOKEN = os.environ.get("DOC_APP_TOKEN", doc_app_token)
# GOOGLE_KEY = os.environ["GOOGLE_KEY"]
google_key = os.getenv["GOOGLE_KEY"]
GOOGLE_KEY = os.environ.get("HEROKU_GOOGLE_KEY",google_key)

# Yelp API
# CLIENT_ID = os.environ["YELP_APP_ID"]
yelp_app_id = os.getenv["YELP_APP_ID"]
CLIENT_ID = os.environ.get("HEROKU_YELP_APP_ID",yelp_app_id)
CLIENT_SECRET = os.environ["YELP_APP_SECRET"]
yelp_app_secret = os.getenv["YELP_APP_SECRET"]
CLIENT_SECRET = os.environ.get("HEROKU_YELP_APP_SECRET",yelp_app_secret)
url_yelp='https://api.yelp.com/oauth2/token'
data_yelp ={'grand_type': 'client_credentials',
    'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
r = requests.post(url_yelp, data = data_yelp)

YELP_ACCESS_TOKEN = r.json()['access_token']
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'Bearer ' + YELP_ACCESS_TOKEN}
# no need to put in upper case things i dont need in the server like'r'
# like yelp and data yelp
