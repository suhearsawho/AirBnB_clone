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
    base_types = ['BaseModel', 'User', 'State', 'City', 'Amenity',
                  'Place', 'Review']

    @staticmethod
    def determine_type(arg):
        string_char = ['"', "'"]
        for character in arg:
            if character in string_char:
                return 'str'
            if ord(character) < ord('0') or ord(character) > ord('9'):
                return 'str'
        if '.' in list[arg]:
                return 'float'
        return 'int'
    
    def do_show(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (len(gary) == 1 and gary[0] not in HBNBCommand().base_types):
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
        elif (len(gary) == 1 and gary[0] not in HBNBCommand().base_types):
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
        elif len(gary) == 1 and gary[0] not in HBNBCommand().base_types:
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
        if len(gary) == 0:
            print([str(v) for k, v in storage.all().items()])
        elif len(gary) == 1 and gary[0] not in HBNBCommand().base_types:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in storage.all().items()
                    if v.__class__.__name__ == gary[0]])

    def do_update(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (len(gary) == 1 and gary[0] not in HBNBCommand().base_types):
            print("** class doesn't exist **")
        elif len(gary) == 1:
            print("**instance id missing **")
        else:
            test_dict = storage.all()
            key = gary[0] + "." + gary[1]
            if key not in test_dict.keys():
                print("** no instance found **")
            else:
                if (len(gary) == 2):
                    print("** attribute name missing **")
                elif (len(gary) == 3):
                    print("** value missing **")
                else:
                    key = gary[0] + "." + gary[1]
                    if key in test_dict:
                        arg_type = self.determine_type(gary[3])
                        if arg_type == 'str':
                            setattr(test_dict[key], gary[2], str(gary[3]))
                        elif arg_type == 'int':
                            setattr(test_dict[key], gary[2], int(gary[3]))
                        elif arg_type == 'float':
                            setattr(test_dict[key], gary[2], float(gary[3]))
                        test_dict[key].save()
                        print(test_dict[key]) 
        
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
