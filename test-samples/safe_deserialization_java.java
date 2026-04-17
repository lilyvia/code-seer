import com.fasterxml.jackson.databind.ObjectMapper;

// Safe: Use JSON deserialization with type binding
public class SafeDeserializationJava {
    public User safeParse(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(json, User.class);
    }

    public static class User {
        public String name;
        public int age;
    }
}
