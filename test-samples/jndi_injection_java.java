import java.util.Hashtable;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.naming.directory.InitialDirContext;

class JndiInjectionJava {
    public Object vulnerableInitialContextLookup(String userControlledName) throws NamingException {
        return new InitialContext().lookup(userControlledName);
    }

    public Object vulnerableInitialContextWithEnv(String userControlledName) throws NamingException {
        Hashtable<String, String> env = new Hashtable<>();
        env.put("java.naming.factory.initial", "com.sun.jndi.rmi.registry.RegistryContextFactory");
        return new InitialContext(env).lookup(userControlledName);
    }

    public Object vulnerableDirContextLookup(String userControlledName) throws NamingException {
        return new InitialDirContext().lookup(userControlledName);
    }
}
