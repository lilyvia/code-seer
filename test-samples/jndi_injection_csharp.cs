using System;
using System.DirectoryServices;

class JndiInjectionCsharp {
    public void VulnerableDirectorySearch(string userFilter) {
        var entry = new DirectoryEntry("LDAP://dc=example,dc=com");
        var searcher = new DirectorySearcher(entry, userFilter);
        searcher.FindAll();
    }

    public void VulnerableDirectoryBind(string userName, string userPassword) {
        var entry = new DirectoryEntry("LDAP://dc=example,dc=com", userName, userPassword);
        entry.RefreshCache();
    }

    public void VulnerableFilterAssignment(string userInput) {
        var searcher = new DirectorySearcher();
        searcher.Filter = $"(uid={userInput})";
        searcher.FindAll();
    }
}
