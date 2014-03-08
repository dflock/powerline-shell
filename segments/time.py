from time import strftime


def add_time_segment():
    powerline.append(" %s " % strftime("%H:%M:%S"), Color.PATH_BG, Color.PATH_FG)


add_time_segment()
