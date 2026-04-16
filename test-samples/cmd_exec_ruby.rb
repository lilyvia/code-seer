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
