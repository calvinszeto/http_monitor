import curses

def initialize(stdscr):
    """Draws the borders for console output."""
    curses.curs_set(0)
    stdscr.border()
    max_y, max_x = stdscr.getmaxyx()
    stdscr.vline(1, 3*max_x/4, '|', max_y-2)
    stdscr.vline(1, max_x/4, '|', max_y-2)
    stdscr.refresh()

def update(stdscr, calc):
    """Update the output with new values."""
    max_y, max_x = stdscr.getmaxyx()
    # Update total traffic in top left
    hits, seconds = calc.get_total_traffic()
    stdscr.addstr(1,1, "Last {seconds} seconds:".format(seconds=seconds))
    stdscr.addstr(2,5, "{hits} hits.".format(hits=hits))
    # Update miscellaneous calc on right side
    # Update hits by section on left side
    section_dict = calc.get_hits_by_section()
    if section_dict is not None:
        line = max_y/3 + 1
        stdscr.addstr(line, 1, "Hits by section:")
        line += 1
        for index, domain in enumerate(section_dict):
            stdscr.addstr(line, 1, "{domain}/:".format(domain=domain))
            line += 1
            for section, count in section_dict[domain]:
                stdscr.addstr(line, 5, "{section}: {count}".format(section=section, count=count))
                line += 1
    # Update alerts in middle
    alerts = calc.get_alerts()
    line = 1 + len(alerts) * 2 
    for alert in alerts:
        if alert[2] != 0:
            stdscr.addstr(line, max_x/4 + 5, "Recovered at {time}.".format(time=alert[2]))
        line -= 1
        stdscr.addstr(line, max_x/4 + 1, "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=alert[0], time=alert[1]))
        line -= 1
    stdscr.refresh()
