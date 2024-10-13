import subprocess

def clean_subprocess(command, n):
    result = subprocess.run (
        command, 
        shell=True, 
        text=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

    stdout_lines = result.stdout.splitlines()

    if n == -1:
        return []
    if 0 <= n < len(stdout_lines):
        return stdout_lines[n]
    else:
        return stdout_lines[0]