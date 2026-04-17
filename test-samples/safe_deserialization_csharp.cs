using System;
using System.Text.Json;

// Safe: Use JSON deserialization with type constraints
public class SafeDeserialization
{
    public User SafeParse(string json)
    {
        return JsonSerializer.Deserialize<User>(json);
    }
}

public class User
{
    public string Name { get; set; }
    public int Age { get; set; }
}
