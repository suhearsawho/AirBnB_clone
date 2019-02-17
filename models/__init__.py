#!/usr/bin/python3
"""Imports the FileStorage class"""
from models.engine.file_storage import FileStorage


storage = FileStorage()  # create filestorage obj
storage.reload()  # load data from json file
