import curses

def initialize(stdscr):
    """Draws the borders for console output."""
    curses.curs_set(0)
    stdscr.border()
    max_y, max_x = stdscr.getmaxyx()
    stdscr.hline(2, 1, '=', max_x-2)
    stdscr.vline(1, 3*max_x/4, '|', max_y-2)
    stdscr.vline(1, max_x/4, '|', max_y-2)
    stdscr.addstr(1,max_x/8 - 4,"Traffic")
    stdscr.addstr(1,max_x/2 - 2,"Alerts")
    stdscr.addstr(1,7*max_x/8 - 5,"Statistics")
    stdscr.refresh()

def update(stdscr, calc):
    """Update the output with new values."""
    max_y, max_x = stdscr.getmaxyx()
    # Update total traffic in top left
    hits, seconds = calc.get_total_traffic()
    stdscr.addstr(3,3, "Last {seconds} seconds:".format(seconds=seconds))
    stdscr.addstr(4,7, "{hits} hits.".format(hits=hits))
    # Update miscellaneous calc on right side
    # Update hits by section on left side
    section_dict = calc.get_hits_by_section()
    if section_dict is not None:
        line = 6
        stdscr.addstr(line, 3, "Hits by section:")
        line += 1
        for index, domain in enumerate(section_dict):
            stdscr.addstr(line, 3, "{domain}/:".format(domain=domain))
            line += 1
            for section, count in section_dict[domain]:
                stdscr.addstr(line, 7, "{section}: {count}".format(section=section, count=count))
                line += 1
    # Update alerts in middle
    alerts = calc.get_alerts()
    line = 3
    for alert in alerts:
        if alert[2] is None and curses.has_colors():
            stdscr.addstr(line, max_x/4 + 3, "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=alert[0], time=alert[1]), curses.A_BOLD)
        else:
            stdscr.addstr(line, max_x/4 + 3, "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=alert[0], time=alert[1]))
        line += 1
        if alert[2] is not None:
            stdscr.addstr(line, max_x/4 + 7, "Recovered at {time}.".format(time=alert[2]))
        line += 1
    stdscr.refresh()
