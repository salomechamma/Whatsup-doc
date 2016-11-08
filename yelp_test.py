"""What's up Doc"""

import os
import module
from jinja2 import StrictUndefined

from flask import jsonify
from flask import (Flask, render_template, redirect, request, flash,
                   session)
import requests
import json

from flask_debugtoolbar import DebugToolbarExtension
# ***************************** Import on SERVER.PY:
from yelp.client import Client 
import io


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC" 
 # session 

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


# extract from secret.sh
# secret_token = os.environ["DOC_APP_TOKEN"]
client_id = os.environ["YELP_APP_ID"]
client_secret = os.environ["YELP_APP_SECRET"]
url_yelp='https://api.yelp.com/oauth2/token'
data_yelp ={'grand_type': 'client_credentials',
    'client_id': client_id, 'client_secret': client_secret}
r = requests.post(url_yelp, data = data_yelp)

yelp_access_token = r.json()['access_token']

yelp_search_url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'Bearer ' + yelp_access_token}
params = {
    'term': 'JOHN SMITH',
    'location':  '08865, PHILLIPSBURG',
    'categories': 'health'

   }
result = requests.get(url=yelp_search_url, params=params, headers=headers)

print result.json()['total']
business_name = result.json()['businesses'][0]['name']
rating = result.json()['businesses'][0]['rating']
if (session['info_doc']['first_name'] not in business_name) or (session['info_doc']['last_name'] not in business_name):
    rating = -1

# @app.route('/')
# def index():
#     """Homepage."""

#     p_id = 49877
#     # parameter including app_secret
#     payload = {'$$app_token': secret_token,
#                 'physician_profile_id': p_id}

#     response = requests.get("https://openpaymentsdata.cms.gov/resource/tf25-5jad.json", params=payload)
#     # import pdb; pdb.set_trace()
#     # response = "https://openpaymentsdata.cms.gov/resource/tf25-5jad.json?$$app_token=secret_token&physician_profile_id=49877"
#     response = response.json()
    
#     return render_template('homepage.html', response=response)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host="0.0.0.0")
