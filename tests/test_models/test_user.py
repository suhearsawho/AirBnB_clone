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

    def test_to_dict(self):
        """test that to_dict creates dict"""
        my_user = User()
        test_dict = my_user.to_dict()
        self.assertEqual(dict, type(test_dict))

        capture = {k: v for k, v in my_user.__dict__.items()}
        capture['__class__'] = 'User'
        capture['updated_at'] = capture['updated_at'].isoformat()
        capture['created_at'] = capture['created_at'].isoformat()
        actual = my_user.to_dict()
        self.assertDictEqual(capture, actual)
        actual['cat'] = 2
        self.assertEqual(actual['cat'], 2)

    def test_unique_values(self):
        """test each user has unique values"""
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)
        self.assertNotEqual(user1.created_at, user2.created_at)
        self.assertNotEqual(user1.updated_at, user2.updated_at)

    def test_str_output(self):
        """Tests that str is printing in the correct format"""
        date = '2017-09-28T21:05:54.119427'
        entries = {'id': '124', 'created_at': date, 'updated_at': date}
        a = BaseModel(**entries)
        entries['created_at'] = datetime.strptime(
            entries['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
        entries['updated_at'] = datetime.strptime(
            entries['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
        expected = '[BaseModel] (124) {}'.format(entries)
        actual = str(a)
        self.assertEqual(expected, actual)
