import ldap3

class SafeJndiInjectionPython:
    def safe_ldap_search(self, conn):
        filter_str = "(uid=admin)"
        conn.search('dc=example,dc=com', filter_str)

    def safe_ldap_bind(self, conn):
        conn.bind('admin', 'password')
