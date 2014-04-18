def initialize(stdscr):
    """Draws the borders for console output."""
    curses.curs_set(0)
    stdscr.border()
    max_y, max_x = stdscr.getmaxyx()
    stdscr.hline(max_y/3, 1, '_', max_x-2)
    stdscr.vline(1, max_x/4, '_', max_x-2)
    stdscr.refresh()
