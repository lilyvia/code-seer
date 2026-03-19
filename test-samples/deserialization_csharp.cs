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
