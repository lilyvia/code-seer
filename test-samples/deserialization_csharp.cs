using System.IO;

public class InsecureDeserializationCsharp
{
    public object Parse(Stream stream)
    {
        var formatter = new BinaryFormatter();
        var obj = formatter.Deserialize(stream);
        return obj;
    }
}

class FalseNegativeExpansionDeserCSharp {
    void FalseNegativeExpansion(Stream userData, string userJson) {
        new BinaryFormatter().Deserialize(userData);
        new SoapFormatter().Deserialize(userData);
        new LosFormatter().Deserialize(userJson);
        JsonConvert.DeserializeObject(userJson, new JsonSerializerSettings { TypeNameHandling = TypeNameHandling.All });
        new ObjectStateFormatter().Deserialize(userData);
        new NetDataContractSerializer().ReadObject(userData);
        new JavaScriptSerializer().Deserialize(userJson);
        JSON.ToObject(userJson);
    }
}

class BinaryFormatter { public object Deserialize(Stream stream) { return new object(); } }
class SoapFormatter { public object Deserialize(Stream stream) { return new object(); } }
class LosFormatter { public object Deserialize(string data) { return new object(); } }
class ObjectStateFormatter { public object Deserialize(Stream stream) { return new object(); } }
class NetDataContractSerializer { public object ReadObject(Stream stream) { return new object(); } }
class JavaScriptSerializer { public object Deserialize(string data) { return new object(); } }
class JsonSerializerSettings { public TypeNameHandling TypeNameHandling { get; set; } }
enum TypeNameHandling { All }
static class JsonConvert { public static object DeserializeObject(string data, JsonSerializerSettings settings) { return new object(); } }
static class JSON { public static object ToObject(string data) { return new object(); } }
