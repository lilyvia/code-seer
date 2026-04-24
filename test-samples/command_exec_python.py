import os
import pty
import subprocess


def vulnerable_os_system(user_input):
    os.system(user_input)


def vulnerable_subprocess_shell(command):
    subprocess.run(command, shell=True)


def vulnerable_eval(user_code):
    return eval(user_code)


def vulnerable_exec(user_code):
    exec(user_code)


def safe_usage():
    subprocess.run(["ls", "-la"], check=True, capture_output=True, text=True)

async def false_negative_expansion_async_command(asyncio, user_cmd):
    await asyncio.create_subprocess_shell(user_cmd)
    await asyncio.create_subprocess_exec("sh", "-c", user_cmd)

def false_negative_expansion_ssh(ssh, conn, pexpect, user_cmd):
    ssh.exec_command(user_cmd)
    conn.run(user_cmd)
    pexpect.spawn(user_cmd)


def false_negative_expansion_additional_sinks(user_input, user_cmd):
    # Vulnerable: user-controlled command reaches shell helpers.
    subprocess.getoutput(user_input)
    subprocess.getstatusoutput(user_input)
    pty.spawn(user_cmd)
