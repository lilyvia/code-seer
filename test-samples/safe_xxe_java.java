import com.fasterxml.jackson.dataformat.xml.XmlMapper;

// Safe: Use Jackson XML mapper instead of DocumentBuilderFactory
public class SafeXxeJava {
    public Object safeParse(String xml) throws Exception {
        XmlMapper mapper = new XmlMapper();
        return mapper.readValue(xml, Object.class);
    }
}
