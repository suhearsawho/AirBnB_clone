#!/usr/bin/python3
"""tests for User class"""
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage

class Test_BaseModel(unittest.TestCase):
    """test cases for User obj"""

    def setUp(self):
        """Setup for all tests that will be run"""
        # Delete file.json
        try:
            with open('file.json', 'w+') as f:
                f.write('')
        except Exception as e:
            pass

    def test_create_new(self):
        """tests if valid instance of User is created"""
        my_user = User()
        my_user.first_name = "Betty"
        my_user.last_name = "Holberton"
        my_user.email = "airbnb@holbertonshool.com"
        my_user.password = "root"

        self.assertEqual(str, type(my_user.first_name))
        self.assertEqual(str, type(my_user.last_name))
        self.assertEqual(str, type(my_user.email))
        self.assertEqual(str, type(my_user.password))

        self.assertEqual(my_user.first_name, "Betty")
        my_user.first_name = "bob"
        self.assertEqual(my_user.first_name, "bob")
        my_user.first_name = ""
        self.assertEqual(my_user.first_name, "")

    def test_create_empty(self):
        """test user attributes from BaseModel"""
        my_user = User()
        self.assertEqual(str, type(my_user.id))
        self.assertEqual(datetime, type(my_user.created_at))
        self.assertEqual(datetime, type(my_user.updated_at))

    def test_serialization(self):
        """test that user object gets serialized"""
        my_user = User()
        my_user.save()
        
