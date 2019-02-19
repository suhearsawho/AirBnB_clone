#!/usr/bin/python3
"""tests for state class"""
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.state import State
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

    def test_create(self):
        """create instance of state class"""
        my_state1 = State()
        self.assertEqual(str, type(my_state1.id))
        self.assertEqual(datetime, type(my_state1.created_at))
        self.assertEqual(datetime, type(my_state1.updated_at))

    def test_to_dict(self):
        """test that to_dict creates dict"""
        my_state = State()
        my_state.name = "bobo"
        test_dict = my_state.to_dict()
        self.assertEqual(dict, type(test_dict))

        capture = {k: v for k, v in my_state.__dict__.items()}
        capture['__class__'] = 'State'
        capture['updated_at'] = capture['updated_at'].isoformat()
        capture['created_at'] = capture['created_at'].isoformat()
        actual = my_state.to_dict()
        self.assertDictEqual(capture, actual)
        actual['cat'] = 2
        self.assertEqual(actual['cat'], 2)
        self.assertEqual(actual['name'], "bobo")

        """test type of values in to_dict"""
        self.assertEqual(str, type(capture['__class__']))
        self.assertEqual(str, type(capture['updated_at']))
        self.assertEqual(str, type(capture['created_at']))

    def test_unique_values(self):
        """test each state has unique values"""
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)
        self.assertNotEqual(state1.created_at, state2.created_at)
        self.assertNotEqual(state1.updated_at, state2.updated_at)
        self.assertEqual(state1.name, state2.name)

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
        my_state = State()
        org_created = my_state.created_at.isoformat()
        org_updated = my_state.updated_at.isoformat()
        my_state.save()
        new_created = my_state.created_at.isoformat()
        new_updated = my_state.updated_at.isoformat()
        self.assertNotEqual(org_updated, org_created)
        self.assertEqual(org_created, new_created)

    def test_check_save(self):
        """check save writes to file"""
        storage = FileStorage()
        my_state1 = State()
        my_state1.save()
        len_dict1 = len(storage.all())
        my_state2 = State()
        my_state2.save()
        len_dict2 = len(storage.all())
        self.assertNotEqual(len_dict1, len_dict2)

    def test_create(self):
        """create instance of State from kwargs"""
        storage = FileStorage()
        state1 = State(created_at = "2017-06-14T22:31:03.285259", heads = 4,
                      updated_at = "2017-06-14T22:31:03.285259", id = 3434)
        self.assertEqual(state1.heads, 4)
        _dict = storage.all()  # store __object dict
        test_list = [k for k in _dict.keys()]
        key = "State." + str(state1.id)
        self.assertIn(key, test_list)
        state1.name = "sam"
        self.assertEqual(state1.name, "sam")

    def test_invalid_initialization(self):
        """create State instance in illegal ways"""
        storage = FileStorage()
        state1 = State(None)
        self.assertEqual(str, type(state1.id))
        self.assertEqual(datetime, type(state1.created_at))
        state2 = State(id = "ball")
        self.assertEqual(str, type(state2.id))
        self.assertEqual(datetime, type(state2.created_at))

    def test_create_instance_partial_input_valid(self):
        """Create an instance of BaseModel from dictionary input
        that does not have all common attributes of
        BaseModel class"""

        # Only id is given
        expected = 5
        a = State(id=expected)
        self.assertEqual(a.id, expected)

        # Only updated_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = State(updated_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['updated_at'])

        # Only created_at is given
        expected = '2017-09-28T21:03:54.052302'
        a = State(created_at=expected)
        actual = a.to_dict()
        self.assertEqual(expected, actual['created_at'])

        # Variables other than the three listed were given
        expected = 'hi'
        a = State(random=expected)
        self.assertEqual(a.random, expected)

    def test_create_instance_empty_dict(self):
        """Create an instance of BaseModel when no dictionary is used"""
        inputs = [10, 10.2, (10, ), [1], 'str', True, None]
        for element in inputs:
            a = State(element)
            self.assertEqual(State, type(a))
