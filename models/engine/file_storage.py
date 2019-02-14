#!/usr/bin/python3
"""recreate a base model"""
import json

class FileStorage:
    """store data in a file"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """populates dictionary"""
        __objects[obj.__class__.__name__ + "." + str(BaseModel.id)] = obj

    def save(self):
        """convert to json"""
        with open("file.json", "a+") as f:
            f.append(json.dumps(self.__objects))

    def reload(self):
        """converting JSON to obj -> store obj in dict"""
        try:
            with open("file.json", "r") as f:
                self.__objects.update(json.loads(f.read()))
        except Exception:
            pass
