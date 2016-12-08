import json
import unittest
from unittest import TestCase
from model import Doctor, User, Like, connect_to_db, db, example_data
from server import app
import server, helper, model


class FlaskTestIntegrationLoggedIn(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "ABC"
        
        # session entering in search 'Charles Saha' and being logged in as 'salome' user 
        with self.client as c:
            with c.session_transaction() as session:
                session['info_doc'] = {'short_specialty': u'Gastroenterology', 
                'city': u'NEW YORK', 'first_name': u'CHARLES', 'last_name': u'SAHA', 
                'name': u'Charles Saha', 'rating': 3.5, 'url': u'https://www.yelp.com'\
                '/biz/saha-s-charles-md-new-york?adjust_creative=tlmYwaULihK1wN2xL2o_'\
                'FQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_'\
                'source=tlmYwaULihK1wN2xL2o_FQ', 'p_id': u'98906', 
                'specialty': u'Allopathic & Osteopathic Physicians|Internal Medicine|Gastroenterology', 
                'total_received': 1087.71, 'zipcode': u'10028-1062', 'state': u'NY', 
                'lat': 40.7795808, 'lng': -73.95631519999999, 
                'gmap_address': u'120 E 86TH ST 10028-1062 NEW YORK NY ', 
                'street_address': u'120 E 86TH ST'}
                session['pay_breakdown'] = [(u'Shire North American Group Inc', 171.77), 
                (u'GlaxoSmithKline, LLC.', 160.48000000000002), 
                (u'Merck Sharp & Dohme Corporation', 127.34000000000002), 
                (u'Takeda Pharmaceuticals U.S.A., Inc.', 121.86)]
                session['doc_chart_pharm'] = [u'GlaxoSmithKline, LLC.',
                u'Merck Sharp & Dohme Corporation', 'Other', 
                u'Shire North American Group Inc', u'Takeda Pharmaceuticals U.S.A., Inc.']
                session['doc_chart_payment'] = [160.48, 127.34, 506.26, 171.77, 121.86]
                session['listsamecompanies'] = [u'GlaxoSmithKline, LLC.', 
                u'Merck Sharp & Dohme Corporation', u'Shire North American Group Inc', u'Takeda Pharmaceuticals U.S.A., Inc.']
                session['doc_payments_no_other'] = [160.48, 127.34, 171.77, 121.86]
                session['likes'] = 2L
                session['doc_comp'] = {u'Shire North American Group Inc': 171.77, 
                u'Merck Sharp & Dohme Corporation': 127.34000000000002, 
                u'Takeda Pharmaceuticals U.S.A., Inc.': 121.86, u'GlaxoSmithKline, LLC.': 160.48000000000002}
                session['pharm_avg'] = [17.0, 27.0, 16.0, 117.0]
                session["user_id"] = 2

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertEqual(result.status_code,200)
        self.assertIn("Search", result.data)


    def testResultPage(self):
        """Test results page."""

        result = self.client.get("/results_list", data={'firstname':'charles', 'lastname':'saha'})
        self.assertIn("Specialty", result.data)


    def testSummaryPage(self):
        """Test summary page."""
        result = self.client.get("/doc_summary/98906", data={'physician_profile_id': 98906})
        self.assertIn("Email", result.data)
        # self.assertIn('<iframe class="chartjs-hidden-iframe"', result.data)


    def testIndComparison(self):
        """ Test industry comparison page """
        result = self.client.get("/ind_comparison/98906/Allopathic & Osteopathic " \
            "Physicians|Internal Medicine|Gastroenterology/NY/NEW YORK")
        self.assertIn("Average", result.data)


    def testUserPage(self):
        """ Test user page """
        result = self.client.get("/user_page")
        self.assertIn("liked", result.data)


    def testSignIn(self):
        """ Test Sign-in page"""
        result = self.client.post("/sign_in", data={'fname': 'ben', 'lname':'berger', 
            'email':'ben@gmail.com','password': 'ben', 'zipcode':94109})
        self.assertIn("Welcome", result.data)


    def testLogOut(self):
        """ Test Log-out page"""
        result = self.client.get("/log_out", follow_redirects=True)
        # import pdb; pdb.set_trace() 
        self.assertIn("Find", result.data)

        
    def testLogIn(self):
        """ Test Log-in page if already logged-in"""
        result = self.client.get("/log_in", follow_redirects=True)
        # import pdb; pdb.set_trace() 
        self.assertIn("Number", result.data)


    def testLike(self):
        """ Test /Like route """
        result = self.client.post("/like", follow_redirects=True)
        self.assertEqual(result.status_code, 200)

    def testUnlike(self):
        """ Test /unlke route """
        result = self.client.post("/unlike", follow_redirects=True)
        self.assertEqual(result.status_code, 200)

    def testPieChart(self):
        """ Test /doc_info route route """
        result = self.client.get("/doc_info.json", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("datasets", result.data)


    def testBarChart(self):
        """ Test /ind_info.json route route """
        result = self.client.get("/ind_info.json", follow_redirects=True)
        self.assertEqual(result.status_code, 200)


    def testSendEmail(self):
        """ Test /send_email route route """
        result = self.client.post("/send_email", data={'emailAddress': "bla@gmail.com"})
        self.assertEqual(result.status_code, 200)
     

# test if log in and wrong password

# case where doc paid by less than 3 companies
# case where response is empty
# if I have less than 10 doctors payed less


# Do integration test forform (post) search, log in and log out 
# class FlaskTestsDatabase(TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """Do at end of every test."""

#         db.session.close()
#         db.drop_all()

#     def test_departments_list(self):
#         """Test departments page."""

#         result = self.client.get("/departments")
#         self.assertIn("Legal", result.data)


#     def test_departments_details(self):
#         """Test departments page."""

#         result = self.client.get("/department/fin")
#         self.assertIn("Phone: 555-1000", result.data)


#     

# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_user_page(self):
#         """Test important page."""

#         result = self.client.get("/user_page")
#         self.assertIn("You are a valued user", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged out of session."""

    def setUp(self):
        """ To do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()
        app.config['SECRET_KEY'] = "ABC"

        with self.client as c:
            with c.session_transaction() as session:
                session['info_doc'] = {'short_specialty': u'Gastroenterology', 
                'city': u'NEW YORK', 'first_name': u'CHARLES', 'last_name': u'SAHA', 
                'name': u'Charles Saha', 'rating': -1, 'p_id': u'98906', 
                'specialty': u'Allopathic & Osteopathic Physicians|Internal Medicine|Gastroenterology', 
                'total_received': 1087.71, 'zipcode': u'10028-1062', 'state': u'NY', 
                'street_address': u'120 E 86TH ST'}
                session['pay_breakdown'] = [(u'Shire North American Group Inc', 171.77), (u'GlaxoSmithKline, LLC.', 160.48000000000002), 
                (u'Merck Sharp & Dohme Corporation', 127.34000000000002), 
                (u'Takeda Pharmaceuticals U.S.A., Inc.', 121.86)]
                session['doc_chart_pharm'] = [u'GlaxoSmithKline, LLC.',
                u'Merck Sharp & Dohme Corporation', 'Other', 
                u'Shire North American Group Inc', u'Takeda Pharmaceuticals U.S.A., Inc.']
                session['doc_chart_payment'] = [160.48, 127.34, 506.26, 171.77, 121.86]
                session['listsamecompanies'] = [u'GlaxoSmithKline, LLC.', 
                u'Merck Sharp & Dohme Corporation', u'Shire North American Group Inc', u'Takeda Pharmaceuticals U.S.A., Inc.']
                session['doc_payments_no_other'] = [160.48, 127.34, 171.77, 121.86]
                session['likes'] = 2L
                session['doc_comp'] = {u'Shire North American Group Inc': 171.77, 
                u'Merck Sharp & Dohme Corporation': 127.34000000000002, 
                u'Takeda Pharmaceuticals U.S.A., Inc.': 121.86, u'GlaxoSmithKline, LLC.': 160.48000000000002}
                session['pharm_avg'] = [17.0, 27.0, 16.0, 117.0]

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        # Create tables and add sample data
        db.create_all()
        example_data()

    def test_user_page(self):
        """Test that user can't see important page when logged out."""
        result = self.client.get("/user_page")
        self.assertNotIn("Number", result.data)
        self.assertIn("You are not logged-in", result.data)

    def testSummaryLike(self):
        """ Test that summary page do not allow user to 'like'"""
        result = self.client.get("/doc_summary/98906", data={'physician_profile_id': 98906})
        self.assertIn("Login to vote", result.data)


    def LogIn(self):
        """ Test log-in when user not initially logged in'"""
        result = self.client.post("/log_in", data={'email':'salome@gmail.com',
            'password':'salome'})
        self.assertIn("Number", result.data)

    def LogIn2(self):
        """ Test log-in when user not initially logged in and enters wrong password'"""
        result = self.client.post("/log_in", data={'email':'salome@gmail.com',
            'password':'bla'})
        self.assertIn("try", result.data)

    def testSignUp(self):
        """ Test Sign-up page"""
        result = self.client.get("/sign_in", data={'fname': 'ben', 'lname':'berger', 
            'email':'salome@gmail.com','password': 'ben', 'zipcode':94109})
        self.assertIn("name", result.data)

    def testSignUp2(self):
        """ Test Sign-in with existing email address"""
        result = self.client.post("/sign_in", data={'fname': 'ben', 'lname':'berger', 
            'email':'salomefake@gmail.com','password': 'ben', 'zipcode':94109}, follow_redirects=True)
        self.assertIn("Welcome", result.data)

    def testLogOut(self):
        """ Test Log-out page when not logged-in"""
        result = self.client.get("/log_out", follow_redirects=True)
        # import pdb; pdb.set_trace() 
        self.assertIn("Search", result.data)

class UnitTestCase(unittest.TestCase):
    """Test function from helper.py"""
    def test_pay_per_comp_filtered(self):
        assert helper.pay_per_comp_filtered({}, 4) == []
    
    # def test_repr(self):
    # assert model.repr(User(first_name='bar')) == "<MyClass: {'foo': 'bar'}>"
    # True

    # first_name = db.Column(db.String(64), nullable=False)
    # last_name = db.Column(db.String(64), nullable=False)
    # email = db.Column(db.String(64), nullable=False)
    # password = db.Column(db.String(200), nullable=False)
    # age = db.Column(db.Integer, nullable=True)
    # zipcode = db.Column(db.Integer, nullable=False)

if __name__ == "__main__":
    import unittest

    unittest.main()
