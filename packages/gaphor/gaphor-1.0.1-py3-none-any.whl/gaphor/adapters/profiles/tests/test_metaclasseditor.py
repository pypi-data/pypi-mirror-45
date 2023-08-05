from gaphor.tests import TestCase
from gaphor.adapters.profiles.metaclasseditor import MetaclassNameEditor
from gaphor.diagram import items
from gaphor import UML
from gi.repository import Gtk


class MetaclassEditorTest(TestCase):
    def test_name_selection(self):
        ci = self.create(items.MetaclassItem, UML.Class)
        ci.subject.name = "Class"
        editor = MetaclassNameEditor(ci)
        page = editor.construct()
        self.assertTrue(page)
        combo = page.get_children()[0].get_children()[1]
        self.assertSame(Gtk.ComboBox, type(combo))

        self.assertEqual("Class", combo.get_child().get_text())

        ci.subject.name = "Blah"
        self.assertEqual("Blah", combo.get_child().get_text())
