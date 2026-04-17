package main

import (
	"fmt"
	"gopkg.in/ldap.v3"
)

func vulnerableLdapSearch(userInput string) {
	filter := fmt.Sprintf("(uid=%s)", userInput)
	req := ldap.NewSearchRequest("dc=example,dc=com", ldap.ScopeWholeSubtree, ldap.NeverDerefAliases, 0, 0, false, filter, nil, nil)
	_ = req
}

func vulnerableLdapBind(userName, userPassword string) {
	conn, _ := ldap.Dial("tcp", "localhost:389")
	conn.Bind(userName, userPassword)
}
