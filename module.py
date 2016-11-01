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
import server

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




def print_nicely_results(list_results):
    """Fname Lname of results."""
    pprint(list_results)

def unique_id(list_results):
    """ Takes in list of dictionnaries and return list of dict with only unique ids of doctor """
    new_list = []
    for dico in list_results:
        if int(dico['physician_profile_id']) in new_list:
            list_results.remove(dico)
            # del list_results[i]
        else:
            new_list.append(int(dico['physician_profile_id']))
    return list_results
     

def unique_dico(list_results):
    """ xxxx """
    id_list = []
    new_list = []
    for dico in list_results:
        if int(dico['physician_profile_id']) in id_list:
            print "enter"
            pass
            # del list_results[i]
        else:
            id_list.append(int(dico['physician_profile_id']))
            new_list.append(dico)
            print id_list
           
    return new_list
     




