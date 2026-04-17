require 'net/ldap'

class JndiInjectionRuby
  def vulnerable_ldap_search(ldap, user_input)
    filter = "(uid=#{user_input})"
    ldap.search(base: 'dc=example,dc=com', filter: filter)
  end

  def vulnerable_ldap_bind(ldap, user_name, user_password)
    ldap.bind(method: :simple, username: user_name, password: user_password)
  end

  def vulnerable_filter_construct(user_input)
    filter = Net::LDAP::Filter.construct("(uid=#{user_input})")
    filter
  end
end
