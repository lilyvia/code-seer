user_input = "../etc/passwd"
open(user_input, "r")

def false_negative_expansion_path_python(user_path, content, shutil, archive):
    Path(user_path).read_text()
    Path(user_path).write_text(content)
    shutil.copy(user_path, '/tmp/out')
    shutil.move(user_path, '/tmp/out')
    shutil.rmtree(user_path)
    archive.extractall(user_path)
