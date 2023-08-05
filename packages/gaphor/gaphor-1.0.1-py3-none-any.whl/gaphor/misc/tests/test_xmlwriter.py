import sys
import unittest
from gaphor.misc.xmlwriter import XMLWriter


class Writer(object):
    def __init__(self):
        self.s = ""

    def write(self, text):
        self.s += text


class XMLWriterTestCase(unittest.TestCase):
    def test_elements_1(self):
        w = Writer()
        xml_w = XMLWriter(w)
        xml_w.startDocument()
        xml_w.startElement("foo", {})
        xml_w.endElement("foo")

        xml = (
            """<?xml version="1.0" encoding="%s"?>\n<foo/>""" % sys.getdefaultencoding()
        )
        assert w.s == xml, w.s + " != " + xml

    def test_elements_2(self):
        w = Writer()
        xml_w = XMLWriter(w)
        xml_w.startDocument()
        xml_w.startElement("foo", {})
        xml_w.startElement("bar", {})
        xml_w.endElement("bar")
        xml_w.endElement("foo")

        xml = (
            """<?xml version="1.0" encoding="%s"?>\n<foo>\n<bar/>\n</foo>"""
            % sys.getdefaultencoding()
        )
        assert w.s == xml, w.s

    def test_elements_test(self):
        w = Writer()
        xml_w = XMLWriter(w)
        xml_w.startDocument()
        xml_w.startElement("foo", {})
        xml_w.startElement("bar", {})
        xml_w.characters("hello")
        xml_w.endElement("bar")
        xml_w.endElement("foo")

        xml = (
            """<?xml version="1.0" encoding="%s"?>\n<foo>\n<bar>hello</bar>\n</foo>"""
            % sys.getdefaultencoding()
        )
        assert w.s == xml, w.s

    def test_elements_ns_default(self):
        w = Writer()
        xml_w = XMLWriter(w)
        xml_w.startDocument()
        xml_w.startPrefixMapping(None, "http://gaphor.devjavu.com/schema")
        xml_w.startElementNS(("http://gaphor.devjavu.com/schema", "foo"), "qn", {})
        xml_w.endElementNS(("http://gaphor.devjavu.com/schema", "foo"), "qn")

        xml = (
            """<?xml version="1.0" encoding="%s"?>\n<foo xmlns="http://gaphor.devjavu.com/schema"/>"""
            % sys.getdefaultencoding()
        )
        assert w.s == xml, w.s

    def test_elements_ns_1(self):
        w = Writer()
        xml_w = XMLWriter(w)
        xml_w.startDocument()
        xml_w.startPrefixMapping("g", "http://gaphor.devjavu.com/schema")
        xml_w.startElementNS(("http://gaphor.devjavu.com/schema", "foo"), "qn", {})
        xml_w.endElementNS(("http://gaphor.devjavu.com/schema", "foo"), "qn")

        xml = (
            """<?xml version="1.0" encoding="%s"?>\n<g:foo xmlns:g="http://gaphor.devjavu.com/schema"/>"""
            % sys.getdefaultencoding()
        )
        assert w.s == xml, w.s
