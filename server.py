"""What's up Doc"""

import os
import module
from jinja2 import StrictUndefined

from flask import jsonify
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension
import requests
import json
from model import connect_to_db, db, User, Doctor, Like

# ***************************** To use Yelp API:
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


# Government API /extract from secret.sh
secret_token = os.environ["DOC_APP_TOKEN"]

# Yelp API
client_id = os.environ["YELP_APP_ID"]
client_secret = os.environ["YELP_APP_SECRET"]
url_yelp='https://api.yelp.com/oauth2/token'
data_yelp ={'grand_type': 'client_credentials',
    'client_id': client_id, 'client_secret': client_secret}
r = requests.post(url_yelp, data = data_yelp)

yelp_access_token = r.json()['access_token']
yelp_search_url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'Bearer ' + yelp_access_token}

@app.route('/')
def index():
    """Homepage."""

    p_id = 49877

    # parameter including app_secret
    payload = {'$$app_token': secret_token,
                'physician_profile_id': p_id}

    response = requests.get("https://openpaymentsdata.cms.gov/resource/tf25-5jad.json", params=payload)
    
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
    headers = {'user-agent': 'curl/7.10.6 (i386-redhat-linux-gnu) libcurl/7.10.6 OpenSSL/0.9.7a ipv6 zlib/1.1.4'}

    response = requests.get("https://openpaymentsdata.cms.gov/resource/tf25-5jad.json", params=data)
    # import pdb; pdb.set_trace()
    # c enter
    search_results = response.json()
    # to keep only unique id of doctor so no duplicates in list of results:
    search_results = module.unique_dico(search_results)

    return render_template('results_list.html', search_results=search_results)

@app.route("/doc_summary/<int:physician_profile_id>")
def summary(physician_profile_id):
    """Show summary page on doctor resulting from search."""
    # Govt API Request
    summ = {'$$app_token': secret_token,
                'physician_profile_id': physician_profile_id,
            }

    # Issue request to Govt API/ Extract doctor personal info/ Caluclate payments received by doctor
    response = requests.get("https://openpaymentsdata.cms.gov/resource/tf25-5jad.json", params=summ)
    search_results = response.json()
    t = module.total_payments(search_results)
    first_name = search_results[0]['physician_first_name']
    last_name = search_results[0]['physician_last_name']
    info_doc = module.perso_doc_info(search_results)
    pay_breakdown = module.pay_per_comp(search_results)
    # List of tuple ; tuple = (pharmacy name, total):
    top_pharm = module.pay_per_comp_filtered(pay_breakdown,t)


    # Nber of Like for this doctor section:
    nb_likes = 0
    doctor1 = db.session.query(Doctor).filter(Doctor.doctor_id==info_doc['p_id']).first()
    if doctor1:
        nb_likes = Like.query.filter_by(doctor_id=session['info_doc']['p_id']).count()
    session['likes'] = nb_likes
        
    # Check if user did like this doctor
    liked_check = None
    if session.get('user_id'):
        liked_check = db.session.query(Like).filter(Like.doctor_id==info_doc['p_id'], 
            Like.user_id == session['user_id']).first()


    # Setting relevant values in session what I am going to need later:
    session['info_doc'] = info_doc
    session['info_doc']['total_received'] = round(t,2)
    session['pay_breakdown'] = top_pharm
    session['doc_chart_pharm'] = module.tuplelist_to_listfirstitem(top_pharm)
    session['doc_chart_payment'] = module.tuplelist_to_listseconditem(top_pharm)
  
    top_pharm_dic_no_other = top_pharm
    top_pharm_dic_no_other.pop()
    session['listsamecompanies'] = module.tuplelist_to_listfirstitem(top_pharm_dic_no_other)
    session['doc_payments_no_other']=module.tuplelist_to_listseconditem(top_pharm_dic_no_other)
    
    # Yelp API request
    # storer rating in session
    
    params = {
    'term': session['info_doc']['last_name'],
    'location':  session['info_doc']['city'] + session['info_doc']['zipcode'],
    'categories': 'health'

    }

    result = requests.get(url=yelp_search_url, params=params, headers=headers)

    businesses = result.json()['businesses']
    for business in businesses:
        name = business['name'].upper()
        city = business['location']['city'].upper()
        if session['info_doc']['last_name'] in name and session['info_doc']['city'] in city and session['info_doc']['first_name'] in name:
            session['info_doc']['rating'] = business['rating']
            session['info_doc']['url'] = business['url']
            print session['info_doc']['url']
            break
   
   # Return parameters to jinja  
    return render_template("summary.html", 
        perso_doc_info = info_doc, pay_breakdown=top_pharm, first_name=
        first_name, last_name=last_name, p_id= physician_profile_id, liked_check=liked_check)

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
    avg_per_state = round(module.averg_per_state(all_payments),2)
    avg_pharm = module.averg_per_company(all_payments) #dictionnary with key: pharmacy, value: avg payed doc for specific specialty & state
    avg_pharm_match_doc = module.averg_ind_comp_doc(avg_pharm, session['pay_breakdown'])
    session['doc_comp'] = module.list_tup_to_dic(session['pay_breakdown'])
    # session['bar_chart'] = module.bar_chart_dic(session['doc_comp'],avg_pharm_match_doc)
    session['pharm_avg'] = module.pharm_avg_sortedlist(avg_pharm_match_doc)
    
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

@app.route("/sign_in")
def sign_in():
    """Sign-in access."""

    return render_template("sign_in.html")

@app.route('/confirmation-sign_in', methods=["POST"])
def conf_sign_in():
    """Conf sign-in"""
    fname = request.form.get('fname')
    print fname
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')
    q1 = User.query.filter_by(email=email).first()
    if q1 == None:
        if age:
            u1 = User(first_name = fname, last_name= lname, email=email, password=password,
            age = int(age), zipcode = int(zipcode))
        else:
            u1 = User(first_name = fname, last_name= lname, email=email, password=password,
             zipcode = int(zipcode))
        db.session.add(u1)
        db.session.commit()
        return render_template('conf_sign_in.html', email=email, passw=password)
    else:
        flash("It is already taken, please choose smthg else")
        return redirect('/sign_in')

@app.route("/log_in")
def log_in():
    """Log-in."""
    if session.get('user_id'):
        flash("You are already logged in.")
        return redirect('/')
    return render_template("log_in.html")

@app.route('/logged', methods=['POST'])
def logged():
    email = request.form.get('email')
    password = request.form.get('password')
    user = db.session.query(User).filter(User.email==email).first()
    user_id = user.user_id
    if user == None:
        flash("No such user")
        return redirect('/log_in')
    else:
        if user.password == password:
            flash("Welcome to What's up Doc")
            session["user_id"]= user_id
            return redirect('/')
        else:
            flash("Wrong password, please try again.")
            return redirect('/log_in')

# check why email bug when i log out when im already logged out
@app.route("/log_out")
def log_out():
    """Log user out."""

    if session.get('user_id',0) == 0:
        flash("You are not logged in.")
        return redirect("/")
    else:
        del session["user_id"]
        flash("Logged out.")
    return redirect("/")


# Like button
@app.route('/like', methods=["POST"])
def like():
    # doctor0 = db.session.query(Doctor).filter(Doctor.doctor_id==session['info_doc']['p_id']).first()
    doctor0 = Doctor.query.get(session['info_doc']['p_id'])
    if doctor0 is None:
        doctor1 = Doctor(doctor_id = session['info_doc']['p_id'],first_name = 
        session['info_doc']['first_name'],last_name=session['info_doc']['last_name'],
        specialty= session['info_doc']['short_specialty'],yelp_rating = session['info_doc']['rating'])
        db.session.add(doctor1)
    like1 = Like(doctor_id=session['info_doc']['p_id'], user_id=session['user_id'])
    db.session.add(like1)
    db.session.commit()
    nb_likes = Like.query.filter_by(doctor_id=session['info_doc']['p_id']).count()
    session['likes'] = nb_likes
    return jsonify({'like': nb_likes})

@app.route('/unlike', methods=["POST"])
def unlike():
    
    Like.query.filter_by(doctor_id=session['info_doc']['p_id'], user_id=session['user_id']).delete()
    db.session.commit()
    nb_likes = Like.query.filter_by(doctor_id=session['info_doc']['p_id']).count()
    session['likes'] = nb_likes
    return jsonify({'unlike': nb_likes})


@app.route("/user_page")
def user_page():
    """User_page."""
    user1 = db.session.query(User).filter(User.user_id==session['user_id']).first()
    fname = user1.first_name
    lname = user1.last_name
    email = user1.email
    zipcode = user1.zipcode

    likes = db.session.query(Like).filter(Like.user_id==session['user_id']).all()
    nb_vote = db.session.query(Like).filter(Like.user_id==session['user_id']).count()
    print nb_vote
    return render_template("user.html", fname = fname, lname=lname, email=email, 
        zipcode=zipcode, likes=likes ,nb_vote=nb_vote)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host="0.0.0.0")
