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

    summ = {'$$app_token': secret_token,
                'physician_profile_id': physician_profile_id,
            }

    response = requests.get("https://openpaymentsdata.cms.gov/resource/tf25-5jad.json", params=summ)
    search_results = response.json()
    t = module.total_payments(search_results)
    first_name = search_results[0]['physician_first_name']
    last_name = search_results[0]['physician_last_name']
    perso_doc_info = module.perso_doc_info(search_results)
    pay_breakdown = module.pay_per_comp(search_results)
    # List of tuple ; tuple = (pharmacy name, total):
    top_pharm = module.pay_per_comp_filtered(pay_breakdown,t)

    # Entering in session what I am going to need later:
    session['info_doc'] = perso_doc_info
    session['info_doc']['total_received'] = round(t)
    session['pay_breakdown'] = top_pharm
    session['doc_chart_pharm'] = module.tuplelist_to_listfirstitem(top_pharm)
    session['doc_chart_payment'] = module.tuplelist_to_listseconditem(top_pharm)
  
    top_pharm_dic_no_other = top_pharm
    top_pharm_dic_no_other.pop()
    session['listsamecompanies'] = module.tuplelist_to_listfirstitem(top_pharm_dic_no_other)
    session['doc_payments_no_other']=module.tuplelist_to_listseconditem(top_pharm_dic_no_other)
    
    print '************ top pharm'
    print top_pharm

    print '************ List comp'
    print session['listsamecompanies']

    print '************ List value doc spec'
    print session['doc_payments_no_other']


    return render_template("summary.html", 
        perso_doc_info = perso_doc_info, pay_breakdown=top_pharm, first_name=
        first_name, last_name=last_name, p_id= physician_profile_id)

@app.route("/ind_comparison/<int:physician_profile_id>/<specialty>/<state>")
def ind_comparison(physician_profile_id, specialty, state):
    """Show payments received by doctor in comparison to payments received by 
    all doctors of the same specialty"""
    
    summ = {'$$app_token': secret_token,
            'physician_specialty': specialty,
            'recipient_state': state
            }
    response = requests.get("https://openpaymentsdata.cms.gov/resource/tf25-5jad.json", params=summ, stream=True)
    all_payments = module.results_per_spe(response)
    avg_per_state = module.averg_per_state(all_payments)
    avg_pharm = module.averg_per_company(all_payments) #dictionnary with key: pharmacy, value: avg payed doc for specific specialty & state
    avg_pharm_match_doc = module.averg_ind_comp_doc(avg_pharm, session['pay_breakdown'])
    session['doc_comp'] = module.list_tup_to_dic(session['pay_breakdown'])
    session['bar_chart'] = module.bar_chart_dic(session['doc_comp'],avg_pharm_match_doc)
    session['pharm_avg'] = module.pharm_avg_sortedlist(avg_pharm_match_doc)
    print '************ Value of companies for all doctors'
    print session['pharm_avg']
    print '************'
    return render_template('ind_comparison.html', avg_per_state=avg_per_state, 
        avg_pharm=avg_pharm, avg_pharm_ind_doc=avg_pharm_match_doc)

@app.route('/payment_type')
def payment():
    """For each payment made to the doctor by company X, show the payment type 
    and weight over total  """
    pass 
    return render_template('payment_type.html')

@app.route('/doctor_like')
def doctor_like():
    pass
    return render_template("doctor_like.html")



@app.route('/doc_info.json')
def payment_doc():
    """Return data about payments received by doctor per each company."""

# Be careful here , formatted for only 5 companies
    data_dict = {
                "labels":  session['doc_chart_pharm'],
                "datasets": [
                    {
                        "data": session['doc_chart_payment'],
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56",
                            "#02c8a7",
                            "#552847"
                        ],
                        "hoverBackgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56",
                            "#02c8a7",
                            "#552847"
                        ]
                
                    }]
            }

    return jsonify(data_dict)

            
@app.route("/ind_info.json")
def payment_ind_doc():
    """Return data about average payments made by each company to same specialty of doc 
    versus payment receievd by specific doctor of same specialty."""
   
    data_dict = {
                "labels": session['listsamecompanies'],
                "datasets":[
                    {
                        "label": "Payments Received by this specific Doctor",
                        "data": session['doc_payments_no_other'],
                        "borderColor": '#00FF00',
                        "borderWidth": 2,
                        "stack": 1,
                        "backgroundColor": "rgba(99,255,132,0.2)"
                        
                
                    },
                    {
                        "label": "Average Payments spent on this Specialty per Doctor",
                        "data": session['pharm_avg'],
                        "borderColor": '#00FF00',
                        "borderWidth": 2,
                        "stack": 2,
                        "backgroundColor": "rgba(255,99,132,0.2)"
                        
                
                    }]
                }
    return jsonify(data_dict)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host="0.0.0.0")
