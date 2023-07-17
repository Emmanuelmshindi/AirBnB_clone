#!/usr/bin/python3
"""
HolbertonBnB project file storage
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """
    Storage engine for the airbnb clone project.
    Class attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): Dictionary of instantiated objects.
        class_dict (dict): Dictionary of all the classes.

    Class methods:
        all: Returns the object
        new: updates the dictionary id
        save: Serializes, or converts Python objects into JSON strings
        reload: Deserializes, or converts JSON strings into Python objects.
    """
    __file_path = 'file.json'
    __objects = {}
    class_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "Amenity": Amenity, "City": City, "Review": Review,
                  "State": State}

    def all(self):
        '''Return a dictionary of <class>.<id> : instance'''
        return self.__objects

    def new(self, obj):
        '''Set new __objects to existing dic of instances '''
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj 

    def save(self):
        '''Save/serialize object dictionaries to JSON file '''
        obj_dict = {}

        for key, obj in self.__objects.items():
            obj_dict[key] = obj.to_dict()

        with open(self.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserialize/convert obj dicts back to instances, if it exists"""
        try:
            with open(self.__file_path, 'r') as f:
                new_obj_dict = json.load(f)
            for key, value in new_obj_dict.items():
                obj = self.class_dict[value['__class__']](**value)
                self.__objects[key] = obj
        except Exception:
            pass
