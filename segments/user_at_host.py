def get_colors_for_hostname(hostname):
    from binascii import crc32
    cmin = 17     # min ANSI color to use
    cmax = 231    # max ANSI color to use

    # color ranges that should use white FG
    white_fg = (
        range(16, 34), range(52, 70), range(88, 106),
        range(124, 136), range(160, 172), range(196, 208)
    )

    crange = cmax - cmin + 1
    bg = (crc32(hostname.encode('utf8')) % crange) + cmin
    fg = 7 if (True in [bg in r for r in white_fg]) else 8
    return (fg, bg)


def add_user_at_host_segment():
    import os
    import socket

    hostname = socket.gethostname()

    if powerline.args.shell == 'bash':
        host_prompt = ' \\h '
        user_prompt = ' \\u '
    elif powerline.args.shell == 'zsh':
        host_prompt = ' %m '
        user_prompt = ' %n '
    else:
        host_prompt = ' %s ' % hostname.split('.')[0]
        user_prompt = ' %s ' % os.getenv('USER')

    if powerline.args.colorize_hostname:
        FG, BG = get_colors_for_hostname(hostname)
    else:
        FG = Color.HOSTNAME_FG
        BG = Color.HOSTNAME_BG

    if os.getenv('USER') == 'root':
        # Root use colour overrides host colour
        BG = Color.USERNAME_ROOT_BG

    powerline.append(str(user_prompt).rstrip() + '@' + str(host_prompt).lstrip(), FG, BG)

add_user_at_host_segment()
