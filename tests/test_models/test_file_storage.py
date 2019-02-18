#!/usr/bin/python3
"""TestFileStorage class"""
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import json
import os
import unittest


class TestFileStorage(unittest.TestCase):
    """Unit tests for FileStorage class"""

    def setUp(self):
        """Setup for all tests that will be run"""
        # Delete file.json
        try:
            with open('file.json', 'w+') as f:
                os.remove('file.json')
        except Exception as e:
            pass

        # Empty __objects dictionary in FileStorage
        a = FileStorage().all()
        keys = list(a.keys())
        for value in keys:
            del a[value]

    def test_all_method_when_empty(self):
        """Tests the return value of all when no objects have been saved"""
        a = FileStorage()
        expected = {}
        actual = a.all()
        self.assertDictEqual(expected, actual)

    def test_all_method_when_not_empty(self):
        """Tests the return value of all when objects have been saved"""
        a = BaseModel()
        a.save()
        a_id = 'BaseModel' + '.' + a.id
        expected = {a_id: a}
        actual = FileStorage().all()
        self.assertDictEqual(expected, actual)

        b = BaseModel()
        b.save()
        b_id = 'BaseModel' + '.' + b.id
        expected = {a_id: a, b_id: b}
        actual = FileStorage().all()
        self.assertDictEqual(expected, actual)

    def test_new_method(self):
        """Tests that new sets the value in __objects with the key
            in the form <obj class name>.id"""
        a = BaseModel()
        storage = FileStorage()
        storage.new(a)

        a_id = a.__class__.__name__ + '.' + a.id
        expected = {a_id: a}
        actual = FileStorage().all()
        self.assertDictEqual(expected, actual)

    def test_new_method_invalid_types(self):
        """Tests that objects that are not instances derived from BaseModel
            will not be saved with new method"""
        input_data = [10, 10.2, (10, ), [124, 1], 'a', {'hi': 5}]
        storage = FileStorage()
        expected = {}
        for value in input_data:
            storage.new(value)
            actual = FileStorage().all()
            self.assertDictEqual(expected, actual)

    def test_save_method_valid(self):
        """Tests that the save method correctly serializes __objects"""
        storage = FileStorage()
        a = BaseModel()
        a.save()
        a_to_dict = a.to_dict()
        expected = {a.__class__.__name__ + '.' + a.id:
                    a.to_dict()}
        storage.save()
        with open('file.json', 'r+') as f:
            actual = json.loads(f.read())
            self.assertDictEqual(expected, actual)

    def test_reload_method_valid(self):
        """Tests that the reload method correctly deserializes JSON file
            when file exists"""
        storage = FileStorage()
        a = BaseModel()
        b = BaseModel()
        a.save()
        b.save()
        storage.save()
        del a, b

        # Check that json file exists now
        self.assertEqual(True, os.path.exists('file.json'))
        storage.reload()

        # Check that restored values are equivalent to the original
        new_instances = storage.all()
        for key, value in new_instances.items():
            self.assertEqual(type(value), BaseModel)

    def test_reload_method_no_file(self):
        """Tests that the reload method does not raise an error when
            JSON file does not exist"""

        storage = FileStorage()
        self.assertEqual(False, os.path.exists('file.json'))
