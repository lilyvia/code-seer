require 'pathname'

# Safe: Validate user path within base directory
class SafePathTraversal
  def safe_read(base_dir, usr_path)
    base = Pathname.new(base_dir).realpath
    dest = (base + usr_path).realpath
    raise 'Path traversal detected' unless dest.to_s.start_with?(base.to_s + '/')
    File.read(dest)
  end
end
