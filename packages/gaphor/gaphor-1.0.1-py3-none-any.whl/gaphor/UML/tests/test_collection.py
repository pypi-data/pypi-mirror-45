"""
Test if the collection's list supports all trickery.
"""

import unittest
from gaphor.UML.collection import collectionlist


class CollectionlistTestCase(unittest.TestCase):
    def test_listing(self):
        c = collectionlist()
        c.append("a")
        c.append("b")
        c.append("c")
        assert str(c) == "['a', 'b', 'c']"
