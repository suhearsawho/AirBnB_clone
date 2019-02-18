#!/usr/bin/python3
"""entry point of command line interpreter"""
import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '
    basemodel_types = ['BaseModel', 'User', 'State', 'City', 'Amenity',
                        'Place', 'Review']
    def do_show(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (len(gary) == 1 and (gary[0] != "BaseModel" or
                                  gary[0] != "User")):
            print("** class doesn't exist **")
        elif (len(gary) == 1):
            print("** instance id missing **")
        else:
            test_dict = storage.all()
            key = gary[0] + "." + gary[1]
            if key not in test_dict.keys():
                print("** no instance found **")
            else:
                print(test_dict[key])

    def do_destroy(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (len(gary) == 1 and (gary[0] != "BaseModel" or
                                  gary[0] != "User")):
            print("** class doesn't exist **")
        elif (len(gary) == 1):
            print("** instance id missing **")
        else:
            test_dict = storage.all()
            key = gary[0] + "." + gary[1]
            if key not in test_dict.keys():
                print("** no instance found **")
            else:
                del test_dict[key]
                storage.save()

    def do_create(self, arg):
        """Creates a new instance of BaseModel (or derived) class"""
        gary = parse(arg)
        if len(gary) == 0:
            print("** class name missing **")
        elif len(gary) == 1 and gary[0] not in HBNBCommand().basemodel_types:
            print("** class doesn't exist **")
        else:
            if gary[0] == 'BaseModel': 
                new_obj = BaseModel()
            elif gary[0] == 'User':
                new_obj = User()
            elif gary[0] == 'State':
                new_obj = State()
            elif gary[0] == 'City':
                new_obj = City()
            elif gary[0] == 'Amenity':
                new_obj = Amenity()
            elif gary[0] == 'Place':
                new_obj = Place()
            elif gary[0] == 'Review':
                new_obj = Review()
            print(new_obj.id)
            new_obj.save()  # save meth from file_storage

    def do_all(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (len(gary) == 1 and (gary[0] != "BaseModel" or
                                  gary[0] != "User")):
            print("** class doesn't exist **")
        else:
            print([str(v) for (k, v) in storage.all().items()])

    def do_update(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")

        elif (len(gary) == 1 and (gary[0] != "BaseModel" or
                                  gary[0] != "User")):
            print("** class doesn't exist **")

        elif (len(gary) == 3):
            print("** attribute name missing **")

        elif (len(gary) == 4):
            print("** value missing **")

        else:
            test_dict = storage.all()
            key = gary[0] + "." + gary[1]
            if key not in test_dict.keys():
                print("** no instance found **")
            else:
                test_dict = storage.all()
                key = gary[0] + "." + gary[1]
                if key in test_dict:
                    setattr(test_dict[key], gary[3], gary[4])
                    storage.save()

    def emptyline(self):
        """do nothing on empty line"""
        pass

    def do_EOF(self, s):
        """exit interpreter"""
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(str, arg.split()))

if __name__ == '__main__':
    HBNBCommand().cmdloop()
