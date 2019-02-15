#!/usr/bin/python3
"""Tests for the BaseModel class"""
import unittest
from models.base_model import BaseModel
from datetime import datetime


class Test_BaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""
    list_id = []

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
        
        test_input = [80, (80, ), 'a', {'hi': 5}, [1], 5.12]
        for test in test_input:
            a.my_number = test
            expected['my_number'] = test
            actual = a.to_dict()
            self.assertDictEqual(actual, expected)

    def test_base 
