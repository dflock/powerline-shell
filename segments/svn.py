import subprocess


def add_svn_segment():
    is_svn = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    is_svn_output = is_svn.communicate()[1].strip()
    if len(is_svn_output) != 0:
        return

    p0 = subprocess.Popen(['svn', 'info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info_raw = p0.communicate()[0].strip()
    info = {}
    for pair in info_raw.split("\n"):
        vals = pair.split(":")
        k = vals[0]
        v = vals[1]
        info[k] = v.strip()
    rev = ""
    if info["Revision"]:
        rev = info["Revision"]

    # Run "svn status | grep -c "^[ACDIMRX\\!\\~]" and parse:
    p1 = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-c', '^[ACDIMR\\!\\~]'], stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0].strip()
    changes = ""
    if len(output) > 0 and int(output) > 0:
        changes = u" \u00B1 %s" % output.strip()

    # Color indicates pending commits
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    if changes:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

    powerline.append(u' %s %s%s ' % (powerline.branch, rev, changes), fg, bg)

try:
    add_svn_segment()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
