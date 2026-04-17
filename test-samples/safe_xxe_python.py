from defusedxml import ElementTree as SafeET


# Safe: Use defusedxml for untrusted XML
def safe_parse(xml_data):
    return SafeET.fromstring(xml_data)


# Safe: lxml with secure parser settings
def safe_lxml_parse(xml_data):
    from lxml import etree
    parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    return etree.fromstring(xml_data, parser=parser)
