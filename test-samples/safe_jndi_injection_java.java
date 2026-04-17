import java.util.Map;

class SafeJndiInjectionJava {
    private static final Map<String, String> RESOURCE_MAP = Map.of(
        "main", "java:comp/env/jdbc/main",
        "audit", "java:comp/env/jdbc/audit"
    );

    public String resolveResourceName(String resourceKey) {
        String resourceName = RESOURCE_MAP.get(resourceKey);
        if (resourceName == null) {
            return "unknown";
        }
        return resourceName;
    }
}
