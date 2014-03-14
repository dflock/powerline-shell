def add_battery_segment():
    charge = 00
    status = "X"
    status_file = "/sys/class/power_supply/BAT0/uevent"  # This is where it is for me...

    state = dict()
    try:
        with open(status_file) as fh:
            # Convert the key=value lines in the file into a dictionary
            lines = fh.readlines()
            state = dict(s.split('=') for s in lines)
    except IOError:
        # This could fail for any number of reasons, but the most likely is that the
        # file called for does not exist (i.e.: you are running on a desktop, or under
        # cygwin, or something). Just assume there is no battery, and don't render
        # a segment.
        return

    charge = int(state["POWER_SUPPLY_CAPACITY"])
    if state["POWER_SUPPLY_STATUS"][0] == 'D':  # "D" for "Discharging"
        status = u'\U0001F50B'  # Battery symbol
    else:
        status = u'\U0001F50C'  # Power plug symbol
        if charge >= 100:  # If fully charged, don't show any status arrows
            charge = 100
            status = ""

    # set colors based on charge state
    if charge > 30:
        bg = Color.BATTERY_NRM_BG
        fg = Color.BATTERY_NRM_FG
    elif charge > 10:
        bg = Color.BATTERY_LOW_BG
        fg = Color.BATTERY_LOW_FG
    else:
        bg = Color.BATTERY_CRT_BG
        fg = Color.BATTERY_CRT_FG

    # Battery symbol, then percentage remaining, then charge status arrow
    powerline.append(" %s%s " % (charge, status), fg, bg)

add_battery_segment()
