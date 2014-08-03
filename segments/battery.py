import platform
from subprocess import Popen, PIPE


class BatteryException(Exception):
    pass


def _get_bat_status_win():
    # First, lets (quickly) try to even see if this system _has_ a battery
    line = Popen('wmic path win32_battery get batterystatus', shell=True, stdout=PIPE, stderr=PIPE).stderr.readline()
    if "No Instance" in line:
        # Nope, no battery. Bail out now.
        raise BatteryException("No battery in system")

    # We're pretty sure we have a battery, so get its status
    try:
        out = Popen('wmic path win32_battery get batterystatus',
                    shell=True, stdout=PIPE).stdout.read().strip()
        state = int(out.split('\n')[-1])
        out = Popen('wmic path win32_battery get estimatedchargeremaining',
                    shell=True, stdout=PIPE).stdout.read().strip()
        charge = int(out.split('\n')[-1])
    except ValueError:
        # This fails if one of these two commands doesn't parse correctly into
        # an int, which probably means that there is no battery to get the status
        # of, so we are pobably on a desktop. Just abort.
        raise BatteryException("Couldn't parse charge state")

    status = powerline.discharge if state == 1 else powerline.charge

    return(status, charge)


def _get_bat_status_lin():
    status_file = "/sys/class/power_supply/BAT0/uevent"  # This is where it is for me...
    lines = []
    try:
        with open(status_file) as handle:
            # Convert the key=value lines in the file into a dictionary
            lines = handle.readlines()
    except IOError:
        # This could fail for any number of reasons, but the most likely is that the
        # file called for does not exist (i.e.: you are running on a desktop, or something).
        # Just assume there is no battery, and don't render a segment.
        raise BatteryException("Can't open battery status file: %s" % status_file)

    # The status file could contain a bunch of key-value pairs structured as:
    #    KEY=value
    state = dict(s.split('=') for s in lines)

    charge = int(state["POWER_SUPPLY_CAPACITY"])
    status = powerline.discharge if 'Discharging' in state["POWER_SUPPLY_STATUS"] else powerline.charge

    return (status, charge)


def add_battery_segment():
    try:
        # Linux: Read battery status from a system file
        if "Linux" in platform.system():
            status, charge = _get_bat_status_lin()
        # Cygwin: use the Windows Management Instrumentation Command-line (wmic) to get battery status
        elif "CYGWIN" in platform.system():
            status, charge = _get_bat_status_win()
        else:
            warn("Unknown OS '%s'. Battery status unavailable.", platform.system())
            return
    except BatteryException:
        # If we had trouble getting the battery info, just quit now.
        return

    # Make sure it actually worked...
    if not charge or not status:
        return

    if charge >= 100:  # If fully charged, don't show any status symbol
        charge = 100
        status = ""

    # Set colors based on charge state
    # TODO: These thresholds really should come from the system's power profile
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
