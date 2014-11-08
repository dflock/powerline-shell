class Color(DefaultColor):
    """
    This subclass is required when the user chooses to use 'default' theme.
    Because the segments require a 'Color' class for every theme.
    """
    USERNAME_FG = 250
    USERNAME_BG = 240
    USERNAME_ROOT_BG = 124

    HOSTNAME_FG = 240 # dark grey
    HOSTNAME_BG = 148

    HOME_SPECIAL_DISPLAY = True
    HOME_BG = 31  # cyan
    HOME_FG = 15  # white
    PATH_BG = 31  # cyan
    PATH_FG = 15  # light grey
    CWD_FG = 254  # nearly-white grey
    SEPARATOR_FG = 237 # dark grey

    READONLY_BG = 124
    READONLY_FG = 254

    SSH_BG = 166 # medium orange
    SSH_FG = 254

    REPO_CLEAN_BG = 148  # a light green color
    REPO_CLEAN_FG = 0  # black
    REPO_DIRTY_BG = 161  # pink/red
    REPO_DIRTY_FG = 15  # white

    JOBS_FG = 39
    JOBS_BG = 238

    CMD_PASSED_BG = 236
    CMD_PASSED_FG = 15
    CMD_FAILED_BG = 161
    CMD_FAILED_FG = 15

    SVN_CHANGES_BG = 148
    SVN_CHANGES_FG = 22  # dark green

    VIRTUAL_ENV_BG = 166 # medium orange
    VIRTUAL_ENV_FG = 00
