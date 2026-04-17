using System;

class SafeJndiInjectionCsharp {
    public void SafeDirectorySearch() {
        var connection = CreateLdapConnection("dc=example,dc=com");
        var results = connection.Search("(uid=admin)");
    }

    public void SafeDirectoryBind() {
        var connection = CreateLdapConnection("dc=example,dc=com");
        connection.Authenticate("admin", "password");
    }

    private dynamic CreateLdapConnection(string path) {
        return null;
    }
}
