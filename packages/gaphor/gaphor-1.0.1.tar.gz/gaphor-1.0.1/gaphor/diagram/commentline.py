"""
CommentLine -- A line that connects a comment to another model element.

"""

from zope import component

from gaphor.diagram.diagramline import DiagramLine
from gaphor.diagram.interfaces import IConnect


class CommentLineItem(DiagramLine):
    def __init__(self, id=None):
        DiagramLine.__init__(self, id)

    def save(self, save_func):
        DiagramLine.save(self, save_func)

    def load(self, name, value):
        DiagramLine.load(self, name, value)

    def postload(self):
        DiagramLine.postload(self)

    def unlink(self):
        canvas = self.canvas
        c1 = canvas.get_connection(self.head)
        c2 = canvas.get_connection(self.tail)
        if c1 and c2:
            query = (c1.connected, self)
            adapter = component.queryMultiAdapter(query, IConnect)
            adapter.disconnect(self.head)
        super(CommentLineItem, self).unlink()

    def draw(self, context):
        context.cairo.set_dash((7.0, 5.0), 0)
        DiagramLine.draw(self, context)


# vim: sw=4:et:ai
