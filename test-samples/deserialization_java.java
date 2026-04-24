import java.beans.XMLDecoder;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.ObjectInputStream;

class InsecureDeserializationJava {
    public Object parse(byte[] data) throws Exception {
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        Object obj = ois.readObject();

        XMLDecoder decoder = new XMLDecoder(new ByteArrayInputStream(data));
        Object xmlObj = decoder.readObject();
        return obj == null ? xmlObj : obj;
    }
}

class FalseNegativeExpansionDeserJava {
    void false_negative_expansion(Object data, InputStream inputStream, XStream xstream, Yaml yaml, ObjectMapper mapper, Kryo kryo) throws Exception {
        xstream.fromXML(data.toString());
        yaml.load(data.toString());
        mapper.enableDefaultTyping();
        mapper.readValue(data.toString(), Object.class);
        new XMLDecoder(inputStream).readObject();
        new JSONDeserializer().deserialize(data);
        new Gson().fromJson(data.toString(), Object.class);
        kryo.readClassAndObject(inputStream);
        kryo.readObject(inputStream, Object.class);
        new Yaml().loadAll(data.toString());
    }
}

class XStream { Object fromXML(String data) { return data; } }
class Yaml {
    Object load(String data) { return data; }
    Iterable<Object> loadAll(String data) { return java.util.List.of(data); }
}
class ObjectMapper {
    void enableDefaultTyping() {}
    <T> T readValue(String data, Class<T> type) { return null; }
}
class JSONDeserializer { Object deserialize(Object data) { return data; } }
class Gson { <T> T fromJson(String data, Class<T> type) { return null; } }
class Kryo {
    Object readClassAndObject(InputStream input) { return null; }
    <T> T readObject(InputStream input, Class<T> type) { return null; }
}
