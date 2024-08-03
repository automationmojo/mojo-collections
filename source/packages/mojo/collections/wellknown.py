"""
.. module:: wellknown
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`Context` singleton instance and factory.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from mojo.collections.context import Context
from mojo.collections.singletons import SINGLETON_LOCK


CONTEXT_SINGLETON = None


def ContextSingleton() -> Context:
    """
        Instantiates and gets a global instance of the :class:`Context` class.  The global
        :class:`Context` allows for easy sharing of a global context and configuration map.
    """
    global SINGLETON_LOCK
    global CONTEXT_SINGLETON

    # If the singleton is already set, don't bother grabbing a lock
    # to set it.  The full path of the setting of the singleton will only
    # ever be taken once
    SINGLETON_LOCK.acquire()
    try:
        if CONTEXT_SINGLETON is None:
            CONTEXT_SINGLETON = Context()
    finally:
        SINGLETON_LOCK.release()

    return CONTEXT_SINGLETON
