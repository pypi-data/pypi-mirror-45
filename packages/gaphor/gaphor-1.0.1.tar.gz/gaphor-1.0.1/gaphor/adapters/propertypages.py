"""
Adapters for the Property Editor.

To register property pages implemented in this module, it is imported in
gaphor.adapter package.

# TODO: make all labels align top-left
# Add hidden columns for list stores where i can put the actual object
# being edited.

TODO:
 - stereotypes
 - association / association ends.
 - Follow HIG guidelines:
   * Leave a 12-pixel border between the edge of the window and
     the nearest controls.
   * Leave a 12-pixel horizontal gap between a control and its label. (The gap
     may be bigger for other controls in the same group, due to differences in
     the lengths of the labels.)
   * Labels must be concise and make sense when taken out of context.
     Otherwise, users relying on screenreaders or similar assistive
     technologies will not always be able to immediately understand the
     relationship between a control and those surrounding it.
   * Assign access keys to all editable controls. Ensure that using the access
     key focuses its associated control.
"""

import math
import logging
from zope import component

import gaphas.item
from gaphas.decorators import AsyncIO
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import Gtk
from zope.interface import implementer

from gaphor import UML
from gaphor.core import _, inject, transactional
from gaphor.diagram import items
from gaphor.services.elementdispatcher import EventWatcher
from gaphor.ui.interfaces import IPropertyPage

log = logging.getLogger(__name__)


class EditableTreeModel(Gtk.ListStore):
    """Editable GTK tree model based on ListStore model.

    Every row is represented by a list of editable values. Last column
    contains an object, which is being edited (this column is not
    displayed). When editable value in first column is set to empty string
    then object is deleted.

    Last row is empty and contains no object to edit. It allows to enter
    new values.

    When model is edited, then item is requested to be updated on canvas.

    Attributes:
    - _item: diagram item owning tree model
    """

    element_factory = inject("element_factory")

    def __init__(self, item, cols=None):
        """Create new model.

        Parameters:
        - _item: diagram item owning tree model
        - cols: model columns, defaults to [str, object]
        """

        if cols is None:
            cols = (str, object)
        super(EditableTreeModel, self).__init__(*cols)
        self._item = item

        for data in self._get_rows():
            self.append(data)
        self._add_empty()

    def refresh(self, obj):
        for row in self:
            if row[-1] is obj:
                self._set_object_value(row, len(row) - 1, obj)
                self.row_changed(row.path, row.iter)
                return

    def _get_rows(self):
        """Return rows to be edited.

        Last column has to contain object being edited.
        """

        raise NotImplemented

    def _create_object(self):
        """
        Create new object.
        """
        raise NotImplemented

    def _set_object_value(self, row, col, value):
        """
        Update row's column with a value.
        """
        raise NotImplemented

    def _swap_objects(self, o1, o2):
        """
        Swap two objects. If objects are swapped, then return ``True``.
        """
        raise NotImplemented

    def _get_object(self, iter):
        """
        Get object from ``iter``.
        """
        path = self.get_path(iter)
        return self[path][-1]

    def swap(self, a, b):
        """
        Swap two list rows.
        Parameters:
        - a: path to first row
        - b: path to second row
        """
        if not a or not b:
            return
        o1 = self[a][-1]
        o2 = self[b][-1]
        if o1 and o2 and self._swap_objects(o1, o2):
            # self._item.request_update(matrix=False)
            super(EditableTreeModel, self).swap(a, b)

    def _add_empty(self):
        """
        Add empty row to the end of the model.
        """
        self.append([None] * self.get_n_columns())

    @transactional
    def set_value(self, iter, col, value):
        row = self[iter][:]

        if col == 0 and not value and row[-1]:
            # kill row and delete object if text of first column is empty
            self.remove(iter)

        elif col == 0 and value and not row[-1]:
            # create new object
            obj = self._create_object()
            row[-1] = obj
            self._set_object_value(row, col, value)
            self._add_empty()

        elif row[-1]:
            self._set_object_value(row, col, value)

        self.set(iter, list(range(len(row))), row)

        self.set(iter, list(range(len(row))), row)

    def remove(self, iter):
        """
        Remove object from GTK model and destroy it.
        """
        obj = self._get_object(iter)
        if obj:
            obj.unlink()
            # self._item.request_update(matrix=False)
            return super(EditableTreeModel, self).remove(iter)
        else:
            return iter


class ClassAttributes(EditableTreeModel):
    """GTK tree model to edit class attributes."""

    def _get_rows(self):
        for attr in self._item.subject.ownedAttribute:
            if not attr.association:
                yield [UML.format(attr), attr.isStatic, attr]

    def _create_object(self):
        attr = self.element_factory.create(UML.Property)
        self._item.subject.ownedAttribute = attr
        return attr

    @transactional
    def _set_object_value(self, row, col, value):
        attr = row[-1]
        if col == 0:
            UML.parse(attr, value)
            row[0] = UML.format(attr)
        elif col == 1:
            attr.isStatic = not attr.isStatic
            row[1] = attr.isStatic
        elif col == 2:
            # Value in attribute object changed:
            row[0] = UML.format(attr)
            row[1] = attr.isStatic

    def _swap_objects(self, o1, o2):
        return self._item.subject.ownedAttribute.swap(o1, o2)


class ClassOperations(EditableTreeModel):
    """GTK tree model to edit class operations."""

    def _get_rows(self):
        for operation in self._item.subject.ownedOperation:
            yield [
                UML.format(operation),
                operation.isAbstract,
                operation.isStatic,
                operation,
            ]

    def _create_object(self):
        operation = self.element_factory.create(UML.Operation)
        self._item.subject.ownedOperation = operation
        return operation

    @transactional
    def _set_object_value(self, row, col, value):
        operation = row[-1]
        if col == 0:
            UML.parse(operation, value)
            row[0] = UML.format(operation)
        elif col == 1:
            operation.isAbstract = not operation.isAbstract
            row[1] = operation.isAbstract
        elif col == 2:
            operation.isStatic = not operation.isStatic
            row[2] = operation.isStatic
        elif col == 3:
            row[0] = UML.format(operation)
            row[1] = operation.isAbstract
            row[2] = operation.isStatic

    def _swap_objects(self, o1, o2):
        return self._item.subject.ownedOperation.swap(o1, o2)


class CommunicationMessageModel(EditableTreeModel):
    """GTK tree model for list of messages on communication diagram."""

    def __init__(self, item, cols=None, inverted=False):
        self.inverted = inverted
        super(CommunicationMessageModel, self).__init__(item, cols)

    def _get_rows(self):
        if self.inverted:
            for message in self._item._inverted_messages:
                yield [message.name, message]
        else:
            for message in self._item._messages:
                yield [message.name, message]

    def remove(self, iter):
        """Remove message from message item and destroy it."""

        message = self._get_object(iter)
        item = self._item
        super(CommunicationMessageModel, self).remove(iter)
        item.remove_message(message, self.inverted)

    def _create_object(self):
        item = self._item
        subject = item.subject
        message = UML.model.create_message(self.element_factory, subject, self.inverted)
        item.add_message(message, self.inverted)
        return message

    def _set_object_value(self, row, col, value):
        message = row[-1]
        message.name = value
        row[0] = value
        self._item.set_message_text(message, value, self.inverted)

    def _swap_objects(self, o1, o2):
        return self._item.swap_messages(o1, o2, self.inverted)


@transactional
def remove_on_keypress(tree, event):
    """Remove selected items from GTK model on ``backspace`` keypress."""

    k = Gdk.keyval_name(event.keyval).lower()
    if k == "backspace" or k == "kp_delete":
        model, iter = tree.get_selection().get_selected()
        if iter:
            model.remove(iter)


@transactional
def swap_on_keypress(tree, event):
    """Swap selected and previous (or next) items."""

    k = Gdk.keyval_name(event.keyval).lower()
    if k == "equal" or k == "kp_add":
        model, iter = tree.get_selection().get_selected()
        model.swap(iter, model.iter_next(iter))
        return True
    elif k == "minus":
        model, iter = tree.get_selection().get_selected()
        model.swap(iter, model.iter_previous(iter))
        return True


@transactional
def on_text_cell_edited(renderer, path, value, model, col=0):
    """Update editable tree model based on fresh user input."""

    iter = model.get_iter(path)
    model.set_value(iter, col, value)


@transactional
def on_bool_cell_edited(renderer, path, model, col):
    """Update editable tree model based on fresh user input."""

    iter = model.get_iter(path)
    model.set_value(iter, col, renderer.get_active())


class UMLComboModel(Gtk.ListStore):
    """UML combo box model.

    Model allows to easily create a combo box with values and their labels,
    for example

        label1  ->  value1
        label2  ->  value2
        label3  ->  value3

    Labels are displayed by combo box and programmer has easy access to
    values associated with given label.

    Attributes:

    - _data: model data
    - _indices: dictionary of values' indices
    """

    def __init__(self, data):
        super(UMLComboModel, self).__init__(str)

        self._indices = {}
        self._data = data

        # add labels to underlying model and store index information
        for i, (label, value) in enumerate(data):
            self.append([label])
            self._indices[value] = i

    def get_index(self, value):
        """
        Return index of a ``value``.
        """
        return self._indices[value]

    def get_value(self, index):
        """
        Get value for given ``index``.
        """
        return self._data[index][1]


def create_uml_combo(data, callback):
    """
    Create a combo box using ``UMLComboModel`` model.

    Combo box is returned.
    """
    model = UMLComboModel(data)
    combo = Gtk.ComboBox(model=model)
    cell = Gtk.CellRendererText()
    combo.pack_start(cell, True)
    combo.add_attribute(cell, "text", 0)
    combo.connect("changed", callback)
    return combo


def create_hbox_label(adapter, page, label):
    """
    Create a HBox with a label for given property page adapter and page
    itself.
    """
    hbox = Gtk.HBox(spacing=12)
    label = Gtk.Label(label=label)
    # label.set_alignment(0.0, 0.5)
    adapter.size_group.add_widget(label)
    hbox.pack_start(label, False, True, 0)
    page.pack_start(hbox, False, True, 0)
    return hbox


def create_tree_view(model, names, tip="", ro_cols=None):
    """
    Create a tree view for an editable tree model.

    :Parameters:
     model
        Model, for which tree view is created.
     names
        Names of columns.
     tip
        User interface tool tip for tree view.
     ro_cols
        Collection of indices pointing read only columns.
    """
    if ro_cols is None:
        ro_cols = set()

    tree_view = Gtk.TreeView(model=model)

    n = model.get_n_columns() - 1
    for name, i in zip(names, list(range(n))):
        col_type = model.get_column_type(i)
        if col_type == GObject.TYPE_STRING:
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", i not in ro_cols)
            renderer.set_property("is-expanded", True)
            renderer.connect("edited", on_text_cell_edited, model, i)
            col = Gtk.TreeViewColumn(name, renderer, text=i)
            col.set_expand(True)
            tree_view.append_column(col)
        elif col_type == GObject.TYPE_BOOLEAN:
            renderer = Gtk.CellRendererToggle()
            renderer.set_property("activatable", i not in ro_cols)
            renderer.connect("toggled", on_bool_cell_edited, model, i)
            col = Gtk.TreeViewColumn(name, renderer, active=i)
            col.set_expand(False)
            tree_view.append_column(col)

    tree_view.connect("key_press_event", remove_on_keypress)
    tree_view.connect("key_press_event", swap_on_keypress)

    tip = (
        tip
        + """
Press ENTER to edit item, BS/DEL to remove item.
Use -/= to move items up or down.\
    """
    )
    tree_view.set_tooltip_text(tip)

    return tree_view


@implementer(IPropertyPage)
@component.adapter(UML.Comment)
class CommentItemPropertyPage(object):
    """Property page for Comments."""

    order = 0

    def __init__(self, subject):
        self.subject = subject
        self.watcher = EventWatcher(subject)

    def construct(self):
        subject = self.subject
        page = Gtk.VBox()

        if not subject:
            return page

        label = Gtk.Label(label=_("Comment"))
        label.set_justify(Gtk.Justification.LEFT)
        page.pack_start(label, False, True, 0)

        buffer = Gtk.TextBuffer()
        if subject.body:
            buffer.set_text(subject.body)
        text_view = Gtk.TextView()
        text_view.set_buffer(buffer)
        text_view.show()
        text_view.set_size_request(-1, 100)
        page.pack_start(text_view, True, True, 0)
        page.default = text_view

        changed_id = buffer.connect("changed", self._on_body_change)

        def handler(event):
            if not text_view.props.has_focus:
                buffer.handler_block(changed_id)
                buffer.set_text(event.new_value)
                buffer.handler_unblock(changed_id)

        self.watcher.watch("body", handler).register_handlers()
        text_view.connect("destroy", self.watcher.unregister_handlers)

        return page

    @transactional
    def _on_body_change(self, buffer):
        self.subject.body = buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), False
        )


component.provideAdapter(CommentItemPropertyPage, name="Properties")


@implementer(IPropertyPage)
@component.adapter(UML.NamedElement)
class NamedElementPropertyPage(object):
    """An adapter which works for any named item view.

    It also sets up a table view which can be extended.
    """

    order = 10

    NAME_LABEL = _("Name")

    def __init__(self, subject):
        assert subject is None or isinstance(subject, UML.NamedElement), "%s" % type(
            subject
        )
        self.subject = subject
        self.watcher = EventWatcher(subject)
        self.size_group = Gtk.SizeGroup.new(Gtk.SizeGroupMode.HORIZONTAL)

    def construct(self):
        page = Gtk.VBox()

        subject = self.subject
        if not subject:
            return page

        hbox = create_hbox_label(self, page, self.NAME_LABEL)
        entry = Gtk.Entry()
        entry.set_text(subject and subject.name or "")
        hbox.pack_start(entry, True, True, 0)
        page.default = entry

        # monitor subject.name attribute
        changed_id = entry.connect("changed", self._on_name_change)

        def handler(event):
            if event.element is subject and event.new_value is not None:
                entry.handler_block(changed_id)
                entry.set_text(event.new_value)
                entry.handler_unblock(changed_id)

        self.watcher.watch("name", handler).register_handlers()
        entry.connect("destroy", self.watcher.unregister_handlers)

        return page

    @transactional
    def _on_name_change(self, entry):
        self.subject.name = entry.get_text()


component.provideAdapter(NamedElementPropertyPage, name="Properties")


class NamedItemPropertyPage(NamedElementPropertyPage):
    """
    Base class for named item based adapters.
    """

    def __init__(self, item):
        self.item = item
        super(NamedItemPropertyPage, self).__init__(item.subject)


@component.adapter(UML.Class)
class ClassPropertyPage(NamedElementPropertyPage):
    """Adapter which shows a property page for a class view."""

    def __init__(self, subject):
        super(ClassPropertyPage, self).__init__(subject)

    def construct(self):
        page = super(ClassPropertyPage, self).construct()

        if not self.subject:
            return page

        # Abstract toggle
        hbox = Gtk.HBox()
        label = Gtk.Label(label="")
        label.set_justify(Gtk.Justification.LEFT)
        self.size_group.add_widget(label)
        hbox.pack_start(label, False, True, 0)
        button = Gtk.CheckButton(label=_("Abstract"))
        button.set_active(self.subject.isAbstract)

        button.connect("toggled", self._on_abstract_change)
        hbox.pack_start(button, True, True, 0)
        page.pack_start(hbox, False, True, 0)

        return page

    @transactional
    def _on_abstract_change(self, button):
        self.subject.isAbstract = button.get_active()


component.provideAdapter(ClassPropertyPage, name="Properties")


@component.adapter(items.InterfaceItem)
class InterfacePropertyPage(NamedItemPropertyPage):
    """Adapter which shows a property page for an interface view."""

    def construct(self):
        page = super(InterfacePropertyPage, self).construct()
        item = self.item

        # Fold toggle
        hbox = Gtk.HBox()
        label = Gtk.Label(label="")
        label.set_justify(Gtk.Justification.LEFT)
        self.size_group.add_widget(label)
        hbox.pack_start(label, False, True, 0)

        button = Gtk.CheckButton(_("Folded"))
        button.set_active(item.folded)
        button.connect("toggled", self._on_fold_change)

        connected_items = [c.item for c in item.canvas.get_connections(connected=item)]
        allowed = (items.DependencyItem, items.ImplementationItem)
        can_fold = (
            len(connected_items) == 0
            or len(connected_items) == 1
            and isinstance(connected_items[0], allowed)
        )

        button.set_sensitive(can_fold)
        hbox.pack_start(button, True, True, 0)
        page.pack_start(hbox, False, True, 0)

        return page

    @transactional
    def _on_fold_change(self, button):
        item = self.item

        connected_items = [c.item for c in item.canvas.get_connections(connected=item)]
        assert len(connected_items) <= 1

        line = None
        if len(connected_items) == 1:
            line = connected_items[0]

        fold = button.get_active()

        if fold:
            item.folded = item.FOLDED_PROVIDED
        else:
            item.folded = item.FOLDED_NONE

        if line:
            if fold and isinstance(line, items.DependencyItem):
                item.folded = item.FOLDED_REQUIRED

            line._solid = fold
            constraint = line.canvas.get_connection(line.head).constraint
            constraint.ratio_x = 0.5
            constraint.ratio_y = 0.5
            line.request_update()


component.provideAdapter(InterfacePropertyPage, name="Properties")


@implementer(IPropertyPage)
@component.adapter(items.ClassItem)
class AttributesPage(object):
    """An editor for attributes associated with classes and interfaces."""

    order = 20

    def __init__(self, item):
        super(AttributesPage, self).__init__()
        self.item = item
        self.watcher = EventWatcher(item.subject)

    def construct(self):
        page = Gtk.VBox()

        if not self.item.subject:
            return page

        # Show attributes toggle
        hbox = Gtk.HBox()
        label = Gtk.Label(label="")
        label.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(label, False, True, 0)
        button = Gtk.CheckButton(label=_("Show attributes"))
        button.set_active(self.item.show_attributes)
        button.connect("toggled", self._on_show_attributes_change)
        hbox.pack_start(button, True, True, 0)
        page.pack_start(hbox, False, True, 0)

        def create_model():
            return ClassAttributes(self.item, (str, bool, object))

        self.model = create_model()

        tip = """\
Add and edit class attributes according to UML syntax. Attribute syntax examples
- attr
- + attr: int
- # /attr: int
"""
        tree_view = create_tree_view(self.model, (_("Attributes"), _("S")), tip)
        page.pack_start(tree_view, True, True, 0)

        @AsyncIO(single=True)
        def handler(event):
            # Single it's asynchronous, make sure all properties are still there
            if not tree_view.props.has_focus and self.item and self.item.subject:
                self.model = create_model()
                tree_view.set_model(self.model)

        self.watcher.watch("ownedAttribute.name", handler).watch(
            "ownedAttribute.isDerived", handler
        ).watch("ownedAttribute.visibility", handler).watch(
            "ownedAttribute.isStatic", handler
        ).watch(
            "ownedAttribute.lowerValue", handler
        ).watch(
            "ownedAttribute.upperValue", handler
        ).watch(
            "ownedAttribute.defaultValue", handler
        ).watch(
            "ownedAttribute.typeValue", handler
        ).register_handlers()
        tree_view.connect("destroy", self.watcher.unregister_handlers)
        return page

    @transactional
    def _on_show_attributes_change(self, button):
        self.item.show_attributes = button.get_active()
        self.item.request_update()


component.provideAdapter(AttributesPage, name="Attributes")


@implementer(IPropertyPage)
@component.adapter(items.ClassItem)
class OperationsPage(object):
    """An editor for operations associated with classes and interfaces."""

    order = 30

    def __init__(self, item):
        super(OperationsPage, self).__init__()
        self.item = item
        self.watcher = EventWatcher(item.subject)

    def construct(self):
        page = Gtk.VBox()

        if not self.item.subject:
            return page

        # Show operations toggle
        hbox = Gtk.HBox()
        label = Gtk.Label(label="")
        label.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(label, False, True, 0)
        button = Gtk.CheckButton(label=_("Show operations"))
        button.set_active(self.item.show_operations)
        button.connect("toggled", self._on_show_operations_change)
        hbox.pack_start(button, True, True, 0)
        page.pack_start(hbox, False, True, 0)

        def create_model():
            return ClassOperations(self.item, (str, bool, bool, object))

        self.model = create_model()
        tip = """\
Add and edit class operations according to UML syntax. Operation syntax examples
- call()
- + call(a: int, b: str)
- # call(a: int: b: str): bool
"""
        tree_view = create_tree_view(self.model, (_("Operation"), _("A"), _("S")), tip)
        page.pack_start(tree_view, True, True, 0)

        @AsyncIO(single=True)
        def handler(event):
            if not tree_view.props.has_focus and self.item and self.item.subject:
                self.model = create_model()
                tree_view.set_model(self.model)

        self.watcher.watch("ownedOperation.name", handler).watch(
            "ownedOperation.isAbstract", handler
        ).watch("ownedOperation.visibility", handler).watch(
            "ownedOperation.returnResult.lowerValue", handler
        ).watch(
            "ownedOperation.returnResult.upperValue", handler
        ).watch(
            "ownedOperation.returnResult.typeValue", handler
        ).watch(
            "ownedOperation.formalParameter.lowerValue", handler
        ).watch(
            "ownedOperation.formalParameter.upperValue", handler
        ).watch(
            "ownedOperation.formalParameter.typeValue", handler
        ).watch(
            "ownedOperation.formalParameter.defaultValue", handler
        ).register_handlers()
        tree_view.connect("destroy", self.watcher.unregister_handlers)

        return page

    @transactional
    def _on_show_operations_change(self, button):
        self.item.show_operations = button.get_active()
        self.item.request_update()


component.provideAdapter(OperationsPage, name="Operations")


@implementer(IPropertyPage)
@component.adapter(items.DependencyItem)
class DependencyPropertyPage(object):
    """Dependency item editor."""

    order = 0

    element_factory = inject("element_factory")

    DEPENDENCY_TYPES = (
        (_("Dependency"), UML.Dependency),
        (_("Usage"), UML.Usage),
        (_("Realization"), UML.Realization),
        (_("Implementation"), UML.Implementation),
    )

    def __init__(self, item):
        super(DependencyPropertyPage, self).__init__()
        self.item = item
        self.size_group = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)
        self.watcher = EventWatcher(self.item)

    def construct(self):
        page = Gtk.VBox()

        hbox = create_hbox_label(self, page, _("Dependency type"))

        self.combo = create_uml_combo(
            self.DEPENDENCY_TYPES, self._on_dependency_type_change
        )
        hbox.pack_start(self.combo, False, True, 0)

        hbox = create_hbox_label(self, page, "")

        button = Gtk.CheckButton(_("Automatic"))
        button.set_active(self.item.auto_dependency)
        button.connect("toggled", self._on_auto_dependency_change)
        hbox.pack_start(button, True, True, 0)

        self.watcher.watch("subject", self._on_subject_change).register_handlers()
        button.connect("destroy", self.watcher.unregister_handlers)

        self.update()

        return page

    def _on_subject_change(self, event):
        self.update()

    def update(self):
        """
        Update dependency type combo box.

        Disallow dependency type when dependency is established.
        """
        combo = self.combo
        item = self.item
        index = combo.get_model().get_index(item.dependency_type)
        combo.props.sensitive = not item.auto_dependency
        combo.set_active(index)

    @transactional
    def _on_dependency_type_change(self, combo):
        combo = self.combo
        cls = combo.get_model().get_value(combo.get_active())
        self.item.dependency_type = cls
        if self.item.subject:
            self.element_factory.swap_element(self.item.subject, cls)
            self.item.request_update()

    @transactional
    def _on_auto_dependency_change(self, button):
        self.item.auto_dependency = button.get_active()
        self.update()


component.provideAdapter(DependencyPropertyPage, name="Properties")


@component.adapter(items.AssociationItem)
class AssociationPropertyPage(NamedItemPropertyPage):
    """
    """

    def construct_end(self, title, end):

        if not end.subject:
            return None

        # TODO: use Gtk.Frame here
        frame = Gtk.Frame.new("%s (: %s)" % (title, end.subject.type.name))
        vbox = Gtk.VBox()
        vbox.set_border_width(6)
        vbox.set_spacing(6)
        frame.add(vbox)

        self.create_pages(end, vbox)

        return frame

    def construct(self):
        page = super(AssociationPropertyPage, self).construct()

        if not self.subject:
            return page

        hbox = Gtk.HBox()
        label = Gtk.Label(label="")
        label.set_justify(Gtk.Justification.LEFT)
        self.size_group.add_widget(label)
        hbox.pack_start(label, False, True, 0)

        button = Gtk.CheckButton(label=_("Show direction"))
        button.set_active(self.item.show_direction)
        button.connect("toggled", self._on_show_direction_change)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button(label=_("Invert Direction"))
        button.connect("clicked", self._on_invert_direction_change)
        hbox.pack_start(button, True, True, 0)

        page.pack_start(hbox, False, True, 0)

        box = self.construct_end(_("Head"), self.item.head_end)
        if box:
            page.pack_start(box, False, True, 0)

        box = self.construct_end(_("Tail"), self.item.tail_end)
        if box:
            page.pack_start(box, False, True, 0)

        self.update()

        return page

    def update(self):
        pass

    @transactional
    def _on_show_direction_change(self, button):
        self.item.show_direction = button.get_active()

    @transactional
    def _on_invert_direction_change(self, button):
        self.item.invert_direction()

    def get_adapters(self, item):
        """
        Return an ordered list of (order, name, adapter).
        """
        adaptermap = {}
        try:
            if item.subject:
                for name, adapter in component.getAdapters(
                    [item.subject], IPropertyPage
                ):
                    adaptermap[name] = (adapter.order, name, adapter)
        except AttributeError:
            pass
        for name, adapter in component.getAdapters([item], IPropertyPage):
            adaptermap[name] = (adapter.order, name, adapter)

        adapters = sorted(adaptermap.values())
        return adapters

    def create_pages(self, item, vbox):
        """
        Load all tabs that can operate on the given item.

        The first item will not contain a title.
        """
        adapters = self.get_adapters(item)

        first = True
        for _, name, adapter in adapters:
            try:
                page = adapter.construct()
                if page is None:
                    continue
                if first:
                    vbox.pack_start(page, False, True, 0)
                    first = False
                else:
                    expander = Gtk.Expander()
                    expander.set_use_markup(True)
                    expander.set_label("<b>%s</b>" % name)
                    expander.add(page)
                    expander.show_all()
                    vbox.pack_start(expander, False, True, 0)
            except Exception as e:
                log.error(
                    "Could not construct property page for " + name, exc_info=True
                )


component.provideAdapter(AssociationPropertyPage, name="Properties")


@implementer(IPropertyPage)
@component.adapter(UML.Property)
class AssociationEndPropertyPage(object):
    """Property page for association end properties."""

    order = 0

    NAVIGABILITY = [None, False, True]

    def __init__(self, subject):
        self.subject = subject
        self.watcher = EventWatcher(subject)

    def construct(self):
        vbox = Gtk.VBox()

        entry = Gtk.Entry()
        # entry.set_text(UML.format(self.subject, visibility=True, is_derived=Truemultiplicity=True) or '')

        # monitor subject attribute (all, cause it contains many children)
        changed_id = entry.connect("changed", self._on_end_name_change)

        def handler(event):
            if not entry.props.has_focus:
                entry.handler_block(changed_id)
                entry.set_text(
                    UML.format(
                        self.subject,
                        visibility=True,
                        is_derived=True,
                        multiplicity=True,
                    )
                    or ""
                )
                # entry.set_text(UML.format(self.subject, multiplicity=True) or '')
                entry.handler_unblock(changed_id)

        handler(None)

        self.watcher.watch("name", handler).watch("aggregation", handler).watch(
            "visibility", handler
        ).watch("lowerValue", handler).watch("upperValue", handler).register_handlers()
        entry.connect("destroy", self.watcher.unregister_handlers)

        vbox.pack_start(entry, True, True, 0)

        entry.set_tooltip_text(
            """\
Enter attribute name and multiplicity, for example
- name
+ name [1]
- name [1..2]
~ 1..2
- [1..2]\
"""
        )

        combo = Gtk.ComboBoxText()
        for t in ("Unknown navigation", "Not navigable", "Navigable"):
            combo.append_text(t)

        nav = self.subject.navigability
        combo.set_active(self.NAVIGABILITY.index(nav))

        combo.connect("changed", self._on_navigability_change)
        vbox.pack_start(combo, False, True, 0)

        combo = Gtk.ComboBoxText()
        for t in ("No aggregation", "Shared", "Composite"):
            combo.append_text(t)

        combo.set_active(
            ["none", "shared", "composite"].index(self.subject.aggregation)
        )

        combo.connect("changed", self._on_aggregation_change)
        vbox.pack_start(combo, False, True, 0)

        return vbox

    @transactional
    def _on_end_name_change(self, entry):
        UML.parse(self.subject, entry.get_text())

    @transactional
    def _on_navigability_change(self, combo):
        nav = self.NAVIGABILITY[combo.get_active()]
        UML.model.set_navigability(self.subject.association, self.subject, nav)

    @transactional
    def _on_aggregation_change(self, combo):
        self.subject.aggregation = ("none", "shared", "composite")[combo.get_active()]


component.provideAdapter(AssociationEndPropertyPage, name="Properties")


@implementer(IPropertyPage)
@component.adapter(gaphas.item.Line)
class LineStylePage(object):
    """Basic line style properties: color, orthogonal, etc."""

    order = 400

    def __init__(self, item):
        super(LineStylePage, self).__init__()
        self.item = item
        self.size_group = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.HORIZONTAL)

    def construct(self):
        page = Gtk.VBox()

        hbox = Gtk.HBox()
        label = Gtk.Label(label="")
        label.set_justify(Gtk.Justification.LEFT)
        self.size_group.add_widget(label)
        hbox.pack_start(label, False, True, 0)

        button = Gtk.CheckButton(label=_("Orthogonal"))
        button.set_active(self.item.orthogonal)
        button.connect("toggled", self._on_orthogonal_change)
        hbox.pack_start(button, True, True, 0)

        page.pack_start(hbox, False, True, 0)

        if len(self.item.handles()) < 3:
            # Only one segment
            button.props.sensitive = False

        hbox = Gtk.HBox()
        label = Gtk.Label(label="")
        label.set_justify(Gtk.Justification.LEFT)
        self.size_group.add_widget(label)
        hbox.pack_start(label, False, True, 0)

        button = Gtk.CheckButton(label=_("Horizontal"))
        button.set_active(self.item.horizontal)
        button.connect("toggled", self._on_horizontal_change)
        hbox.pack_start(button, True, True, 0)

        page.pack_start(hbox, False, True, 0)

        return page

    @transactional
    def _on_orthogonal_change(self, button):
        self.item.orthogonal = button.get_active()

    @transactional
    def _on_horizontal_change(self, button):
        self.item.horizontal = button.get_active()


component.provideAdapter(LineStylePage, name="Style")


@component.adapter(items.ObjectNodeItem)
class ObjectNodePropertyPage(NamedItemPropertyPage):
    """
    """

    ORDERING_VALUES = ["unordered", "ordered", "LIFO", "FIFO"]

    def construct(self):
        page = super(ObjectNodePropertyPage, self).construct()

        subject = self.subject

        if not subject:
            return page

        hbox = create_hbox_label(self, page, _("Upper bound"))
        entry = Gtk.Entry()
        entry.set_text(subject.upperBound or "")
        entry.connect("changed", self._on_upper_bound_change)
        hbox.pack_start(entry, True, True, 0)

        hbox = create_hbox_label(self, page, "")
        combo = Gtk.ComboBoxText()
        for v in self.ORDERING_VALUES:
            combo.append_text(v)
        combo.set_active(self.ORDERING_VALUES.index(subject.ordering))
        combo.connect("changed", self._on_ordering_change)
        hbox.pack_start(combo, False, True, 0)

        hbox = create_hbox_label(self, page, "")
        button = Gtk.CheckButton(_("Ordering"))
        button.set_active(self.item.show_ordering)
        button.connect("toggled", self._on_ordering_show_change)
        hbox.pack_start(button, False, True, 0)

        return page

    def update(self):
        pass

    @transactional
    def _on_upper_bound_change(self, entry):
        value = entry.get_text().strip()
        self.item.set_upper_bound(value)

    @transactional
    def _on_ordering_change(self, combo):
        value = self.ORDERING_VALUES[combo.get_active()]
        self.subject.ordering = value

    @transactional
    def _on_ordering_show_change(self, button):
        self.item.show_ordering = button.get_active()
        self.item.set_ordering(self.subject.ordering)


component.provideAdapter(ObjectNodePropertyPage, name="Properties")


@component.adapter(items.ForkNodeItem)
class JoinNodePropertyPage(NamedItemPropertyPage):
    """
    """

    def construct(self):
        page = super(JoinNodePropertyPage, self).construct()

        subject = self.subject

        if not subject:
            return page

        hbox = Gtk.HBox()
        page.pack_start(hbox, False, True, 0)

        if isinstance(subject, UML.JoinNode):
            hbox = create_hbox_label(self, page, _("Join specification"))
            entry = Gtk.Entry()
            entry.set_text(subject.joinSpec or "")
            entry.connect("changed", self._on_join_spec_change)
            hbox.pack_start(entry, True, True, 0)

        button = Gtk.CheckButton(_("Horizontal"))
        button.set_active(self.item.matrix[2] != 0)
        button.connect("toggled", self._on_horizontal_change)
        page.pack_start(button, False, True, 0)

        return page

    def update(self):
        pass

    @transactional
    def _on_join_spec_change(self, entry):
        value = entry.get_text().strip()
        self.subject.joinSpec = value

    def _on_horizontal_change(self, button):
        if button.get_active():
            self.item.matrix.rotate(math.pi / 2)
        else:
            self.item.matrix.rotate(-math.pi / 2)
        self.item.request_update()


component.provideAdapter(JoinNodePropertyPage, name="Properties")


class FlowPropertyPageAbstract(NamedElementPropertyPage):
    """Flow item element editor."""

    def construct(self):
        page = super(FlowPropertyPageAbstract, self).construct()

        subject = self.subject

        if not subject:
            return page

        hbox = create_hbox_label(self, page, _("Guard"))
        entry = Gtk.Entry()
        entry.set_text(subject.guard or "")
        changed_id = entry.connect("changed", self._on_guard_change)
        hbox.pack_start(entry, True, True, 0)

        def handler(event):
            entry.handler_block(changed_id)
            v = event.new_value
            entry.set_text(v if v else "")
            entry.handler_unblock(changed_id)

        self.watcher.watch("guard", handler).register_handlers()
        entry.connect("destroy", self.watcher.unregister_handlers)

        return page

    @transactional
    def _on_guard_change(self, entry):
        value = entry.get_text().strip()
        self.subject.guard = value


# TODO: unify ObjectFlowPropertyPage and ControlFlowPropertyPage
#   after introducing common class for element editors
@component.adapter(UML.ControlFlow)
class ControlFlowPropertyPage(FlowPropertyPageAbstract):
    pass


@component.adapter(UML.ObjectFlow)
class ObjectFlowPropertyPage(FlowPropertyPageAbstract):
    pass


component.provideAdapter(ControlFlowPropertyPage, name="Properties")
component.provideAdapter(ObjectFlowPropertyPage, name="Properties")


@component.adapter(items.ComponentItem)
class ComponentPropertyPage(NamedItemPropertyPage):
    """
    """

    def construct(self):
        page = super(ComponentPropertyPage, self).construct()

        subject = self.subject

        if not subject:
            return page

        hbox = Gtk.HBox()
        page.pack_start(hbox, False, True, 0)

        button = Gtk.CheckButton(_("Indirectly instantiated"))
        button.set_active(subject.isIndirectlyInstantiated)
        button.connect("toggled", self._on_ii_change)
        hbox.pack_start(button, False, True, 0)

        return page

    def update(self):
        pass

    @transactional
    def _on_ii_change(self, button):
        """
        Called when user clicks "Indirectly instantiated" check button.
        """
        subject = self.subject
        if subject:
            subject.isIndirectlyInstantiated = button.get_active()


component.provideAdapter(ComponentPropertyPage, name="Properties")


@component.adapter(items.MessageItem)
class MessagePropertyPage(NamedItemPropertyPage):
    """Property page for editing message items.

    When message is on communication diagram, then additional messages can
    be added. On sequence diagram sort of message can be changed.
    """

    element_factory = inject("element_factory")

    NAME_LABEL = _("Message")

    MESSAGE_SORT = (
        ("Call", "synchCall"),
        ("Asynchronous", "asynchCall"),
        ("Signal", "asynchSignal"),
        ("Create", "createMessage"),
        ("Delete", "deleteMessage"),
        ("Reply", "reply"),
    )

    def construct(self):
        page = super(MessagePropertyPage, self).construct()

        item = self.item
        subject = item.subject

        if not subject:
            return page

        if item.is_communication():
            self._messages = CommunicationMessageModel(item)
            tree_view = create_tree_view(self._messages, (_("Message"),))
            tree_view.set_headers_visible(False)
            frame = Gtk.Frame.new(label=_("Additional Messages"))
            frame.add(tree_view)
            page.pack_start(frame, True, True, 0)

            self._inverted_messages = CommunicationMessageModel(item, inverted=True)
            tree_view = create_tree_view(self._inverted_messages, (_("Message"),))
            tree_view.set_headers_visible(False)
            frame = Gtk.Frame.new(label=_("Inverted Messages"))
            frame.add(tree_view)
            page.pack_end(frame, True, True, 0)
        else:
            hbox = create_hbox_label(self, page, _("Message sort"))

            sort_data = self.MESSAGE_SORT
            lifeline = None
            cinfo = item.canvas.get_connection(item.tail)
            if cinfo:
                lifeline = cinfo.connected

            # disallow connecting two delete messages to a lifeline
            if (
                lifeline
                and lifeline.is_destroyed
                and subject.messageSort != "deleteMessage"
            ):
                sort_data = list(sort_data)
                assert sort_data[4][1] == "deleteMessage"
                del sort_data[4]

            combo = self.combo = create_uml_combo(
                sort_data, self._on_message_sort_change
            )
            hbox.pack_start(combo, False, True, 0)

            index = combo.get_model().get_index(subject.messageSort)
            combo.set_active(index)

        return page

    @transactional
    def _on_message_sort_change(self, combo):
        """Update message item's message sort information."""

        combo = self.combo
        ms = combo.get_model().get_value(combo.get_active())

        item = self.item
        subject = item.subject
        lifeline = None
        cinfo = item.canvas.get_connection(item.tail)
        if cinfo:
            lifeline = cinfo.connected

        #
        # allow only one delete message to connect to lifeline's lifetime
        # destroyed status can be changed only by delete message itself
        #
        if lifeline:
            if subject.messageSort == "deleteMessage" or not lifeline.is_destroyed:
                is_destroyed = ms == "deleteMessage"
                lifeline.is_destroyed = is_destroyed
                # TODO: is required here?
                lifeline.request_update()

        subject.messageSort = ms
        # TODO: is required here?
        item.request_update()


component.provideAdapter(MessagePropertyPage, name="Properties")
