import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
# Optional: Update the book information in setUp to make the test database your own!
    # def test_404_on_root(self):
    #     res = self.client().get('/')
    #     self.assertEqual(res.status.code,404)

    def test_422_on_delete_non_existant_book(self):
        res = self.client().delete("/books/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"unprocessable")

    def test_405_on_delete_when_no_record_is_specified(self):
        res = self.client().delete("/books")
        data = json.loads(res.data)

        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Method Not Allowed")
        self.assertEqual(res.status_code,405)

    def test_405_on_get_a_non_existant_book(self):
        res = self.client().get("/books/1000")
        data = json.loads(res.data)

        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Method Not Allowed")
        self.assertEqual(res.status_code,405)

    # def test_on_get_paginated_books(self):
    #     res = self.client().get("/books")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data["success"],True)
    #     self.assertEqual(data["total_books"],16)

    def test_get_paginated_books(self):
        res = self.client().get("/books")
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
