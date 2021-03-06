#What's Up Doc ![carrot](https://github.com/salomechamma/Whatsup-doc/blob/master/static/img/carrot_title.png)

===========

###### Deployed Site: [What's Up Doc](https://whatsup-doc.herokuapp.com/)<br>

Finding a doctor is hard. When I first moved to the US from France 4 years ago I didn't know where to turn to find a doctor. There are some resources like Zocdoc and Yelp, but who really wants to find their doctor from the same place they find the best taco truck? 

##Contents
* [Overview](#overview)
* [Tech Stack](#tech)
* [Features](#features)
* [Version 2.0](#v2)
* [Installation](#install)
* [Behind The Scene](#bts)
* [Challenges](#challenges)
* [Structure](#structure)
* [About Me](#aboutme)


### <a name="overview"></a>Overview

What's up Doc features a responsive search interface to explore the relationship between doctors and pharmaceutical companies.

The website offers users a unique tool to discover physicians’ compensations from pharmaceutical companies. Intended to educate patients, the app allows users to gain greater transparency and strengthen the trust between patients and doctors. To help better interpret the results, What’s up Doc compares payments received by a doctor with the state average compensation rate and pulls reviews from various sources. For users looking for a different physician, the app also provides an alternate list of doctors in the same city who have accepted less compensation. Authenticated users can refer to a list of their saved or ‘liked’ physicians and email themselves the information for future reference.



### <a name="tech"></a>Tech Stack

* Python
* Flask, Flask-mail
* Jinja
*  PostgreSQL, SQL Alchemy
* Javascript (Jquery, Ajax, JSON, Chart.js)
* HTML, CSS & Bootstrap
* Passlib
* Unit and Integration Testing

To build this website I used 3 RESTful web APIS: 
* The Centers for Medicare and Medicaid Services or CMS
* Yelp 
* Google maps


#### <a name="features"></a>Features

![List of results](https://github.com/salomechamma/Doctor_Project/blob/master/static/img/homepage.png)

* The Homepage
    * Search bar to look up specific doctors
    * Users can Sign Up and create their own account to save their favorite doctors.
    * Users can login to their their existing account.

* Result page
    * Users choose the right doctor

![List of results](https://github.com/salomechamma/Doctor_Project/blob/master/static/img/results.png)

-------------

* Doctor Details Page
    * Lists doctors name, adress and specialty
    * Uses Google Maps Geocoder and Google Maps API to display the exact location.
    * Connects to the Yelp API to show the yelp score (if available) and a link to the Yelp Page.
    * Users can like or unlike a doctor which automatically saves that doctor to the Users account page.
    * Shows total number of doctor likes by all web app users.
    * Displays total compensation to doctor and breaks it down by pharmaceutical company in a pie chart.
    * Link to Industry Average page

 ![Physician Information](https://github.com/salomechamma/Doctor_Project/blob/master/static/img/docinfo.png)

---------

* Industry Comparison and Alternate Doctors Page
    * Bar chart comparing doctors compensation to the state average, broken down by individual pharmaceutical company. 
    * List of alternative doctors of the same specialty, in the same city who recieved less by pharmaceutical companies

![Homepage](https://github.com/salomechamma/Doctor_Project/blob/master/static/img/comp.png)





### Tests
The web app has been tested using unit tests and integration tests.
The coverage so far reached 92%.

### <a name="v2"></a>Version 2.0

###### Improvements
* Allow the User to look for a doctor by only entering the last name or the zipcode instead of the full name as it is currently.
* Create more API keys to reach a total match of 100% when searching for a doctor.
* Show on the pie chart for each company the type of expenses (ex: restaurant, conference, travel etc..).

###### New Features
* On the bar chart: Add breakdown of type of payment for each company for both the doctor bar and the state average bar.
* Display the average payments per state per specialty.
* Predict compensations for next year (the API only tracks companies payments since 2013).

### <a name="install"></a>Installation 

To run What's Up Doc:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
$ git clone https://github.com/salomechamma/Whatsup-doc.git
```

Create and activate a virtual environment inside your What's Up Doc directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use the [CMS API](https://dev.socrata.com/foundry/openpaymentsdata.cms.gov/tf25-5jad), the [Google Maps API](https://developers.google.com/maps/documentation/embed/guide), and the [Yelp API](https://www.yelp.com/login?return_url=%2Fdevelopers%2Fmanage_api_keys)

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format. Note that 5 different CMS keys have been created in order to increase the match rate (for more details, please refer to the ReadMe "Challenge" section).

```
export EMAIL_PASSWORD="YOUR_KEY_HERE"

export DOC_APP_TOKEN3="YOUR_KEY_HERE"
export DOC_APP_TOKEN1="YOUR_KEY_HERE"
export DOC_APP_TOKEN2="YOUR_KEY_HERE"
export DOC_APP_TOKEN4="YOUR_KEY_HERE"
export DOC_APP_TOKEN5="YOUR_KEY_HERE"

export YELP_APP_ID="YOUR_KEY_HERE"
export YELP_APP_SECRET="YOUR_KEY_HERE"
export GOOGLE_KEY="YOUR_KEY_HERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb doctors
python model.py
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access What's Up Doc.


### <a name="bts"></a>Behind The Scene

When the User enters a doctor name, the server, built using the Flask framework, makes a request to the CMS API, the parameters being the name entered. It lists of all the different doctors that match the search using the API doctor's ID to differentiate them. 



The User selects the right doctor and gets: 
* The Doctor's contact information 
* A map showing the Physician's location: the latitude and longitude of the Doctor's address is retrived using Google maps Geocoder and sent the request to Google Maps API.
* The yelp score and URL of the doctor page if it exists: a call is made to the Yelp API using the doctor name and location as parameters. To make sure the URL and score correspond to the right doctor, I check tht the full doctor name is part of the Yelp business name (title of the Yelp page).
* An internal rating system where the User can like or unlike a doctor: An ajax call is made to the server using SQL Alchemy to update the number of likes in the Postgress database and at the same time the number of likes and the button action are dynamically updated using JavaScript. 
* Two charts using Chart.js: 
    * Pie chart to display the payments from each pharmaceutical company to the doctor. After extracting and storing the company that paid the doctors I calculated the total payments  they each made and returned this info as a JSON file to the front end.
    * Bar chart to compare the payments received by the doctor with the state average for the same specialty broken down by pharmaceutical company.


* The option to  email the information of this page by creating a route in the server which builds and sends the email using Flask-mail.

![Physician Information](https://github.com/salomechamma/Doctor_Project/blob/master/static/img/email.png)

* A list of alternatives doctors who received less compensations than the given doctor.  
* The website also includes register login logout and user page including a list of doctors the User has previously liked. 




### <a name="challenges"></a>Challenges
* An interesting challenge I had was that my API was not always returning results even though it returned it in the past. When the attempt was unsuccessful it would return an empty list.  I realized the lack of consistency was coming from the API, and to circumvent this I created additional web keys and had the server choose randomly from the list of keys when making a request until the list received was not empty. I was able to improve the match rate from 30% to 90%.

### <a name="structure"></a>Structure

##### server.py
Core of the flask app, lists all routes.

##### configuration.py
Contains all of the global variables.

##### helper.py
Contains all the helper functions called by the server.

##### model.py
All database queries made by the flask app.

##### tests.py
Include integration and unit tests.

### <a name="aboutme"></a>About the Developer 

Salomé lives in the San Francisco Bay Area. This is her first software project.
<br />
Before Hackbright Salomé worked in Marketing for four years in New York, growing from a Coordinator to a Manager in top cosmetic companies. Prior to this, she completed a Master’s degree in Mathematics at Dauphine University including some coding classes followed by a Master’s in Business at ESSEC Business School. She decided to pick up coding where she left off and to join Hackbright. Salomé is now excited to look for a full-stack software engineer position in the Bay Area.
 
Visit her on [LinkedIn](https://www.linkedin.com/in/salomechamma).

<img src="/static/img/salome.png" alt="salome"/>
<!-- 
![salome](https://github.com/salomechamma/Whatsup-doc/blob/master/static/img/salome.jpg) -->
<!-- style="height:50%;" -->
