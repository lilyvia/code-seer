package main

func safeLdapSearch(userInput string) {
	filter := "(uid=admin)"
	_ = filter
}

func safeLdapBind(userName, userPassword string) {
	allowedUsers := map[string]bool{"admin": true, "user1": true}
	if !allowedUsers[userName] {
		return
	}
}
