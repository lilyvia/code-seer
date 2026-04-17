require 'net/ldap'

class SafeJndiInjectionRuby
  def safe_ldap_search(ldap)
    filter = Net::LDAP::Filter.eq('uid', 'admin')
    ldap.search(base: 'dc=example,dc=com', filter: filter)
  end

  def safe_ldap_bind(ldap)
    ldap.bind(method: :simple, username: 'admin', password: 'password')
  end
end
