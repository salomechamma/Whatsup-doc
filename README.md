What's Up Doc
===========

Learn more about the developer: https://www.linkedin.com/in/salomechamma

Finding a doctor is hard. When I first moved to the US from France 4 years ago I didn't know where to turn to find a doctor. There are some resources like Zocdoc and Yelp, but who really wants to find their doctor from the same place they find the best taco truck? 


### Overview

What's up Doc features a responsive search interface to explore the relationship between doctors and pharmaceutical companies.

The website offers users a unique tool to discover physicians’ compensations from pharmaceutical companies. Intended to educate patients, the app allows users to gain greater transparency and strengthen the trust between patients and doctors. To help better interpret the results, What’s up Doc compares payments received by a doctor with the state average compensation rate and pulls reviews from various sources. For users looking for a different physician, the app also provides an alternate list of doctors in the same city who have accepted less compensation. Authenticated users can refer to a list of their saved or ‘liked’ physicians and email themselves the information for future reference.



### Technology

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


##### Features

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
    * Users can like or unlike a doctor which automatically saves that doctor to the users account page.
    * Shows total number of doctor likes by all web app users.
    * Displays total compensation to doctor and breaks it down by pharmaceutical company in a pie chart.
    * Link to Industry Average page

 ![Physician Information](https://github.com/salomechamma/Doctor_Project/blob/master/static/img/docinfo.png)

---------

* Industry Comparison and Alternate Doctors Page
    * Bar graph comparing doctors compensation to the state average, broken down by individual pharmaceutical company. 
    * List of alternative doctors of the same specialty, in the same city who recieved less by pharmaceutical companies

![Homepage](https://github.com/salomechamma/Doctor_Project/blob/master/static/img/comp.png)


### The Mechanic behind What's Up Doc


When the user enters a doctor name, the server, built using the Flask framework, makes a request to the CMS API, the parameters being the name entered. It lists of all the different doctors that match the search using the API doctor ID to differentiate them. 



The users selects the right doctor and gets: 
* The doctor contact information 
* A map showing the physician location: the latitude and longitude of the doctor address is retrived using Google maps Geocoder and sent the request to Google Maps API.
* The yelp score and URL of the doctor page if it exists: a call is made to the Yelp API using the doctor name and location as parameters. To make sure the URL and score correspond to the right doctor, I check tht the full doctor name is part of the Yelp business name (title of the Yelp page).
* An internal rating system where the user can like or unlike a doctor: An ajax call is made to the server using SQL Alchemy to update the number of likes in the Postgress database and at the same time the number of likes and the button action are dynamically updated using JavaScript. 
* Two charts using Chart.js: 
    * Pie chart to display the payments from each pharmaceutical company to the doctor. After extracting and storing the company that paid the doctors I calculated the total payments  they each made and returned this info as a JSON file to the front end.
    * Bar chart to compare the payments received by the doctor with the state average for the same specialty broken down by pharmaceutical company.


* The option to  email the information of this page by creating a route in the server which builds and sends the email using Flask-mail.

![Physician Information](https://github.com/salomechamma/Doctor_Project/blob/master/static/img/email.png)

* A list of alternatives doctors who received less compensations than the given doctor.  
* The website also includes register login logout and user page including a list of doctors the user has previously liked. 




### Challenges
* An interesting challenge I had was that my API was not always returning results even though it returned it in the past. When the attempt was unsuccessful it would return an empty list.  I realized the lack of consistency was coming from the API, and to circumvent this I created additional web keys and had the server choose randomly from the list of keys when making a request until the list received was not empty. I was able to improve the match rate from 30% to 90%.


### Tests
The web app has been tested using unit tests and integration tests.
The coverage so far reached 90%.

### Version 2.0

###### Improvements
* Allow the user to look for a doctor by only entering the last name or the zipcode instead of the full name as it is currently.
* Create more API keys to reach a total match of 100% when searching for a doctor.
* Show on the pie chart for each company the type of expenses (ex: restaurant, conference, travel etc..).

###### New Features
* On the bar chart: Add breakdown of type of payment for each company for both the doctor bar and the state average bar.
* Display the average payments per state per specialty.
* Predict compensations for next year (the API only tracks companies payments since 2013).



### Structure

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




 



