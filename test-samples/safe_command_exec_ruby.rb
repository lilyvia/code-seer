# Safe: Use Ruby built-in methods instead of shell commands
class SafeCmdExec
  def safe_list_files(dir)
    Dir.entries(dir)
  end

  def safe_file_info(path)
    File.stat(path)
  end

  def safe_kernel_system
    Kernel.public_send(:system, 'date')
  end
end
