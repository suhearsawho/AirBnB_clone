#!/usr/bin/python3
"""Tests for the BaseModel class"""
import unittest
from models.base_model import BaseModel
from datetime import datetime
from models.engine.file_storage import FileStorage


class Test_BaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""
    list_id = []

    def setUp(self):
        """Setup for all tests that will be run"""
        # Delete file.json
        try:
            with open('file.json', 'w+') as f:
                f.write('')
        except Exception as e:
            pass

    def test_create_new_valid(self):
        """Tests when a valid instance of BaseModel is created"""
        a = BaseModel()
        # Check id values
        self.assertEqual(str, type(a.id))
        self.assertNotIn(a.id, self.list_id)
        self.list_id.append(a.id)

        # Check updated_at and created_at values
        self.assertNotEqual(a.created_at.isoformat(), a.updated_at.isoformat())
        self.assertEqual(datetime, type(a.created_at))
        self.assertEqual(datetime, type(a.updated_at))

    # TODO: Test when BASEMODEL is given parameters upon instantiation

    def test_unique_id_values(self):
        """Tests that each instantiation of an object produces a unique ID"""
        a = BaseModel()
        self.assertNotIn(a.id, self.list_id)
        self.list_id.append(a.id)

        b = BaseModel()
        self.assertNotIn(b.id, self.list_id)
        self.list_id.append(b.id)

    def test_str_output(self):
        """Tests that str is printing in the correct format"""
        a = BaseModel()

    def test_save_method(self):
        """Tests that save updates the time"""
        a = BaseModel()
        original = a.updated_at.isoformat()
        original_created = a.created_at.isoformat()
        a.save()
        new = a.updated_at.isoformat()
        new_created = a.created_at.isoformat()
        self.assertNotEqual(original, new)
        self.assertEqual(original_created, new_created)

    def test_to_dict(self):
        """Tests that to_dict returns the appropriate dictionary"""
        a = BaseModel()
        expected = {key: value for key, value in a.__dict__.items()}
        expected['__class__'] = 'BaseModel'
        expected['updated_at'] = expected['updated_at'].isoformat()
        expected['created_at'] = expected['created_at'].isoformat()
        actual = a.to_dict()
        self.assertDictEqual(actual, expected)

        test_input = [80, (80, ), 'a', {'hi': 5}, [1], 5.12, True, None]
        for test in test_input:
            a.my_number = test
            expected['my_number'] = test
            actual = a.to_dict()
            self.assertDictEqual(actual, expected)

    def test_type_from_to_dict(self):
        """Tests the type of the values stored in the to_dict dictionary"""
        a = BaseModel()
        to_dict_result = a.to_dict()
        self.assertEqual(str, type(to_dict_result['updated_at']))
        self.assertEqual(str, type(to_dict_result['created_at']))
        self.assertEqual(str, type(to_dict_result['id']))
        self.assertEqual(str, type(to_dict_result['__class__']))

    def test_create_instance_valid(self):
        """Create an instance of BaseModel from dictionary input"""
        expected = BaseModel().to_dict()
        new = BaseModel(**expected)
        actual = new.to_dict()
        self.assertDictEqual(expected, actual)
        self.assertIsNot(expected, actual)

    def test_create_instance_partial_input_valid(self):
        """Create an instance of BaseModel from dictionary input
            that does not have all common attributes of
            BaseModel class"""

        # Only id is given
        expected = 5
        a = BaseModel(id=expected)
        self.assertEqual(a.id, str(expected))

        # Only updated_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = BaseModel(updated_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['updated_at'])

        # Only created_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = BaseModel(created_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['created_at'])

        # Variables other than the three listed were given
        expected = 'hi'
        a = BaseModel(random=expected)
        self.assertEqual(a.random, expected)

    def test_invalid_iso_string(self):
        """Tests when an invalid iso string is given"""
        invalid_str = '2017-08'
        with self.assertRaises(ValueError):
            a = BaseModel(updated_at=invalid_str)

    def test_invalid_types_created_updated(self):
        """Tests when an invalid type is given for created at
            and updated at variable"""
        invalid_types = [12, 12.4, True, None, (10, ), [1], {'hi': 5}]
        for element in invalid_types:
            a = BaseModel(created_at=element, updated_at=element)
            expected = (datetime, datetime)
            actual = (type(a.created_at), type(a.updated_at))
            self.assertEqual(expected, actual)

    def test_invalid_types_id(self):
        """Tests when non-string input is given for id"""
        invalid_types = [12, 12.4, True, None, (10, ), [1], {'hi': 5}]
        for element in invalid_types:
            a = BaseModel(id=element)
            expected = str(element)
            actual = a.id
            self.assertEqual(expected, actual)

    def test_create_instance_empty_dict(self):
        """Create an instance of BaseModel when no dictionary is used"""
        inputs = [10, 10.2, (10, ), [1], 'str', True, None]
        for element in inputs:
            a = BaseModel(element)
            self.assertEqual(BaseModel, type(a))

    def test_create_instance_invalid_dict(self):
        """Create an instance of BaseModel with invalid inputs"""
        pass
