#!/usr/bin/env python
import os
import stat
import sys

try:
    import config
except ImportError:
    print('Created personal config.py for your customizations')
    import shutil
    shutil.copyfile('config.py.dist', 'config.py')
    import config

TEMPLATE_FILE = 'powerline-shell.py.template'
OUTPUT_FILE = 'powerline-shell.py'
SEGMENTS_DIR = 'segments'
THEMES_DIR = 'themes'


def load_source(srcfile):
    try:
        return ''.join(open(srcfile).readlines()) + '\n\n'
    except IOError:
        print('Could not open', srcfile)
        return ''

if __name__ == "__main__":
    source = load_source(TEMPLATE_FILE)
    source += load_source(os.path.join(THEMES_DIR, 'default.py'))

    # Load any specified theme
    if config.THEME != "default":
        source += load_source(os.path.join(THEMES_DIR, config.THEME + '.py'))

    # Load segments
    for segment in config.SEGMENTS:
        source += load_source(os.path.join(SEGMENTS_DIR, segment + '.py'))

    # Load any right-to-left segments
    if config.RIGHT_SEGMENTS:
        for segment in config.RIGHT_SEGMENTS:
            source += load_source(os.path.join(SEGMENTS_DIR, segment + '.py'))

    source += '''
import sys
if sys.version > '3':
    sys.stdout.buffer.write(powerline.draw())
else:
    sys.stdout.write(powerline.draw())
'''

    try:
        open(OUTPUT_FILE, 'w').write(source)
        st = os.stat(OUTPUT_FILE)
        os.chmod(OUTPUT_FILE, st.st_mode | stat.S_IEXEC)
        print('%s saved successfully' % OUTPUT_FILE)
    except IOError:
        print('ERROR: Could not write to powerline-shell.py. Make sure it is writable')
        exit(1)
