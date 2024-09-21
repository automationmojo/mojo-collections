 
from typing import Dict, List, Any, Optional, Union, Iterable

import re

from collections import ChainMap
from weakref import ReferenceType

from mojo.collections.mergemap import MergeMap


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


class DictMap:
    """
        The :class:`DictMap` object is used to provide a file system like interface to working with dictionary oriented
        objects.  The :class:`DictMap` provides special methods (exists, insert and lookup).  That are used with path
        based strings used to lookup values.  The :class:`DictMap` uses paths that use '/' as a path seperator.  All paths
        must also begin with '/'.

        Examples:
            dm.insert("/a/b/c", "some value")

            val = dm.lookup("/a/b/c", default="default value")
         
    """

    def __init__(self, store: Dict[str, Any], path: Optional[str] = "/", root_ref: Optional[ReferenceType["DictMap"]] = None):
        self._store = store
        self._path = path
        self._root_ref = root_ref
        return


    @property
    def is_root(self) -> bool:
        rtnval = True if self._root_ref is not None else False
        return rtnval


    @property
    def root(self) -> "DictMap":
        rtnval = None

        if self._root_ref is not None:
            rtnval = self._root_ref()
        else:
            rtnval = self
        
        return rtnval


    def exists(self, path: str) -> bool:
        """
            Checks to see if a value exists at the path specified.

            :param path: Path where the object is to be inserted

            :returns: A boolean indicating if the specified path contains a value
        """

        if isinstance(path, (list, tuple)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))
        
        found = self._exists(self._store, path, path_parts)

        return found


    def insert(self, path: str, obj: Any):
        """
            Insert an object at the path specified.

            :param path: Path where the object is to be inserted
            :param obj: The object to insert

            :raises: :class:`ValueError`
        """
        if isinstance(path, (list, tuple)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))

        self._insert(path=path, sref=self._store, path_parts=path_parts, obj=obj)

        return


    def lookup(self, path: Union[str, Iterable[str]], default: Optional[Any]=None, raise_error: bool=True) -> Union["DictMap", Iterable[Any], Any]:
        """
            Lookup an object at the path specified.

            :param path: Path where the desired object is located.

            :returns: The object stored at the specified path.

            :raises: :class:`LookupError`
        """
        found = None

        try:
            if isinstance(path, (list, tuple)):
                path_parts = path
                path = "/%s" %  "/".join(path_parts)
            else:
                path_parts = validate_path_name(path.rstrip("/"))

            found = self._lookup(path=path, sloc=[], sref=self._store, path_parts=path_parts, default=default)
        except LookupError:
            if raise_error:
                raise

        return found


    def remove(self, path: str) -> Any:
        """
            Remove an object at the specified path

            :param path: Path where the desired object is located.

            :returns: The being removed from the specified path.

            :raises: :class:`LookupError`
        """
        found_node = None

        if isinstance(path, (list, tuple)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))

        found_node = self._remove(path=path, sref=self._store, path_parts=path_parts)

        return found_node


    def _exists(self, dref: dict, path: str, path_parts: List[str]) -> bool:

        found = False

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in dref:
                found_node = dref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found_node, (dict, ChainMap, MergeMap)):
                        found = self._exists(found_node, path, path_parts[1:])
                else:
                    found = True

        return found


    def _insert(self, *, path: str, sref: dict, path_parts: List[str], obj: Any) -> Any:

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if len(path_parts) > 1:
                if leaf_name not in sref:
                    sref[leaf_name] = {}
                found = sref[leaf_name]
                self._insert(path=path, sref=found, path_parts=path_parts[1:], obj=obj)
            else:
                sref[leaf_name] = obj
        else:
            raise ValueError("Invalid path=%s" % path)

        return


    def _lookup(self, *, path: str, sloc: List[str], sref: dict, path_parts: List[str], default: Optional[Any]=None) -> Any:

        found = None

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in sref:
                found = sref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found, (dict, ChainMap, MergeMap)):
                        floc = sloc + path_parts[:1] 
                        found = self._lookup(path=path, sloc=floc, sref=found, path_parts=path_parts[1:], default=default)
                    else:
                        raise LookupError("Context lookup failure for path=%s" % path)
                else:
                    if isinstance(found, (dict, ChainMap, MergeMap)):
                        cpath = "/" + "/".join(path_parts)
                        root_ref = ReferenceType(self) if self._root_ref is None else self._root_ref
                        found = DictMap(found, path=cpath, root_ref=root_ref)
            elif default is not None:
                if len(path_parts) > 1:
                    found = {}
                    sref[leaf_name] = found
                    floc = sloc + path_parts[:1]
                    found = self._lookup(path=path, sloc=floc, sref=found, path_parts=path_parts[1:], default=default)
                else:
                    sref[leaf_name] = default
                    if isinstance(default, dict, ChainMap, MergeMap):
                        cpath = "/" + "/".join(path_parts)
                        root_ref = ReferenceType(self) if self._root_ref is None else self._root_ref
                        found = DictMap(default, path=cpath, root_ref=root_ref)
                    else:
                        found = default
            else:
                raise LookupError("Context lookup failure for path=%s" % path)
        else:
            raise ValueError("Invalid path=%s" % path)

        return found


    def _remove(self, *, path: str, sref: dict,  path_parts: List[str]) -> Any:

        found = None

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in sref:
                found = sref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found, (dict, ChainMap, MergeMap)):
                        found = self._remove(path=path, sref=found, path_parts=path_parts[1:])
                    else:
                        raise LookupError("Context remove failure for path=%s" % path)
                else:
                    del sref[leaf_name]
            else:
                raise LookupError("Context remove failure for path=%s" % path)
        else:
            raise ValueError("Invalid path=%s" % path)

        return found


    def __contains__(self, key: str) -> bool:
        found = self.exists(key)
        return found


    def __getitem__(self, key: str) -> Any:
        found_node = self._lookup(self._store, key, [key])
        return found_node


    def __setitem__(self, key: str, val: Any):
        self._insert(self._store, key, [key], val)
        return


if __name__ == "__main__":
    
    testdict = {
        "a": { "a" : 1 },
        "b": 2,
        "c": { "a": { "a": 1, "b": 2}}
    }

    dfs = DictMap(testdict)

    print(dfs.lookup("/a/a"))
    print(dfs.lookup("/c/a/b"))

    cc = dfs.lookup("/c")
    print(cc.lookup("/a/b"))
