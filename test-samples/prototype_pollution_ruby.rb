class PrototypePollutionRuby
  def vulnerable_instance_variable_set(obj, user_var_name, user_value)
    obj.instance_variable_set(user_var_name, user_value)
  end

  def vulnerable_send(obj, user_method_name, *args)
    obj.send(user_method_name, *args)
  end

  def vulnerable_public_send(obj, user_method_name, *args)
    obj.public_send(user_method_name, *args)
  end

  def vulnerable_eval(user_code)
    eval(user_code)
  end

  def vulnerable_instance_eval(obj, user_code)
    obj.instance_eval(user_code)
  end

  def vulnerable_class_eval(user_code)
    Object.class_eval(user_code)
  end
end
