class DefaultColor:
    """
    This class should have the default colors for every segment.
    Please test every new segment with this theme first.
    """
    USERNAME_FG = 250
    USERNAME_BG = 240
    USERNAME_ROOT_BG = 124

    HOSTNAME_FG = 250
    HOSTNAME_BG = 238

    HOME_SPECIAL_DISPLAY = True
    HOME_BG = 31            # blueish
    HOME_FG = 15            # white
    PATH_BG = 237           # dark grey
    PATH_FG = 250           # light grey
    CWD_FG = 254            # nearly-white grey
    SEPARATOR_FG = 244

    READONLY_BG = 124       # red
    READONLY_FG = 254       # white

    SSH_BG = 166            # medium orange
    SSH_FG = 254

    REPO_CLEAN_BG = 148     # a light green color
    REPO_CLEAN_FG = 22      # dark green
    REPO_DIRTY_BG = 161     # pink/red
    REPO_DIRTY_FG = 15      # white

    JOBS_FG = 39
    JOBS_BG = 238

    CMD_PASSED_BG = 236     # dark gray
    CMD_PASSED_FG = 15      # white
    CMD_FAILED_BG = 161     # light red/pink
    CMD_FAILED_FG = 15      # white

    SVN_CHANGES_BG = 148    # light green
    SVN_CHANGES_FG = 22     # dark green

    VIRTUAL_ENV_BG = 35     # a mid-tone green
    VIRTUAL_ENV_FG = 236    # black

    BATTERY_NRM_BG = 22
    BATTERY_NRM_FG = 254
    BATTERY_LOW_BG = 118
    BATTERY_LOW_FG = 237
    BATTERY_CRT_BG = 9
    BATTERY_CRT_FG = 147

class Color(DefaultColor):
    """
    This subclass is required when the user chooses to use 'default' theme.
    Because the segments require a 'Color' class for every theme.
    """
    pass
