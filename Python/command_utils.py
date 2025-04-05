import subprocess

from logger import Logger

def run_command(logger: Logger, command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0, encoding="utf-8", errors="replace")
    for log_line in map(str.strip, process.stdout):
        logger.info(log_line)
    process.wait()