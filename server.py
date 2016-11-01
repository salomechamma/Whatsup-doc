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



@app.route('/')
def index():
    """Homepage."""

    p_id = 49877
    # parameter including app_secret
    payload = {'$$app_token': secret_token,
                'physician_profile_id': p_id}

    response = requests.get("https://openpaymentsdata.cms.gov/resource/tf25-5jad.json", params=payload)
    # import pdb; pdb.set_trace()
    # response = "https://openpaymentsdata.cms.gov/resource/tf25-5jad.json?$$app_token=secret_token&physician_profile_id=49877"
    response = response.json()
    
    return render_template('homepage.html', response=response)

@app.route("/results_list")
def results_list():
    """Show list of doctor resulting from search."""
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    data = {'$$app_token': secret_token,
                'physician_first_name': firstname,
                'physician_last_name': lastname}

    response = requests.get("https://openpaymentsdata.cms.gov/resource/tf25-5jad.json", params=data)
    search_results = response.json()
    # to keep only unique id of doctor so no duplicates in list of results:
    search_results = module.unique_dico(search_results)

    return render_template('results_list.html', search_results=search_results)

@app.route("/doc_summary/<int:physician_profile_id>")
def summary(physician_profile_id):
    """Show summary page on doctor resulting from search."""
    return render_template("summary.html", p_id=physician_profile_id)

@app.route('/ind_comparison')
def ind_comparison():
    """Show payments received by doctor in comparison to payments received by 
    all doctors of the same specialty"""
    pass
    return render_template("ind_comparison.html")

@app.route('/payment_type')
def payment():
    """For each payment made to the doctor by company X, show the payment type 
    and weight over total  """
    pass 
    return render_template('payment_type.html')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host="0.0.0.0")
