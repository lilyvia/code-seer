<?php

class SafeJndiInjectionPhp {
    public function safeLdapSearch($conn) {
        $filter = "(uid=admin)";
        $this->executeLdapQuery($conn, "dc=example,dc=com", $filter);
    }

    public function safeLdapBind($conn) {
        $this->authenticate($conn, "admin", "password");
    }

    private function executeLdapQuery($conn, $base, $filter) {
        // 安全的LDAP查询实现
    }

    private function authenticate($conn, $user, $pass) {
        // 安全的认证实现
    }
}
