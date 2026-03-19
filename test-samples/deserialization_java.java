import java.beans.XMLDecoder;
import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;

public class InsecureDeserializationJava {
    public Object parse(byte[] data) throws Exception {
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        Object obj = ois.readObject();

        XMLDecoder decoder = new XMLDecoder(new ByteArrayInputStream(data));
        Object xmlObj = decoder.readObject();
        return obj == null ? xmlObj : obj;
    }
}
