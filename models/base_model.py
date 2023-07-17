#!/usr/bin/python3
import models
from uuid import uuid4
from datetime import datetime

"""
Parent class to all classes in the HolbertonBnB project
"""

class BaseModel:
    """
    Defines common attributes and methods for all other classes
    Methods:
        __init__(self, *args, **kwargs)
        __str__(self)
        __save(self)
        __repr__(self)
        to_dict(self)
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize attributes uuid and datetime when instance is created/updated
        """
        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        if kwargs:
            for key, value in kwargs.items():
                if "created_at" == key:
                    self.created_at = datetime.strptime(kwargs["created_at"], date_format)
                elif "updated_at" == key:
                    self.updated_at = datetime.strptime(kwargs["created_at"], date_format)
                elif "__class__" == key:
                    pass
                else:
                    setattr(self, key, value)

        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
    
    def save(self):
        """
        Updates updated_at with the current time and saves
        to serialized file
        """
        self.updated_at = datetime.now()
        models.storage.save()
    
    def to_dict(self):
        """
        Return dictionary representation of BaseModel and string representation of datetime
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict

    def __str__(self):
        """
        Returns, classname, id, and the dictionary
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__) 

    def __repr__(self):
        """Returns string's repr"""
        return(self.__str__())
