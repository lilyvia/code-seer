require 'open3'

cmd = params[:cmd]
code = params[:code]

system(cmd)
exec(cmd)
IO.popen(cmd)
Open3.popen3(cmd)
Open3.capture3(cmd)
Open3.popen2(cmd)
eval(code)
instance_eval(code)
class_eval(code)
module_eval(code)
Kernel.eval(code)
`#{cmd}`

def false_negative_expansion_ruby_command(user_cmd)
  Open3.pipeline(user_cmd)
  Open3.pipeline_start(user_cmd)
  spawn(user_cmd)
  %x{#{user_cmd}}
end
