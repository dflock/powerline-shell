import os
import re
import subprocess
import platform


def add_jobs_segment():
    if "Linux" in platform.system():
        pppid = subprocess.Popen(
            [
                'ps',
                '-p',
                str(os.getppid()),
                '-oppid='
            ], stdout=subprocess.PIPE).communicate()[0].strip()
        output = str(subprocess.Popen(
            [
                'ps',
                '-a',
                '-o',
                'ppid'
            ], stdout=subprocess.PIPE).communicate()[0])
        num_jobs = len(re.findall(str(pppid), output)) - 1

    elif "CYGWIN" in platform.system():
        # PS under Cygwin doesn't support the "-o" option. Have to parse it ourselves.
        ps_out = subprocess.Popen(['ps', '-p', str(os.getppid())], stdout=subprocess.PIPE).communicate()[0]
        pppid = re.search(r'(\d+)', ps_out.split('\n')[1]).group(0)
        output = subprocess.Popen(['ps', '-a'], stdout=subprocess.PIPE).communicate()[0]
        jobs = [line.split() for line in output.split("\n")][1:]
        pids = [job[1] if job else 0 for job in jobs]
        num_jobs = sum(pid == pppid for pid in pids) - 1  # -1 for the instance of PS being run

    else:
        # This _should_ never happen. What are you running this under?
        warn("Unrecognized OS: %s" % platform.system())
        return

    if num_jobs > 0:
        powerline.append(' %d ' % num_jobs, Color.JOBS_FG, Color.JOBS_BG)

add_jobs_segment()
