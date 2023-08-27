"""
.. module:: contextuser
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`ContextUser` class that objects can inherit
               from to gain access to the global context.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from mojo.collections.context import Context
from mojo.collections.wellknown import ContextSingleton

class ContextUser:
    """
        Serves as a base class for all classes that need a reference to the singleton context object.
    """

    context: Context = ContextSingleton()