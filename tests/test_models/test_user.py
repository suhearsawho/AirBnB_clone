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

        """test type of values in to_dict"""
        self.assertEqual(str, type(capture['__class__']))
        self.assertEqual(str, type(capture['updated_at']))
        self.assertEqual(str, type(capture['created_at']))


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

    def test_save_method(self):
        """test save method updates time"""
        my_user = User()
        org_created = my_user.created_at.isoformat()
        org_updated = my_user.updated_at.isoformat()
        my_user.save()
        new_created = my_user.created_at.isoformat()
        new_updated = my_user.updated_at.isoformat()
        self.assertNotEqual(org_updated, org_created)
        self.assertEqual(org_created, new_created)

    def test_check_save(self):
        """check save writes to file"""
        storage = FileStorage()
        my_user1 = User()
        my_user1.save()
        len_dict1 = len(storage.all())
        my_user2 = User()
        my_user2.save()
        len_dict2 = len(storage.all())
        self.assertNotEqual(len_dict1, len_dict2)

    def test_create(self):
        """create instance of user from kwargs"""
        storage = FileStorage()
        user1 = User(created_at = "2017-06-14T22:31:03.285259", heads = 4,
                      updated_at = "2017-06-14T22:31:03.285259", id = 3434)
        self.assertEqual(user1.heads, 4)
        _dict = storage.all()  # store __object dict
        test_list = [k for k in _dict.keys()]
        key = "User." + str(user1.id)
        self.assertIn(key, test_list)

    def test_invalid_initialization(self):
        """create User instance in illegal ways"""
        storage = FileStorage()
        user1 = User(None)
        self.assertEqual(str, type(user1.id))
        self.assertEqual(datetime, type(user1.created_at))
        user2 = User(id = "ball")
        self.assertEqual(str, type(user2.id))
        self.assertEqual(datetime, type(user2.created_at))

    def test_create_instance_partial_input_valid(self):
        """Create an instance of BaseModel from dictionary input
        that does not have all common attributes of
        BaseModel class"""

        # Only id is given
        expected = 5
        a = User(id=expected)
        self.assertEqual(a.id, expected)

        # Only updated_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = User(updated_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['updated_at'])

        # Only created_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = User(created_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['created_at'])

        # Variables other than the three listed were given
        expected = 'hi'
        a = User(random=expected)
        self.assertEqual(a.random, expected)

    def test_create_instance_empty_dict(self):
        """Create an instance of BaseModel when no dictionary is used"""
        inputs = [10, 10.2, (10, ), [1], 'str', True, None]
        for element in inputs:
            a = User(element)
            self.assertEqual(User, type(a))
