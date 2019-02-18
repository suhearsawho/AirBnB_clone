#!/usr/bin/python3
"""create user class inherits from BaseModel"""
from models.base_model import BaseModel


class User(BaseModel):
    """Defines the user class"""

    """Public Class Attributes"""
    email = ''
    password = ''
    first_name = ''
    last_name = ''

    def __init__(self):
        """Initialize variables"""
        super().__init__()
