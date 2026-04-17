import java.lang.reflect.Field;
import java.lang.reflect.Method;

class PrototypePollutionJava {
    public void vulnerableSetField(Object obj, String userFieldName, Object userValue) throws Exception {
        obj.getClass().getDeclaredField(userFieldName).set(obj, userValue);
    }

    public void vulnerableSetFieldDirect(Object obj, String userFieldName, Object userValue) throws Exception {
        Class<?> cls = obj.getClass();
        cls.getDeclaredField(userFieldName).set(obj, userValue);
    }

    public void vulnerableInvokeMethod(Object obj, String userMethodName) throws Exception {
        obj.getClass().getDeclaredMethod(userMethodName).invoke(obj);
    }

    public void vulnerableInvokeMethodDirect(Object obj, String userMethodName) throws Exception {
        Class<?> cls = obj.getClass();
        cls.getDeclaredMethod(userMethodName).invoke(obj);
    }
}
