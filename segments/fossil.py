import os
import subprocess


def get_fossil_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False
    output = os.popen('fossil changes 2>/dev/null').read().strip()
    has_untracked_files = True if os.popen("fossil extras 2>/dev/null").read().strip() else False
    has_missing_files = 'MISSING' in output
    has_modified_files = 'EDITED' in output

    return has_modified_files, has_untracked_files, has_missing_files


def add_fossil_segment():
    # Quick check to see if fossil is even available
    if not subprocess.Popen(['fossil'], stdout=subprocess.PIPE).communicate()[0]:
        return

    branches = os.popen("fossil branch 2> /dev/null").read().strip().split("\n")
    branch = ''.join([i.replace('*', '').strip() for i in branches if i.startswith('*')])
    if len(branch) == 0:
        return

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    has_modified_files, has_untracked_files, has_missing_files = get_fossil_status()
    if has_modified_files or has_untracked_files or has_missing_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
        extra = ''
        if has_untracked_files:
            extra += '+'
        if has_missing_files:
            extra += '!'
        branch += (' ' + extra if extra != '' else '')
    powerline.append(' %s %s ' % (powerline.branch, branch), fg, bg)

try:
    add_fossil_segment()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
