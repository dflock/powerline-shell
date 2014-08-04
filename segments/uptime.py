import subprocess
import re
import platform
from datetime import datetime


def _get_uptime_win():
    out = subprocess.Popen('net statistics server',
                           shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    boot_line = [line for line in out.split('\r\n') if line][1]
    boot_str = ' '.join(boot_line.split()[2:])
    boot_time = datetime.strptime(boot_str, "%m/%d/%Y %I:%M:%S %p")
    now_time = datetime.now()
    up_time = now_time-boot_time
    days = up_time.days
    hours, remainder = divmod(up_time.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return " ".join(["%sd" % days if days > 0 else "",
                     "%sh" % hours if hours > 0 else "",
                     "%sm" % minutes])


def _get_uptime_lin():
    # uptime output samples
    # 1h:   00:00:00 up 1:00,  2 users,  load average: 0,00, 0,00, 0,00
    # 10+h: 00:00:00 up 10:00,  2 users,  load average: 0,00, 0,00, 0,00
    # 1+d:  00:00:00 up 1 days, 1:00,  2 users,  load average: 0,00, 0,00, 0,00
    # 9+d:  00:00:00 up 12 days, 1:00,  2 users,  load average: 0,00, 0,00, 0,00
    # -1h   00:00:00 up 120 days, 49 min,  2 users,  load average: 0,00, 0,00, 0,00
    # mac:  00:00:00 up 23  3 day(s), 10:00,  2 users,  load average: 0,00, 0,00, 0,00
    try:
        output = subprocess.check_output(['uptime'], stderr=subprocess.STDOUT).decode('utf8')
        raw_uptime = re.search(r'(?<=up).+(?=,\s+\d+\s+user)', output).group(0)
        day_search = re.search(r'\d+(?=\s+day)', output)
        days = '' if not day_search else '%sd' % day_search.group(0)
        hour_search = re.search(r'\d{1,2}(?=\:)', raw_uptime)
        hours = '' if not hour_search else '%sh' % hour_search.group(0)
        minutes = re.search(r'(?<=\:)\d{1,2}|\d{1,2}(?=\s+min)', raw_uptime).group(0)
        return " ".join([days, hours, minutes])
    except OSError:
        return ""


def add_uptime_segment():
    # Linux: Get uptime from the "uptime" command
    if "Linux" in platform.system():
        uptime = _get_uptime_lin()
    # Cygwin: use the Windows "net" command to get uptime
    elif "CYGWIN" in platform.system():
        uptime = _get_uptime_win()
    else:
        warn("Unknown OS '%s'. Uptime unavailable.", platform.system())
        return

    if not uptime:
        return
    else:
        powerline.append(" %s " % uptime, Color.CWD_FG, Color.PATH_BG)

add_uptime_segment()
