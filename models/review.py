#!/usr/bin/python3
"""Review attributes"""
from models.base_model import BaseModel
from models.place import Place
from models.user import User


class Review(BaseModel):
    """Defines the class Review"""
    place_id = ""
    user_id = ""
    text = ""
