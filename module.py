"""Module including all functions called by server.py in each routes"""

import os
from jinja2 import StrictUndefined

from flask import jsonify
from flask import (Flask, render_template, redirect, request, flash,
                   session)
import requests
from sys import argv
from pprint import pprint
import json

from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC" 
 # session 

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


# extract from secret.sh
secret_token = os.environ["DOC_APP_TOKEN"]

# No need:
# headers = {"Host": "data.seattle.gov",
#           "Accept": "application/json",
#           "X-App-Token": secret_token}




def print_nicely_results(dic_results):
    """Fname Lname of results."""
    pprint(dic_results)
 
     






