#!/usr/bin/python3
"""entry point of command line interpreter"""
import cmd
import sys

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """class for console in Airbnb project"""
    prompt = '(hbnb) '
    base_types = ['BaseModel', 'User', 'State', 'City', 'Amenity',
                  'Place', 'Review']

    @staticmethod
    def determine_type(arg):
        """Determine the type of the argument to update"""
        if arg[0] in ['"', "'"]:
            return 'str'
        for character in arg:
            if (ord(character) != ord('.') and
                    (ord(character) < ord('0') or ord(character) > ord('9'))):
                return 'str'
        if '.' in list(arg):
            return 'float'
        return 'int'

    @staticmethod
    def string_input(raw_list):
        """Create the final string input for setattr in do_update"""
        raw = raw_list[3]
        final = ''
        raw_len = len(raw)
        len_list = len(raw_list)
        for i in range(raw_len):
            if ((i != 0 or raw[i] not in ['"', "'"]) and
                    (i != raw_len - 1 or raw[i] not in ['"', "'"])):
                if raw[i] == "'":
                    final += '\''
                else:
                    final += raw[i]
        if raw[0] == '"' and raw[-1] != '"' and len_list > 4:
            for raw_str in raw_list[4:]:
                final += ' '
                for i in raw_str:
                    if i != '"':
                        final += i
        return final

    def do_show(self, arg):
        """Show the specified instance of the class"""
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (gary[0] not in HBNBCommand().base_types):
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
        """Destroy specified instance"""
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (gary[0] not in HBNBCommand().base_types):
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
        elif gary[0] not in HBNBCommand().base_types:
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
            new_obj.save()  # save meth from file_storage
            print(new_obj.id)

    def do_all(self, arg):
        """Show all models under specified class"""
        gary = parse(arg)
        if len(gary) == 0:
            print([str(v) for k, v in storage.all().items()])
        elif gary[0] not in HBNBCommand().base_types:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in storage.all().items()
                   if v.__class__.__name__ == gary[0]])

    def do_update(self, arg):
        """Update the specified instance"""
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif gary[0] not in HBNBCommand().base_types:
            print("** class doesn't exist **")
        elif len(gary) == 1:
            print("** instance id missing **")
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
                            final = self.string_input(gary)
                            setattr(test_dict[key], gary[2], final)
                        elif arg_type == 'int':
                            setattr(test_dict[key], gary[2], int(gary[3]))
                        elif arg_type == 'float':
                            setattr(test_dict[key], gary[2], float(gary[3]))
                        test_dict[key].save()

    def default(self, arg):
        """Default behavior when argument format is not recognized by cmd"""
        class_name = ''
        cmd_name = ''
        arguments = ''

        before_period = True
        before_arg = True
        for element in arg:
            if before_period is True:
                if element == '.':
                    before_period = False
                else:
                    class_name += element
            else:
                if before_arg is True:
                    if element == '(':
                        before_arg = False
                    else:
                        cmd_name += element
                else:
                    if element != ')':
                        if element not in ['"', "'"]:
                            arguments += element

        final = class_name + ' ' + arguments
        print(final)
        if cmd_name == 'all':
            self.do_all(final)
        elif cmd_name == 'show':
            self.do_show(final)
        elif cmd_name == 'destroy':
            self.do_destroy(final)
        elif cmd_name == 'update':
            self.do_update(final)

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
    """Convert a series of zero or more numbers to an argument tuple"""
    return tuple(map(str, arg.split()))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
