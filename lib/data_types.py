"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""


class Const():
    """
    Because Enum doesn't exist until Python 3.4.
    """
    @classmethod
    def all(cls):
        return (m for m in cls.__dict__ if not m.startswith('__'))