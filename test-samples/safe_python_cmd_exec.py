import subprocess
import shlex


# Safe: Use argument list instead of shell
def safe_ls():
    result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
    return result.stdout


# Safe: Use shlex.quote for dynamic arguments
def safe_grep(pattern):
    safe_pattern = shlex.quote(pattern)
    result = subprocess.run(["grep", safe_pattern, "file.txt"], capture_output=True, text=True)
    return result.stdout


# Safe: Whitelist allowed commands
ALLOWED_COMMANDS = {"date", "whoami", "pwd", "uptime"}


def safe_whitelist(cmd):
    if cmd in ALLOWED_COMMANDS:
        return subprocess.run([cmd], capture_output=True, text=True).stdout
    raise ValueError("Command not allowed")
