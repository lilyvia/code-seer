import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Set;

class SafePrototypePollutionJava {
    private static final Set<String> ALLOWED_FIELDS = Set.of("name", "email", "age");
    private static final Set<String> ALLOWED_METHODS = Set.of("getName", "getEmail");

    public void safeSetField(Object obj, String fieldName, Object value) throws Exception {
        if (ALLOWED_FIELDS.contains(fieldName)) {
            Field field = obj.getClass().getDeclaredField(fieldName);
            field.set(obj, value);
        }
    }

    public void safeInvokeMethod(Object obj, String methodName) throws Exception {
        if (ALLOWED_METHODS.contains(methodName)) {
            Method method = obj.getClass().getDeclaredMethod(methodName);
            method.invoke(obj);
        }
    }
}
