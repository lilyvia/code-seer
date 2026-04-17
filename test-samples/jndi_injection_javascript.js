const ldap = require('ldapjs');

function vulnerableLdapSearch(client, userInput) {
    const filter = `(uid=${userInput})`;
    client.search('dc=example,dc=com', { filter }, (err, res) => {
        // ...
    });
}

function vulnerableLdapBind(client, userName, userPassword) {
    client.bind(userName, userPassword, (err) => {
        // ...
    });
}

function vulnerableLdapSearchDirect(client, userFilter) {
    client.search('dc=example,dc=com', { filter: userFilter }, (err, res) => {
        // ...
    });
}
