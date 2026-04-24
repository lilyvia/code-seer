// Safe: Use JSON deserialization with type binding
class SafeDeserializationJava {
    public User safeParse(String json) throws Exception {
        SafeObjectMapper mapper = new SafeObjectMapper();
        return mapper.readValue(json, User.class);
    }

    public User safeTypeSpecificReadValue(String json) throws Exception {
        SafeObjectMapper mapper = new SafeObjectMapper();
        return mapper.readValue(json, User.class);
    }

    public static class User {
        public String name;
        public int age;
    }
}

class SafeObjectMapper {
    <T> T readValue(String json, Class<T> type) throws Exception {
        return type.getDeclaredConstructor().newInstance();
    }
}
