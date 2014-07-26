import re
import subprocess
import os


def add_git_segment():
    # Quickly check to see if this is even a git repo
    # See http://git-blame.blogspot.com/2013/06/checking-current-branch-programatically.html
    p = subprocess.Popen(
        [
            'git',
            'symbolic-ref',
            '-q',
            'HEAD'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    if err:
        # Maybe its a brand-new, empty repository, so there is no HEAD
        p = subprocess.Popen(["git", "fsck", ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out2, err2 = p.communicate()
        # Check if there is no head yet
        if "HEAD points to an unborn branch" in str(err2):
            # Yup, new/empty repo
            powerline.append(' EMPTY ', Color.REPO_DIRTY_FG, Color.REPO_DIRTY_BG)
            return
        else:
            # Huh. Something is really messed up.
            warn(err2)
            return

    parts = out.decode('UTF-8').split("\n")[:-1]
    git_dir = parts[0]
    inside_gitdir = parts[1] == 'true'
    bare_repo = parts[2] == 'true'
    # inside_worktree = parts[3] == 'true'
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

    # If we haven't found a name for the head yet, try to get one
    if not head:
        with open(os.path.join(git_dir, "HEAD")) as fh:
            # Strip "/refs/heads/"
            parts = fh.read().strip().split('/')
            if len(parts) == 3:
                head = parts[-1]

    # Still no head? Maybe its a tag. Try to get a description.
    if not head:
        p = subprocess.Popen(
            [
                'git',
                'describe',
                '--tags',
                '--exact-match',
                'HEAD'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if not err:
            head = "%s" % out.decode('UTF-8').strip()
            xtra = "|TAG"

    # _Still_ don't have a head? As a last resort, just use the hash
    if not head:
        head = "(%s)" % short_sha
        xtra = "|DETATCHED"

    # Assemble the display data
    if step and total:
        xtra += " %s/%s" % (step, total)
    branch = "%s %s%s" % (powerline.branch, head, xtra)

    if inside_gitdir:
        if bare_repo:
            branch = "BARE:" + branch
        else:
            branch = "GIT_DIR!"

    # Get various status bits about the current repo
    has_pending_commits = True
    has_untracked_files = False
    origin_position = ""

    output = str(subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE).communicate()[0])

    for line in output.split('\n'):
        origin_status = re.findall(
            r"Your branch is (ahead|behind).*?(\d+) comm", line)
        if origin_status:
            origin_position = " %d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += powerline.behind
            if origin_status[0][0] == 'ahead':
                origin_position += powerline.ahead

        if line.find('nothing to commit') >= 0:
            has_pending_commits = False
        if line.find('Untracked files') >= 0:
            has_untracked_files = True

    # Check to see if there is a stash
    has_stash = os.path.exists(os.path.join(git_dir, "refs", "stash"))

    # Color indicates pending commits
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    if has_pending_commits:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

    # Add status flags
    flags = ''.join([
        powerline.stash if has_stash else ''
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
