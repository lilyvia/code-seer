use ldap3::{LdapConn, Scope};

fn vulnerable_ldap_search(ldap: &mut LdapConn, user_input: &str) -> Result<(), ldap3::LdapError> {
    let filter = format!("(uid={})", user_input);
    ldap.search("dc=example,dc=com", Scope::Subtree, &filter, vec![])?;
    Ok(())
}

fn vulnerable_ldap_bind(ldap: &mut LdapConn, user_name: &str, user_password: &str) -> Result<(), ldap3::LdapError> {
    ldap.bind(user_name, user_password)?;
    Ok(())
}
