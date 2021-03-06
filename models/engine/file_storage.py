#!/usr/bin/python3
"""recreate a base model"""
import json


class FileStorage:
    """store data in a file"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__class__.__objects

    def new(self, obj):
        """populates dictionary"""
        from models.base_model import BaseModel

        if isinstance(obj, BaseModel) is True:
            key = "{:s}.{:s}".format(obj.__class__.__name__, str(obj.id))
            # looks like dict when printed because of __str__ method
            self.__class__.__objects[key] = obj

    def save(self):
        """convert to json"""
        with open(self.__class__.__file_path, "w+") as f:
            new_dict = {}
            for key, value in self.__class__.__objects.items():
                new_dict[key] = value.to_dict()
            f.write(json.dumps(new_dict))

    def reload(self):
        """converting JSON to obj -> store obj in dict"""
        try:
            with open(self.__class__.__file_path, "r+") as f:
                output = json.loads(f.read())
        except Exception as e:
            pass
        else:
            for key, value in output.items():
                if value['__class__'] == 'BaseModel':
                    from models.base_model import BaseModel
                    self.__class__.__objects[key] = BaseModel(**value)
                elif value['__class__'] == 'User':
                    from models.user import User
                    self.__class__.__objects[key] = User(**value)
                elif value['__class__'] == 'Place':
                    from models.place import Place
                    self.__class__.__objects[key] = Place(**value)
                elif value['__class__'] == 'State':
                    from models.state import State
                    self.__class__.__objects[key] = State(**value)
                elif value['__class__'] == 'City':
                    from models.city import City
                    self.__class__.__objects[key] = City(**value)
                elif value['__class__'] == 'Amenity':
                    from models.amenity import Amenity
                    self.__class__.__objects[key] = Amenity(**value)
                elif value['__class__'] == 'Review':
                    from models.review import Review
                    self.__class__.__objects[key] = Review(**value)
