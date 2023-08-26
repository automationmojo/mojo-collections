"""
.. module:: wellknown
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`Context` singleton instance and factory.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from threading import RLock

from mojo.collections.context import Context

CONTEXT_SINGLETON = None

SINGLETON_LOCK = RLock()

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
    if CONTEXT_SINGLETON is None:
        SINGLETON_LOCK.acquire()
        try:
            if CONTEXT_SINGLETON is None:
                CONTEXT_SINGLETON = Context()
        finally:
            SINGLETON_LOCK.release()

    return CONTEXT_SINGLETON
