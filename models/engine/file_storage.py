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
        key = "{:s}.{:s}".format(obj.__class__.__name__, str(obj.id))
        self.__objects[key] = obj

    def save(self):
        """convert to json"""
        # we need to first get the original dictionary stored in the json file
        # then, add our new addition to this dictionary
        with open(self.__file_path, "a+") as f:
            for key, value in self.__objects.items():
                self.__objects[key] = value.to_dict()
            f.write(json.dumps(self.__objects))

    def reload(self):
        """converting JSON to obj -> store obj in dict"""
        try:
            with open(self.__file_path, "r+") as f:
                output = json.loads(f.read())
        except Exception as e:
            print(e)
        else:
            for key, value in output.items():
                from models.base_model import BaseModel
                if value['__class__'] == 'BaseModel':
                    self.__objects[key] = BaseModel(**value)
