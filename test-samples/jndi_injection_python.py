import ldap3

class JndiInjectionPython:
    def vulnerable_ldap_search(self, conn, user_input):
        filter_str = f"(uid={user_input})"
        conn.search('dc=example,dc=com', filter_str)

    def vulnerable_ldap_bind(self, conn, user_name, user_password):
        conn.bind(user_name, user_password)

    def vulnerable_ldap_search_direct(self, conn, user_filter):
        conn.search('dc=example,dc=com', user_filter)
