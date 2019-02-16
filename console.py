#!/usr/bin/python3
"""entry point of command line interpreter"""
import cmd, sys
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_show(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (len(gary) == 1 and gary[0] != "BaseModel" and gary[0] != "User"):
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
        elif (len(gary) == 1 and gary[0] != "BaseModel" and gary[0] != "User"):
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
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (len(gary) == 1 and gary[0] != "BaseModel" and gary[0] != "User"):
            print("** class doesn't exist **")
        elif (gary[0] == "User"):
            new_obj = User()
            print(new_obj.id)
            new_obj.save()  # save meth from file_storage
        else:
            new_obj = BaseModel()
            print(new_obj.id)
            new_obj.save()  # save meth from file_storage

    def do_all(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")
        elif (len(gary) == 1 and gary[0] != "BaseModel" and gary[0] != "User"):
            print("** class doesn't exist **")
        else:
            print([str(v) for (k, v) in storage.all().items()])

    def do_update(self, arg):
        gary = parse(arg)
        if (len(gary) == 0):
            print("** class name missing **")

        elif (len(gary) == 1 and gary[0] != "BaseModel" and gary[0] != "User"):
            print("** class doesn't exist **")

        elif (len(gary) == 3):
            print("** no instance found **")

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
                    print(test_dict[key].__dict__)

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
