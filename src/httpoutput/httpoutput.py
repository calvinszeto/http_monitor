import curses

def initialize(stdscr):
    """Draws the borders for console output."""
    curses.curs_set(0)
    stdscr.border()
    max_y, max_x = stdscr.getmaxyx()
    stdscr.hline(max_y/3, 1, '_', max_x-2)
    stdscr.vline(1, max_x/4, '|', max_y-2)
    stdscr.refresh()

def update(stdscr, values):
    """Update the output with new values."""
    if "seconds" in values and "total_traffic" in values:
        stdscr.addstr(1,1, "Last {seconds} seconds:".format(seconds=values["seconds"]))
        stdscr.addstr(2,5, "{hits} hits.".format(hits = values["total_traffic"]))
    stdscr.refresh()
