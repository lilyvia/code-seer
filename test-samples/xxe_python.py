import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import xml.etree.ElementTree
from lxml import etree


def test_et_parse(xml_input):
    ET.parse(xml_input)


def test_et_fromstring(xml_input):
    ET.fromstring(xml_input)


def test_xml_etree_ElementTree_parse(xml_input):
    xml.etree.ElementTree.parse(xml_input)


def test_xml_etree_ElementTree_fromstring(xml_input):
    xml.etree.ElementTree.fromstring(xml_input)


def test_minidom_parse(xml_input):
    minidom.parse(xml_input)


def test_minidom_parseString(xml_input):
    minidom.parseString(xml_input)


def test_etree_fromstring(xml_input):
    etree.fromstring(xml_input)


def test_etree_parse(xml_input):
    etree.parse(xml_input)


def test_etree_XMLParser_resolve_entities():
    parser = etree.XMLParser(resolve_entities=True)


def test_etree_XMLParser_load_dtd():
    parser = etree.XMLParser(load_dtd=True)


def test_etree_XMLParser_no_network():
    parser = etree.XMLParser(no_network=False)

def false_negative_expansion_xxe_python(user_xml, xmltodict):
    xml.sax.make_parser().parse(user_xml)
    xmltodict.parse(user_xml)
    etree.XMLParser(resolve_entities=True)
    ET.iterparse(user_xml)
