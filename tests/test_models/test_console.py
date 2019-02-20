#!/usr/bin/python3
"""unit test the console"""
import io
import unittest
from cmd import Cmd
from console import HBNBCommand
from contextlib import redirect_stdout
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class Test_BaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def setup(self):
        """Setup for all tests that will be run"""
        # Delete file.json
        try:
            with open('file.json', 'w+') as f:
                f.write('')
        except Exception as e:
            pass

    def test_all(self):
        """test the all method in console"""
        cmd_obj = HBNBCommand()  # create cmd obj
        f = io.StringIO()  # create string io obj
        new_model1 = BaseModel()
        with redirect_stdout(f):
            cmd_obj.onecmd("all")
        self.assertEqual(type(f.getvalue()), str)
        d = io.StringIO()
        new_model2 = BaseModel()
        with redirect_stdout(d):
            cmd_obj.onecmd("all Basemodel")
        self.assertEqual(type(d.getvalue()), str)
        self.assertNotEqual(d.getvalue(), f.getvalue())

    def test_create(self):
        """test the create method in console"""
        cmd_obj = HBNBCommand()
        f = io.StringIO()
        new_model1 = BaseModel()
        with redirect_stdout(f):
            cmd_obj.onecmd("Create User")
            cmd_obj.onecmd("all User")
        self.assertEqual(str, type(f.getvalue()))
        save_len = len(f.getvalue())
        new_model2 = BaseModel()
        with redirect_stdout(f):
            cmd_obj.onecmd("Create User")
            cmd_obj.onecmd("all User")
        print(f.getvalue())
        self.assertNotEqual(len(f.getvalue()), save_len)
"""
    def test_show(self):
        cmd_obj = HBNBCommand()
        f = io.StringIO()
        new_model1 = BaseModel()
        new_model2 = BaseModel()
        with redirect_stdout(f):
            cmd_obj.onecmd("Show User")
        self.assertEqual(type(f.getvalue()), str)

    def test_destroy(self):
        cmd_obj = HBNBCommand()
        f = io.StringIO()
        new_model1 = BaseModel()
        new_model2 = BaseModel()
        with redirect_stdout(f):
            cmd_obj.onecmd("Destroy User")
        self.assertEqual(type(f.getvalue()), str)

    def test_update(self):
        cmd_obj = HBNBCommand()
        f = io.StringIO()
        new_model1 = BaseModel()
        new_model2 = BaseModel()
        with redirect_stdout(f):
            cmd_obj.onecmd("Update User  ")
        self.assertEqual(type(f.getvalue()), str)

    def test_default(self):
        cmd_obj = HBNBCommand()
        f = io.StringIO()
        new_model1 = BaseModel()
        new_model2 = BaseModel()
        with redirect_stdout(f):
            cmd_obj.onecmd("")
        self.assertEqual(type(f.getvalue()), str)"""
