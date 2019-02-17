#!/usr/bin/python3
"""create user class inherits from BaseModel"""
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

class User(BaseModel):
    email = ""
    password = ""
    first_name = ""
    last_name = ""
