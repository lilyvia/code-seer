user_input = "../etc/passwd"
File.open(user_input, "r")
File.read(user_input)
send_file(user_input)
FileUtils.rm(user_input)
FileUtils.rm_rf(user_input)
File.delete(user_input)
File.unlink(user_input)
File.exist?(user_input)
File.directory?(user_input)

def false_negative_expansion_path_ruby(user_path)
  FileUtils.cp(user_path, '/tmp/out')
  FileUtils.mv(user_path, '/tmp/out')
  FileUtils.mkdir_p(user_path)
  IO.read(user_path)
  Dir.entries(user_path)
end
