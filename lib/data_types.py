"""
Copyright 2015, Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
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