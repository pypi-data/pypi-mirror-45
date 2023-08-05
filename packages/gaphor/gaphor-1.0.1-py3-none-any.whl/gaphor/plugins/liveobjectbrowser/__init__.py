"""
Plugin based on the Live Object browser
(http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/300304).
It shows the state of the data model at the time the browser is activated.
"""

from zope.interface import implementer

from gaphor.core import inject, action, build_action_group
from gaphor.interfaces import IService, IActionProvider
from gaphor.plugins.liveobjectbrowser.browser import Browser


@implementer(IService, IActionProvider)
class LiveObjectBrowser(object):

    element_factory = inject("element_factory")

    menu_xml = """
      <ui>
        <menubar action="mainwindow">
          <menu action="tools">
            <menuitem action="tools-life-object-browser" />
          </menu>
        </menubar>
      </ui>"""

    def __init__(self):
        self.action_group = build_action_group(self)

    def init(self, app):
        pass

    def shutdown(self):
        pass

    @action(name="tools-life-object-browser", label="Life object browser")
    def execute(self):
        browser = Browser("resource", self.element_factory.lselect())


# vim:sw=4:et
