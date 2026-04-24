using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

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
    }
}
