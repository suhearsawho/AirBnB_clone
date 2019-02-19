#!/usr/bin/python3
"""tests for city class"""
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage


class Test_BaseModel(unittest.TestCase):
    """test cases for City obj"""

    def setUp(self):
        """Setup for all tests that will be run"""
        # Delete file.json
        try:
            with open('file.json', 'w+') as f:
                f.write('')
        except Exception as e:
            pass

    def test_create(self):
        """create instance of city class"""
        my_city1 = City()
        self.assertEqual(str, type(my_city1.id))
        self.assertEqual(datetime, type(my_city1.created_at))
        self.assertEqual(datetime, type(my_city1.updated_at))

    def test_to_dict(self):
        """test that to_dict creates dict"""
        my_city = City()
        my_city.name = "bobo"
        test_dict = my_city.to_dict()
        self.assertEqual(dict, type(test_dict))

        capture = {k: v for k, v in my_city.__dict__.items()}
        capture['__class__'] = 'City'
        capture['updated_at'] = capture['updated_at'].isoformat()
        capture['created_at'] = capture['created_at'].isoformat()
        actual = my_city.to_dict()
        self.assertDictEqual(capture, actual)
        actual['cat'] = 2
        self.assertEqual(actual['cat'], 2)
        self.assertEqual(actual['name'], "bobo")

        """test type of values in to_dict"""
        self.assertEqual(str, type(capture['__class__']))
        self.assertEqual(str, type(capture['updated_at']))
        self.assertEqual(str, type(capture['created_at']))

    def test_unique_values(self):
        """test each city has unique values"""
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)
        self.assertNotEqual(city1.created_at, city2.created_at)
        self.assertNotEqual(city1.updated_at, city2.updated_at)
        self.assertEqual(city1.name, city2.name)

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
        my_city = City()
        org_created = my_city.created_at.isoformat()
        org_updated = my_city.updated_at.isoformat()
        my_city.save()
        new_created = my_city.created_at.isoformat()
        new_updated = my_city.updated_at.isoformat()
        self.assertNotEqual(org_updated, org_created)
        self.assertEqual(org_created, new_created)

    def test_check_save(self):
        """check save writes to file"""
        storage = FileStorage()
        my_city1 = City()
        my_city1.save()
        len_dict1 = len(storage.all())
        my_city2 = City()
        my_city2.save()
        len_dict2 = len(storage.all())
        self.assertNotEqual(len_dict1, len_dict2)

    def test_create(self):
        """create instance of City from kwargs"""
        storage = FileStorage()
        city1 = City(created_at="2017-06-14T22:31:03.285259", heads=4,
                     updated_at="2017-06-14T22:31:03.285259", id=3434)
        self.assertEqual(city1.heads, 4)
        _dict = storage.all()  # store __object dict
        test_list = [k for k in _dict.keys()]
        key = "City." + str(city1.id)
        self.assertIn(key, test_list)
        city1.name = "sam"
        self.assertEqual(city1.name, "sam")

    def test_invalid_initialization(self):
        """create City instance in illegal ways"""
        storage = FileStorage()
        city1 = City(None)
        self.assertEqual(str, type(city1.id))
        self.assertEqual(datetime, type(city1.created_at))
        city2 = City(id="ball")
        self.assertEqual(str, type(city2.id))
        self.assertEqual(datetime, type(city2.created_at))

    def test_create_instance_partial_input_valid(self):
        """Create an instance of BaseModel from dictionary input
        that does not have all common attributes of
        BaseModel class"""

        # Only id is given
        expected = 5
        a = City(id=expected)
        self.assertEqual(a.id, expected)

        # Only updated_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = City(updated_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['updated_at'])

        # Only created_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = City(created_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['created_at'])

        # Variables other than the three listed were given
        expected = 'hi'
        a = City(random=expected)
        self.assertEqual(a.random, expected)

    def test_create_instance_empty_dict(self):
        """Create an instance of BaseModel when no dictionary is used"""
        inputs = [10, 10.2, (10, ), [1], 'str', True, None]
        for element in inputs:
            a = City(element)
            self.assertEqual(City, type(a))
