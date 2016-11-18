import json
from unittest import TestCase
from model import Doctor, User, Like, connect_to_db, db, example_data
from server import app
import server


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
        self.assertIn("Search", result.data)


    def testSummaryPage(self):
        """Test summary page."""
        result = self.client.get("/doc_summary/98906", data={'physician_profile_id': 98906})
        self.assertIn("Forward", result.data)
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


    def testLogIn(self):
        """ Test Log-in page"""
        result = self.client.post("/sign_in", data={'fname': 'ben', 'lname':'berger', 
            'email':'ben@gmail.com','password': 'ben', 'zipcode':94109})
        self.assertIn("Welcome", result.data)

# test if I log out
# test if I sign in and already exists
# test if log in and wrong password
# test if log in and already logged in 

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
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

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


if __name__ == "__main__":
    import unittest

    unittest.main()
