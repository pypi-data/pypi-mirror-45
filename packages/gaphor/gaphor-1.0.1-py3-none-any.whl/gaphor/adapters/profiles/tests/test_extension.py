"""
Extension item connection adapter tests.
"""

from gaphor.tests import TestCase
from gaphor import UML
from gaphor.diagram import items


class ExtensionConnectorTestCase(TestCase):
    """
    Extension item connection adapter tests.
    """

    def test_class_glue(self):
        """Test extension item gluing to a class."""

        ext = self.create(items.ExtensionItem)
        cls = self.create(items.ClassItem, UML.Class)

        # cannot connect extension item tail to a class
        glued = self.allow(ext, ext.tail, cls)
        self.assertFalse(glued)

    def test_stereotype_glue(self):
        """Test extension item gluing to a stereotype."""

        ext = self.create(items.ExtensionItem)
        st = self.create(items.ClassItem, UML.Stereotype)

        # test precondition
        assert isinstance(st.subject, UML.Stereotype)

        # can connect extension item head to a Stereotype UML metaclass,
        # because it derives from Class UML metaclass
        glued = self.allow(ext, ext.head, st)
        self.assertTrue(glued)

    def test_glue(self):
        """Test extension item glue
        """
        ext = self.create(items.ExtensionItem)
        st = self.create(items.ClassItem, UML.Stereotype)
        cls = self.create(items.ClassItem, UML.Class)

        glued = self.allow(ext, ext.tail, st)
        self.assertTrue(glued)

        self.connect(ext, ext.tail, st)

        glued = self.allow(ext, ext.head, cls)
        self.assertTrue(glued)

    def test_connection(self):
        """Test extension item connection
        """
        ext = self.create(items.ExtensionItem)
        st = self.create(items.ClassItem, UML.Stereotype)
        cls = self.create(items.ClassItem, UML.Class)

        self.connect(ext, ext.tail, st)
        self.connect(ext, ext.head, cls)
