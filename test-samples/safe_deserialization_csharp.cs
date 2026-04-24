// Safe: Use JSON deserialization with type constraints
public class SafeDeserialization
{
    public User SafeParse(string json)
    {
        return JsonConvert.DeserializeObject<User>(json);
    }
}

public class User
{
    public string Name { get; set; }
    public int Age { get; set; }
}

static class JsonConvert
{
    public static T DeserializeObject<T>(string json) where T : new()
    {
        return new T();
    }
}
