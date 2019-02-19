#!/usr/bin/python3
"""tests for User class"""
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.amenity import Amenity
from models.engine.file_storage import FileStorage


class Test_BaseModel(unittest.TestCase):
    """test cases for Amenity obj"""

    def setUp(self):
        """Setup for all tests that will be run"""
        # Delete file.json
        try:
            with open('file.json', 'w+') as f:
                f.write('')
        except Exception as e:
            pass

    def test_create_new(self):
        """tests if valid instance of Amenity is created"""
        my_amenity = Amenity()
        my_amenity.first_name = "Betty"
        my_amenity.last_name = "Holberton"
        my_amenity.email = "airbnb@holbertonshool.com"
        my_amenity.password = "root"

        self.assertEqual(str, type(my_amenity.first_name))
        self.assertEqual(str, type(my_amenity.last_name))
        self.assertEqual(str, type(my_amenity.email))
        self.assertEqual(str, type(my_amenity.password))

        self.assertEqual(my_amenity.first_name, "Betty")
        my_amenity.first_name = "bob"
        self.assertEqual(my_amenity.first_name, "bob")
        my_amenity.first_name = ""
        self.assertEqual(my_amenity.first_name, "")

    def test_create_empty(self):
        """test amenity attributes from BaseModel"""
        my_amenity = Amenity()
        self.assertEqual(str, type(my_amenity.id))
        self.assertEqual(datetime, type(my_amenity.created_at))
        self.assertEqual(datetime, type(my_amenity.updated_at))

    def test_to_dict(self):
        """test that to_dict creates dict"""
        my_amenity = Amenity()
        test_dict = my_amenity.to_dict()
        self.assertEqual(dict, type(test_dict))

        capture = {k: v for k, v in my_amenity.__dict__.items()}
        capture['__class__'] = 'Amenity'
        capture['updated_at'] = capture['updated_at'].isoformat()
        capture['created_at'] = capture['created_at'].isoformat()
        actual = my_amenity.to_dict()
        self.assertDictEqual(capture, actual)
        actual['cat'] = 2
        self.assertEqual(actual['cat'], 2)

        """test type of values in to_dict"""
        self.assertEqual(str, type(capture['__class__']))
        self.assertEqual(str, type(capture['updated_at']))
        self.assertEqual(str, type(capture['created_at']))

    def test_unique_values(self):
        """test each amenity has unique values"""
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)
        self.assertNotEqual(amenity1.created_at, amenity2.created_at)
        self.assertNotEqual(amenity1.updated_at, amenity2.updated_at)

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
        my_amenity = Amenity()
        org_created = my_amenity.created_at.isoformat()
        org_updated = my_amenity.updated_at.isoformat()
        my_amenity.save()
        new_created = my_amenity.created_at.isoformat()
        new_updated = my_amenity.updated_at.isoformat()
        self.assertNotEqual(org_updated, org_created)
        self.assertEqual(org_created, new_created)

    def test_check_save(self):
        """check save writes to file"""
        storage = FileStorage()
        my_amenity1 = Amenity()
        my_amenity1.save()
        len_dict1 = len(storage.all())
        my_amenity2 = Amenity()
        my_amenity2.save()
        len_dict2 = len(storage.all())
        self.assertNotEqual(len_dict1, len_dict2)

    def test_create(self):
        """create instance of amenity from kwargs"""
        storage = FileStorage()
        amenity1 = Amenity(created_at="2017-06-14T22:31:03.285259", heads=4,
                           updated_at="2017-06-14T22:31:03.285259", id=3434)
        self.assertEqual(amenity1.heads, 4)
        _dict = storage.all()  # store __object dict
        test_list = [k for k in _dict.keys()]
        key = "Amenity." + str(amenity1.id)
        self.assertIn(key, test_list)

    def test_invalid_initialization(self):
        """create Amenity instance in illegal ways"""
        storage = FileStorage()
        amenity1 = Amenity(None)
        self.assertEqual(str, type(amenity1.id))
        self.assertEqual(datetime, type(amenity1.created_at))
        amenity2 = Amenity(id="ball")
        self.assertEqual(str, type(amenity2.id))
        self.assertEqual(datetime, type(amenity2.created_at))

    def test_create_instance_partial_input_valid(self):
        """Create an instance of BaseModel from dictionary input
        that does not have all common attributes of
        BaseModel class"""

        # Only id is given
        expected = 5
        a = Amenity(id=expected)
        self.assertEqual(a.id, expected)

        # Only updated_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = Amenity(updated_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['updated_at'])

        # Only created_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = Amenity(created_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['created_at'])

        # Variables other than the three listed were given
        expected = 'hi'
        a = Amenity(random=expected)
        self.assertEqual(a.random, expected)

    def test_create_instance_empty_dict(self):
        """Create an instance of BaseModel when no dictionary is used"""
        inputs = [10, 10.2, (10, ), [1], 'str', True, None]
        for element in inputs:
            a = Amenity(element)
            self.assertEqual(Amenity, type(a))
