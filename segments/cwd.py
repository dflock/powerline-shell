import os
import sys

# Hack to support `os.path.samefile` under Windows
if "samefile" not in dir(os.path):
    def f(path1, path2):
        # ensure we actually _got_ two comperable arguments...
        if not path1 or not path2:
            return False
        return os.stat(path1) == os.stat(path2)
    os.path.samefile = f

def get_short_path(cwd):
    home = os.getenv('HOME')
    names = cwd.split(os.sep)
    if names[0] == '':
        names = names[1:]
    path = ''
    for i in range(len(names)):
        path += os.sep + names[i]
        if os.path.samefile(path, home):
            return ['~'] + names[i + 1:]
    if not names[0]:
        return ['/']
    return names


def add_cwd_segment():
    cwd = powerline.cwd or os.getenv('PWD')
    if sys.version > '3':
        names = get_short_path(cwd)
    else:
        names = get_short_path(cwd.decode('utf-8'))

    max_depth = powerline.args.cwd_max_depth
    if len(names) > max_depth:
        names = names[:2] + [powerline.ellipses] + names[2 - max_depth:]

    if not powerline.args.cwd_only:
        for name in names[:-1]:
            if name == '~' and Color.HOME_SPECIAL_DISPLAY:
                powerline.append(' %s ' % name, Color.HOME_FG, Color.HOME_BG)
            else:
                powerline.append(' %s ' % name, Color.PATH_FG, Color.PATH_BG,
                                 powerline.separator_thin, Color.SEPARATOR_FG)

    if names[-1] == '~' and Color.HOME_SPECIAL_DISPLAY:
        powerline.append(' %s ' % names[-1], Color.HOME_FG, Color.HOME_BG)
    else:
        powerline.append(' %s ' % names[-1], Color.CWD_FG, Color.PATH_BG)

add_cwd_segment()
