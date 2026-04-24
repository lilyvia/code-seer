# Safe: Use ActiveRecord safe query methods
class SafeSqli
  def find_user(id)
    User.find(id)
  end

  def find_by_name(nm)
    User.find_by(name: nm)
  end

  def delete_post(id)
    Post.find(id).destroy
  end

  def safe_select_all(id)
    sql = ActiveRecord::Base.sanitize_sql_array(['SELECT * FROM users WHERE id = ?', id])
    ActiveRecord::Base.connection.public_send(:select_all, sql)
  end
end
