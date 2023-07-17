#!/usr/bin/python3
"""Defines the HBnB console"""
import re
import cmd
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

def parse(arg):
    c_braces = re.search(r"\{(.*?)\}", arg)
    s_brackets = re.search(r"\[(.*?)\]", arg)
    if c_braces is None:
        if s_brackets is None:
            return[i.strip(",") for i in arg.split()]
        else:
            lx = split(arg[:s_brackets.span()[0]])
            retl = [i.strip(",") for i in lx]
            retl.append(s_brackets.group())
            return retl
    else:
        lx = split(arg[:c_braces.span()[0]])
        retl = [i.strip(",") for i in lx]
        retl.append(c_braces.group())
        return retl

class HBNBCommand(cmd.Cmd):
    intro = 'Welcome to hbnb'
    prompt = '(hbnb)'
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }


    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False
            
              
    def do_create(self, line):
        """
        Creates a new instance of BaseModel, saves it and prints the id
        Usage: create <class>
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_"," ")
                else:
                    try:
                        value = eval(value)
                    except(SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my__list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_count(self, arg):
        """
        Usage: count <class> <class>.count()
        Retrieve the number of instances of a given class.
        """
        arglist = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arglist[0] == obj.__class__.__name__:
                count += 1
        print(count)
       

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])
            
    def do_destroy(self, arg):
        """
        Usage destroy<class> <id> or <class>.show(<id>)
        Deletes an instance of a class based on given id,
        saves changes to JSON
        """
        arglist = parse(arg)
        objdict = storage.all()
        if len(arglist) == 0:
            print("** class name missing **")
        elif arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arglist) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arglist[0], arglist[1]) not in objdict.keys:
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(arg[0], arg[1])]
            storage.save()

    def do_all(self, arg):
        """
        Usage: all or all <class> or <class>.all()
        Prints a string representation of all instances 
        of a class or all instantiated objects
        """
        arglist = parse(arg)
        if len(arglist) > 0 and arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objlist = []
            for obj in storage.all().values():
                if len(arglist) > 0 and arglist[0] == obj.__class__.__name__:
                    objlist.append(obj.__str__())
                if len(arglist) == 0:
                    objlist.append(obj.__str__())

            print(objlist)
    
    def do_update(self, arg):
        """
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        Updates an instance based on name and id by adding or changing an
        attribute.
        """
        arglist = parse(arg)
        objdict = storage.all()

        if len(arglist) == 0:
            print("** class name missing **")
            return False
        if arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arglist) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arglist[0], arglist[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(arglist) == 2:
            print("** attribute name missing **")
        if len(arglist) == 3:
            try:
                type(eval(arglist[2])) != dict
            except NameError:
                print("** value missing **")
            return False
        
        if len(arglist) == 4:
            obj = objdict["{}.{}".format(arglist[0], arglist[1])]
            if arglist[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arglist[2]])
                obj.__dict__[arglist[2]] = valtype(arglist[3])
            else:
                obj.__dict__[arglist[2]] = arglist[3]
        elif type(eval(arg[2])) == dict:
            obj = objdict["{}.{}".format(arglist[0], arglist[1])]
            for k, v in eval(arglist[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                      type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()        
 
            

    def do_EOF(self, line):
        "Exit"
        return True

    def do_quit(self,line):
        "Quit command to exit the program"
        return True

    def emptyline(self):
        "Do nothing when an empty line is passed"
        pass
        



if __name__ == '__main__':
    HBNBCommand().cmdloop()
