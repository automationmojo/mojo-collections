
import unittest

from mojo.collections.wellknown import ContextSingleton

class TestContext(unittest.TestCase):

    def setUp(self) -> None:
        self._ctx = ContextSingleton()
        return

    def test_context_insert_lookup(self):

        self._ctx.insert("/a/b/c", "blah")

        val = self._ctx.lookup("/a/b/c")

        self.assertTrue(val == "blah", f"The returned context value '{val}' did not match 'blah'.")

        return
    
    def test_context_default_value_lookup(self):

        val = self._ctx.lookup("/d/e/f", default="blah")

        self.assertTrue(val == "blah", f"The returned context value '{val}' did not match 'blah'.")

        return

    def test_context_remove_value(self):

        self._ctx.insert("/a/b/c", "blah")
        
        exists = self._ctx.exists("/a/b/c")
        self.assertTrue(exists, "The value node SHOULD exist.")

        self._ctx.remove("/a/b/c")

        exists = self._ctx.exists("/a/b/c")
        self.assertTrue(not exists, "The value node SHOULD NOT exist.")

        return
    
    def test_context_remove_value_missing(self):

        error_raised = True

        try:
            self._ctx.remove("/a/b/c")

            exists = self._ctx.exists("/a/b/c")
            self.assert_(not exists, "The value node SHOULD NOT exist.")
        except:
            error_raised = True

        self.assertTrue(error_raised, "An exception SHOULD have been raised.")

        return
    
    def test_context_remove_value_missing_ignore_missing(self):

        self._ctx.insert("/a/b/c", "blah")
        
        exists = self._ctx.exists("/a/b/c")
        self.assertTrue(exists, "The value node SHOULD exist.")

        self._ctx.remove("/a/b/c", ignore_missing=True)

        exists = self._ctx.exists("/a/b/c")
        self.assertTrue(not exists, "The value node SHOULD NOT exist.")

        return
    

if __name__ == '__main__':
    unittest.main()
