What's Up Doc
===========

Learn more about the developer: https://www.linkedin.com/in/salomechamma

Finding  doctors is hard. When I first moved to the US from France 4 years ago I didn't know where to turn to find a doctor. There are some resources like Zocdoc and Yelp, but who really wants to find their doctor from the same place they find the best taco truck? I developed What's up Doc to offer users a unique tool to discover physicians’ compensations from pharmaceutical companies. Intended to educate patients, this web app allows users to gain greater transparency and strengthen the trust between patients and doctors.

![Homepage](https://raw.githubusercontent.com/salomechamma/Doctor_Project/master/static/img/homepage.png)


### Technology

* Python
* Flask, Flask-mail
* Jinja
*  PostgreSQL, SQL Alchemy
* Javascript (Jquery, Ajax, JSON, Chart.js)
* HTML, CSS & Bootstrap
* Passlib
* Unit and Integration Testing



##### Backend

An interesting challenge I had was that my API was not always returning results even though it returned it in the past. When the attempt was unsuccessful it would return an empty list.  I realized the lack of consistency was coming from the API, and to circumvent this I created additional web keys and had the server choose randomly from the list of keys when making a request until the list received was not empty. I was able to improve the match rate from 30% to 90%.


##### Database


##### Frontend







##### Tests
##### Version 2.0

###### Improvements



###### New Features



### Structure

##### server.py
Core of the flask app, lists all routes.
##### configuration.py
##### helper.py
##### model.py
All database queries made by the flask app.

##### tests.py




 



