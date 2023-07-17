#!/usr/bin/python3
"""
Defines state class, inherits from BaseModel
"""
from models.base_model import BaseModel


class State(BaseModel):
    """
    Sub-class of BaseModel
    Public class attribute
          name(str)
    """
    name = ""
