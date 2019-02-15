#!/usr/bin/python3
"""entry point of command line interpreter"""
import cmd, sys

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """do nothing on empty line"""
        pass

    def do_EOF(self, s):
        """exit interpreter"""
        return True

if __name__ == '__main__':
    HBNBCommand().cmdloop()
