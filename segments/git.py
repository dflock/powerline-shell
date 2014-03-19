import re
import subprocess
import os
import sys
from distutils.version import LooseVersion

def add_git_segment():
    # Quickly check to see if this is even a git repo
    # See http://git-blame.blogspot.com/2013/06/checking-current-branch-programatically.html
    p = subprocess.Popen(['git', 'symbolic-ref', '-q', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if 'Not a git repo' in str(err):
        return

    # Get some more info about the repo
    p = subprocess.Popen(
        [
            "git",
            "rev-parse",
            "--git-dir",
            "--is-inside-git-dir",
            "--is-bare-repository",
            "--is-inside-work-tree",
            "--short",
            "HEAD",
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    parts = out.decode('UTF-8').split("\n")[:-1]
    git_dir = parts[0]
    inside_gitdir = parts[1] == 'true'
    bare_repo = parts[2] == 'true'
    inside_worktree = parts[3] == 'true'
    short_sha = parts[4]

    xtra = ""
    head = ""
    step = ""
    total = ""
    # See if we are in a rebase/merge
    if os.path.isdir(os.path.join(git_dir, "rebase-merge")):
        with open(os.path.join(git_dir, "rebase-merge", "head-name")) as fh:
            head = fh.read().strip()
        with open(os.path.join(git_dir, "rebase-merge", "msgnum")) as fh:
            step = fh.read().strip()
        with open(os.path.join(git_dir, "rebase-merge", "end")) as fh:
            total = fh.read().strip()
        if os.path.exists(os.path.join(git_dir, "rebase-merge", "interactive")):
            xtra = "|REBASE-i"
        else:
            xtra = "|REBASE-m"
    else:
        # Not in a rebase/merge, something else must be going on...
        if os.path.isdir(os.path.join(git_dir, "rebase-apply")):
            with open(os.path.join(git_dir, "rebase-apply", "next")) as fh:
                step = fh.read().strip()
            with open(os.path.join(git_dir, "rebase-apply", "last")) as fh:
                total = fh.read().strip()
            if os.path.exists(os.path.join(git_dir, "rebase-apply", "rebasing")):
                with open(os.path.join(git_dir, "rebase-apply", "head-name")) as fh:
                    head = fh.read().strip()
                xtra = "|REBASE"
            elif os.path.exists(os.path.join(git_dir, "rebase-apply", "applying")):
                xtra = "|AM"
            else:
                xtra = "|AM/REBASE"
        elif os.path.exists(os.path.join(git_dir, "MERGE_HEAD")):
            xtra = "|MERGING"
        elif os.path.exists(os.path.join(git_dir, "CHERRY_PICK_HEAD")):
            xtra = "|CHERRY-PICKING"
        elif os.path.exists(os.path.join(git_dir, "REVERT_HEAD")):
            xtra = "|REVERTING"
        elif os.path.exists(os.path.join(git_dir, "BISECT_LOG")):
            xtra = "|BISECTING"

        # As a last resort, just get whatever head you can
        if not head:
            with open(os.path.join(git_dir, "HEAD")) as fh:
                head = fh.read().strip()

        # Strip "/refs/heads/"
        if head:
            parts = head.split('/')
            if len(parts) == 3:
                head = parts[-1]
            else:
                head = "(%s)" % short_sha

    # Assemble the display data
    if step and total:
        xtra += " %s/%s" % (step, total)

    branch = head + xtra

    if inside_gitdir:
        if bare_repo:
            branch = "BARE:"
        else:
            branch = "GIT_DIR!"

    # See if therer is anything stashed
    has_stash = os.path.exists(os.path.join(git_dir, "refs", "stash"))

    # Get various status bits about the current repo
    has_pending_commits = True
    has_untracked_files = False
    origin_position = ""
    git_ver = str(subprocess.Popen(['git', '--version'], stdout=subprocess.PIPE).communicate()[0])
    ver = re.findall(r"(?:.* )([\d.]+)", git_ver)[0]
    if LooseVersion(ver) > LooseVersion('1.7.5'):
        output = str(subprocess.Popen(['git', 'status', '--ignore-submodules'], stdout=subprocess.PIPE).communicate()[0])
    else:
        output = str(subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE).communicate()[0])
    for line in output.split('\n'):
        origin_status = re.findall(
            r"Your branch is (ahead|behind).*?(\d+) comm", line)
        if origin_status:
            origin_position = " %d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += u'\u21E3'
            if origin_status[0][0] == 'ahead':
                origin_position += u'\u21E1'

        if line.find('nothing to commit') >= 0:
            has_pending_commits = False
        if line.find('Untracked files') >= 0:
            has_untracked_files = True

    # Color indicates pending commits
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    if has_pending_commits:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

    # Status flags
    flags = ''.join([
        u'\u00A7' if has_stash else ''
        '+' if has_untracked_files else '',
    ])
    if flags:
        branch += " " + flags
    branch += origin_position

    powerline.append(' %s ' % branch, fg, bg)

try:
    add_git_segment()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
