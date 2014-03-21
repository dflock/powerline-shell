import platform
import os

def add_battery_segment():
    charge = 00
    status = "X"
    if "Linux" in platform.system():
        status_file = "/sys/class/power_supply/BAT0/uevent"  # This is where it is for me...
        lines = []
        try:
            with open(status_file) as fh:
                # Convert the key=value lines in the file into a dictionary
                lines = fh.readlines()
        except IOError:
            # This could fail for any number of reasons, but the most likely is that the
            # file called for does not exist (i.e.: you are running on a desktop, or something).
            # Just assume there is no battery, and don't render a segment.
            return

        state = dict(s.split('=') for s in lines)

        charge = int(state["POWER_SUPPLY_CAPACITY"])
        if 'Discharging' in state["POWER_SUPPLY_STATUS"][0] == 'D':
            status = powerline.discharge
        else:
            status = powerline.charge
    elif "CYGWIN" in platform.system():
        charge = int(os.popen('wmic path win32_battery get estimatedchargeremaining').read().strip().split('\n')[-1])
        state = int(os.popen('wmic path win32_battery get batterystatus').read().strip().split('\n')[-1])
        if state == 1:
            status = powerline.discharge
        else:
            status = powerline.charge

    else:
        warn("Unknown OS '%s'. Battery status unavailable.", platform.system())
        return

    if charge >= 100:  # If fully charged, don't show any status symbol
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

    # Battery symbol, then percentage remaining, then charge status symbol
    powerline.append(" %s%s " % (charge, status), fg, bg)

add_battery_segment()
