using System;
using System.Text.Json;

// Safe: Use JSON instead of XML for untrusted data
public class SafeXxe
{
    public object SafeParse(string json)
    {
        return JsonSerializer.Deserialize<object>(json);
    }
}
