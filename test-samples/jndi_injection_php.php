<?php

class JndiInjectionPhp {
    public function vulnerableLdapSearch($conn, $userInput) {
        $filter = "(uid=" . $userInput . ")";
        ldap_search($conn, "dc=example,dc=com", $filter);
    }

    public function vulnerableLdapBind($conn, $userName, $userPassword) {
        ldap_bind($conn, $userName, $userPassword);
    }

    public function vulnerableLdapList($conn, $userInput) {
        $filter = "(uid=" . $userInput . ")";
        ldap_list($conn, "dc=example,dc=com", $filter);
    }
}
