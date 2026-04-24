import java.util.Map;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

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

    public Object safeLocalLookup() throws NamingException {
        Context ctx = new InitialContext();
        return ctx.lookup("java:comp/env/jdbc/main");
    }

    public Object safeFixedResourceLookup() throws NamingException {
        Context ctx = new InitialContext();
        return ctx.lookup("java:comp/env/jms/auditQueue");
    }
}
