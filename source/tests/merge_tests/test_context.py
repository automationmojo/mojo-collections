
import unittest

from mojo.collections.wellknown import ContextSingleton

class TestContext(unittest.TestCase):

    def test_context_insert_lookup(self):

        ctx = ContextSingleton()

        ctx.insert("/a/b/c", "blah")

        val = ctx.lookup("/a/b/c")

        self.assert_(val == "blah", f"The returned context value '{val}' did not match 'blah'.")

        return
    
    def test_context_default_value_lookup(self):

        ctx = ContextSingleton()

        val = ctx.lookup("/d/e/f", default="blah")

        self.assert_(val == "blah", f"The returned context value '{val}' did not match 'blah'.")

        return


if __name__ == '__main__':
    unittest.main()
