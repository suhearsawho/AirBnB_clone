#!/user/bin/python3
"""city class"""
from models.base_model import BaseModel
from models.state import State

class City(BaseModel):
    state_id = ""
    name = ""
