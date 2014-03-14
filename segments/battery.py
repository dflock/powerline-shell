def add_battery_segment():
    charge = 99
    status = "+"
    status_file = "/sys/class/power_supply/BAT0/uevent"

    state = dict()
    try:
        with open(status_file) as fh:
            lines = fh.readlines()
            state = dict(s.split('=') for s in lines)
    except IOError:
        return

    charge = int(state["POWER_SUPPLY_CAPACITY"])
    status = u'\u21E3' if state["POWER_SUPPLY_STATUS"][0] == 'D' else u'\u21E1'
    # status = state["POWER_SUPPLY_STATUS"][0]

    if charge > 99:
        charge = 100
        status = ""

    # print(' %s%s ' % (charge, status))
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

    powerline.append(' %s%s ' % (charge, status), fg, bg)

add_battery_segment()
