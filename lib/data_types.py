"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""


class Const():
    """Group of constants.

    Because Enum doesn't exist until Python 3.4.

    Use:
        >>> class Days(Const):
        >>>     mon = 'Monday'
        >>>     tue = 'Tuesday'
        >>>     wed = 'Wednesday'
        >>>     thu = 'Thursday'
        >>>     fri = 'Friday'
        >>>     sat = 'Saturday'
        >>>     sun = 'Sunday'
        >>>
        >>> today = Days.mon
        >>> print(today)
        >>> Days.all()
        >>> today in Days
    """
    @classmethod
    def all(cls):
        return (getattr(cls, m) for m in cls.__dict__ if not m.startswith('__'))