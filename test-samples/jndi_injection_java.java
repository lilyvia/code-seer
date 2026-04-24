import java.util.Hashtable;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.naming.directory.InitialDirContext;
import javax.naming.spi.NamingManager;

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

    public Object vulnerableContextLookup(String userControlledName) throws NamingException {
        Context ctx = new InitialContext();
        return ctx.lookup(userControlledName);
    }

    public Object vulnerableContextLookupLink(String userControlledName) throws NamingException {
        Context ctx = new InitialContext();
        return ctx.lookupLink(userControlledName);
    }

    public Object vulnerableNamingManagerLookup(String userControlledName) throws NamingException {
        Hashtable<String, String> env = new Hashtable<>();
        return NamingManager.getURLContext("rmi", env).lookup(userControlledName);
    }

    public Object vulnerableStaticDoLookup(String userControlledName) throws NamingException {
        return javax.naming.InitialContext.doLookup(userControlledName);
    }
}

class FalseNegativeExpansionJndiJava {
    void false_negative_expansion(JndiTemplate template, JndiLocatorDelegate delegate, DirContext dir, String userName) throws Exception {
        template.lookup(userName);
        delegate.lookup(userName);
        dir.search("dc=example", userName, null);
        NamingManager.getURLContext(userName, null);
    }
}
