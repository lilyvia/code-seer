import os
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
