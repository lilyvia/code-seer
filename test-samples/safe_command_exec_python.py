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


# Safe: hardcoded commands do not include user-controlled data
def safe_false_negative_expansion():
    get_output = subprocess.getoutput
    get_status_output = subprocess.getstatusoutput
    get_output("date")
    get_status_output("whoami")
    return subprocess.run(["pwd"], capture_output=True, text=True).stdout
