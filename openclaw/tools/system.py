import os

def run_command(cmd):
    return os.popen(cmd).read()
