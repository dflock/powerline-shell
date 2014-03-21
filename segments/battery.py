import platform
from subprocess import Popen, PIPE


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
        # First, lets (quickly) try to even see if this system _has_ a battery
        line = Popen('wmic path win32_battery get batterystatus', shell=True, stdout=PIPE, stderr=PIPE).stderr.readline()
        if "No Instance" in line:
            # Nope, no battery. Bail out now.
            return

        # We're pretty sure we have a battery, so get its status
        try:
            state = int(Popen('wmic path win32_battery get batterystatus', shell=True, stdout=PIPE).stdout.read().strip().split('\n')[-1])
            charge = int(Popen('wmic path win32_battery get estimatedchargeremaining', shell=True, stdout=PIPE).stdout.read().strip().split('\n')[-1])
        except ValueError:
            # This fails if one of these two commands doesn't result in an int, which
            # probably means that there is no battery to get the status of, so we
            # are pobably on a desktop. Just abort.
            return

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
