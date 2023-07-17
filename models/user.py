#!/usr/bin/python3
"""
Class User inherits from BaseModel
"""

from models.base_model import BaseModel
import json

class User(BaseModel):
    """
    A sub class of BaseModel
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""    
