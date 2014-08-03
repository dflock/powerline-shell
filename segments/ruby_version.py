import subprocess
import os


def add_ruby_version_segment():
    try:
        process1 = subprocess.Popen(["ruby", "-v"], stdout=subprocess.PIPE)
        process2 = subprocess.Popen(["sed", "s/ (.*//"], stdin=process1.stdout, stdout=subprocess.PIPE)
        version = process2.communicate()[0].rstrip()
        if "GEM_HOME" in os.environ:
            gem = os.environ["GEM_HOME"].split("@")
            if len(gem) > 1:
                version += " " + gem[1]
        powerline.append(version, 15, 1)
    except OSError:
        return

add_ruby_version_segment()
