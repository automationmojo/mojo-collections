
import unittest

from mojo.collections.mergemap import MergeMap

class TestMergeMap(unittest.TestCase):

    map_zero = {
        "a": {
            "a": "a"
        }
    }

    map_one = {
        "a": {
            "a": {
                "a": "aa",
                "z": "zz"
            },
            "b" : {
                "b": "bb",
                "c": "cc"
            }
        }
    }

    map_two = {
        "a": {
            "a": {
                "a": "aa",
                "z": "zz"
            },
            "e" : {
                "c": "aa",
                "d": "dd"
            }
        },
        "e": {
            "f": {
                "g": "gg",
                "h": "hh"
            }
        }
    }

    map_with_list_a = {
        "merge-list": [
            "a",
            "b",
            "c"
        ]
    }

    map_with_list_b = {
        "merge-list": [
            "c",
            "d",
            "e"
        ]
    }

    path_map_with_list_a = {
        "root": {
            "merge-list": [
                "a",
                "b",
                "c"
            ]
        }
    }

    path_map_with_list_b = {
        "root": {
            "merge-list": [
                "c",
                "d",
                "e"
            ]
        }
    }

    def test_map_shadows_value(self):

        mm = MergeMap(self.map_two, self.map_one, self.map_zero)

        ma = mm["a"]
        maa = ma["a"]

        errmsg =  "The map_two value should be the priority value."
        self.assertTrue(isinstance(maa, dict), errmsg)

        aval = maa["a"]
        self.assertTrue(aval == "aa", errmsg)

        zval = maa["z"]
        self.assertTrue(zval== "zz", errmsg)
        return
    
    def test_value_shadows_map(self):

        mm = MergeMap(self.map_zero, self.map_one, self.map_two)
        ma = mm["a"]
        maa = ma["a"]

        self.assertTrue(maa == "a", "The map_zero value should be the priority value.")
        return

    def test_list_merge(self):

        mm = MergeMap(self.map_with_list_a, self.map_with_list_b)

        mrglist = mm["merge-list"]

        self.assertEqual(len(mrglist), 5)

        return


if __name__ == '__main__':
    unittest.main()
