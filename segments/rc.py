def add_rc_indicator_segment():
    bg = Color.CMD_PASSED_BG
    fg = Color.CMD_PASSED_FG
    rc = ''
    if powerline.args.prev_error != 0:
        fg = Color.CMD_FAILED_FG
        bg = Color.CMD_FAILED_BG
	rc = str(powerline.args.prev_error)
        powerline.append(rc, fg, bg)

add_rc_indicator_segment()
