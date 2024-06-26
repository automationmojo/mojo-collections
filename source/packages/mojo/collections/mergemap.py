"""
.. module:: mergemap
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`MergeMap` object which is similar to
               a :class:`ChainMap` but which allows shadowed results for descendent
               leaves.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from typing import Any, Iterable, List, Optional, MutableMapping

import json
import re
import reprlib

from collections import ChainMap

REGEX_PATH_VALIDATOR = re.compile("/{1}([-a-zA-Z0-9_]+)")


def validate_path_name(path: str) -> List[str]:
    """
        Validates a context pathname.

        :param path: The path to validate and determine its parts.

        :returns: The seperate parts of the path provided.
    """

    parts = None
    mobj = REGEX_PATH_VALIDATOR.findall(path)
    if mobj is not None:
        parts = list(mobj)

    return parts
class MergeMap(MutableMapping):

    def __init__(self, *maps: List[MutableMapping]):
        self.maps: List[MutableMapping] = [m for m in maps]
        return

    def clear(self):
        """
            Clears all maps.
        """
        self.maps = []
        return

    def copy(self):
        """
            New MergeMap or subclass with a new copy of maps[0] and refs to maps[1:]
        """
        cpy_maps = [nm.copy() for nm in self.maps]
        nmm = self.__class__(*cpy_maps)
        return nmm

    def flatten(self) -> dict:
        """
            Flattens the Merge dictionary into a flat representation of
            the combined keys and values of the maps.
        """
        fd = {}

        all_keys = self.keys()
        if len(all_keys):
            for k, v in self.items():
                if isinstance(v, MergeMap):
                    v = v.flatten()
                fd[k] = v

        return fd

    @classmethod
    def fromkeys(cls, iterable, *args):
        """
            Create a MergeMap with a single dict created from the iterable.
        """
        nm = cls(dict.fromkeys(iterable, *args))
        return nm

    def get(self, key: str, default=None):
        """
            Gets the value for a key or returns the specified default value.
        """
        rtnval = self[key] if key in self else default
        return rtnval

    def keys(self) -> Iterable[str]:
        """
            Gets the top level possible keys that can be used to query this merge map.
        """

        mks = set()

        for nm in self.maps:
            mks.update(nm.keys())
        
        return mks
    

    def new_child(self, m: Optional[dict]=None, **kwargs):      # like Django's Context.push()
        """
            New MergeMap with a new map followed by all previous maps.
            If no map is provided, an empty dict is used.
            Keyword arguments update the map or new empty dict.
        """
        if m is None:
            m = kwargs
        elif kwargs:
            m.update(kwargs)
        
        cpy_maps = [nm.copy() for nm in self.maps]

        ncm = self.__class__(m, *cpy_maps)

        return ncm
    
    def _process_candidates(self, candidates: List[Any]) -> Any:

        rtnval = None

        # Check to see if the mapping values at this level are the same type and can be merged
        first_type = type(candidates[0])

        if first_type == dict or first_type == list or first_type == tuple:
            has_common_type = True

            for nxtitem in candidates:
                nxttype = type(nxtitem)
                if nxttype != first_type:
                    has_common_type = False
                    break

            # If we found a common type with the same key, we can merge
            if has_common_type:
                
                if first_type == list or first_type == tuple:

                    cmplist = []
                    merged_list = []
                    for nxtcand in candidates:

                        for nxtval in nxtcand:

                            if isinstance(nxtval, list) or isinstance(nxtcand, tuple):
                                cmpval = [v for v in nxtval]
                                cmpval = json.dumps(cmpval.sort())

                            elif isinstance(nxtval, dict):
                                cmpval = json.dumps(nxtval, sort_keys=True)
                            
                            else:
                                cmpval = nxtval
                            
                            if cmpval not in cmplist:
                                cmplist.append(cmpval)
                                merged_list.append(nxtval)

                    rtnval = merged_list

                elif first_type == dict:
                    mmap = MergeMap(*candidates)
                    rtnval = mmap

            else:
                rtnval = candidates[0]

        else:
            rtnval = candidates[0]

        return rtnval
 
    def __bool__(self):
        return any(self.maps)

    def __contains__(self, key: str):
        haskey = False
        
        for mapping in self.maps:
            if key in mapping:
                haskey = True
                break

        return haskey

    __copy__ = copy
    
    def __delitem__(self, key):
        kfound = False

        for nm in self.maps:
            if key in nm:
                kfound = True
                del nm[key]
        
        if kfound is not None:
            raise KeyError(f'Key not found in the first mapping: {key!r}')

        return

    def __getitem__(self, key: str):

        rtnval = None

        candidates = []

        for nxtmap in self.maps:
            if key in nxtmap:
                mval = nxtmap[key]
                candidates.append(mval)

        if len(candidates) == 0:
            self.__missing__(key)
        elif len(candidates) == 1:
            rtnval = candidates[0]
        else:
            rtnval = self._process_candidates(candidates)

        return rtnval         

    def __iter__(self):
        mks = self.keys()
        return iter(mks)

    def __len__(self):
        """
            Get the length of all possible keys.
        """
        rtnval = len(self.keys())
        return rtnval

    def __missing__(self, key: str):
        raise KeyError(key)

    @reprlib.recursive_repr()
    def __repr__(self):
        rval = f'{self.__class__.__name__}({", ".join(map(repr, self.maps))})'
        return rval

    def __setitem__(self, key, value):

        if len(self.maps) == 0:
            self.maps.append({})

        self.maps[0][key] = value

        return


