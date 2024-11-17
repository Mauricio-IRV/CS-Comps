import subprocess

# Input: A unix command and the lines to print (-1 for no lines)
# Return: A line filtered stdout
def clean_subprocess(command, n = None):
    result = subprocess.run (
        command, 
        shell=True, 
        text=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

    stdout_lines = result.stdout.splitlines()

    if n == -1:
        return
    elif n == 0 < len(stdout_lines):
        return stdout_lines[n]
    elif n == None:
        return "\n".join(stdout_lines)