import os
import requests

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_DEFAULT_SENDER = 'whatsup.doctor.website@gmail.com'
MAIL_USERNAME = 'whatsup.doctor.website@gmail.com'
MAIL_PASSWORD = os.environ["EMAIL_PASSWORD"] 
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# Required to use Flask sessions and the debug toolbar
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "ABC")

# Government API /extract from secret.sh
docapptoken = os.environ['DOC_APP_TOKEN3']
SECRET_TOKEN = os.environ.get("DOC_APP_TOKEN", docapptoken)
GOOGLE_KEY = os.environ["GOOGLE_KEY"]

# Yelp API
CLIENT_ID = os.environ["YELP_APP_ID"]
CLIENT_SECRET = os.environ["YELP_APP_SECRET"]
url_yelp='https://api.yelp.com/oauth2/token'
data_yelp ={'grand_type': 'client_credentials',
    'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
r = requests.post(url_yelp, data = data_yelp)

YELP_ACCESS_TOKEN = r.json()['access_token']
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'Bearer ' + YELP_ACCESS_TOKEN}
# no need to put in upper case things i dont need in the server like'r'
# like yelp and data yelp
