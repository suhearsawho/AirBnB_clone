#!/usr/bin/python3
"""Review attributes"""
from models.base_model import BaseModel
from models.place import Place
from models.user import User


class Review(BaseModel):
    place_id = "{}.{}".format(Place.name, self.id)
    user_id = "{}.{}".format(User.name, self.id)
    text = ""

r = Review(BaseModel)
print(r)
