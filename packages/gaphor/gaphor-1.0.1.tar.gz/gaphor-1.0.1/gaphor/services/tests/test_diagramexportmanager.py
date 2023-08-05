import unittest
from gaphor.application import Application
from gaphor.services.diagramexportmanager import DiagramExportManager


class DiagramExportManagerTestCase(unittest.TestCase):
    def setUp(self):
        Application.init(
            services=[
                "main_window",
                "properties",
                "element_factory",
                "diagram_export_manager",
                "action_manager",
            ]
        )

    def shutDown(self):
        Application.shutdown()

    def test_init(self):
        des = DiagramExportManager()
        des.init(None)

    def test_init_from_application(self):
        Application.get_service("diagram_export_manager")
        Application.get_service("main_window")
