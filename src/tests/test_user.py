import unittest
import os
import json
from ..app import create_app,db


class UserTest(unittest.TestCase):
    """
    User Test Case 
    """
    def setup(self):
        """
        Test Setup
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {
            'name': 'olawale',
            'email':'olawale@gmail.com',
            'password': 'password123'
        }
        

        with self.app.app_context():
            db.create_all()
