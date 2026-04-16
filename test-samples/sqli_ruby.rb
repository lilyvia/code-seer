require 'active_record'

user_id = params[:id]
name = params[:name]

User.find_by_sql("SELECT * FROM users WHERE id = #{user_id}")
User.where("name = '#{name}'")
ActiveRecord::Base.connection.execute("DELETE FROM posts WHERE id = #{user_id}")
ActiveRecord::Base.connection.exec_query("UPDATE users SET name = '#{name}' WHERE id = #{user_id}")
