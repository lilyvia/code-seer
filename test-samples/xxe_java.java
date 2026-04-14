import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.XMLReaderFactory;
import javax.xml.transform.TransformerFactory;

public class XXEJavaSample {

    public void testDocumentBuilderFactory() throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    }

    public void testSAXParserFactory() throws Exception {
        SAXParserFactory factory = SAXParserFactory.newInstance();
    }

    public void testXMLReaderFactory() throws Exception {
        XMLReader reader = XMLReaderFactory.createXMLReader();
    }

    public void testTransformerFactory() throws Exception {
        TransformerFactory factory = TransformerFactory.newInstance();
    }

    public void testSetFeatureDisallowDoctype(DocumentBuilderFactory factory) throws Exception {
        factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", false);
    }

    public void testSetFeatureExternalGeneralEntities(DocumentBuilderFactory factory) throws Exception {
        factory.setFeature("http://xml.org/sax/features/external-general-entities", true);
    }

    public void testSetFeatureExternalParameterEntities(DocumentBuilderFactory factory) throws Exception {
        factory.setFeature("http://xml.org/sax/features/external-parameter-entities", true);
    }

    public void testSetFeatureLoadExternalDtd(DocumentBuilderFactory factory) throws Exception {
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", true);
    }
}
