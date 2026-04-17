class SafePrototypePollutionRuby
  ALLOWED_METHODS = [:name, :email, :age]

  def safe_instance_variable_set(obj, var_name, value)
    allowed_vars = [:@name, :@email, :@age]
    if allowed_vars.include?(var_name.to_sym)
      obj.instance_variable_set(var_name, value)
    end
  end

  def safe_send(obj, method_name, *args)
    if ALLOWED_METHODS.include?(method_name.to_sym)
      obj.call_method(method_name, *args)
    end
  end

  def safe_eval(code)
    # 避免直接eval用户输入
    code
  end
end
