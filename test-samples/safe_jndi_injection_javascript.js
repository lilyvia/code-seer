const ldap = require('ldapjs');

function safeLdapSearch(client) {
    const filter = '(uid=admin)';
    client.search('dc=example,dc=com', { filter }, (err, res) => {
        // ...
    });
}

function safeLdapBind(client) {
    const credentials = { username: 'admin', password: 'password' };
    client.authenticate(credentials, (err) => {
        // ...
    });
}
