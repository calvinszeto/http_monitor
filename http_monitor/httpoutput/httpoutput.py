import curses

class Output:

    _stdscr = None
    _stats = None

    def __init__(self, stdscr, stats):
        self._stdscr = stdscr
        self._stats = stats
        self.initialize()

    def initialize(self):
        """Draws the borders for console output."""
        curses.curs_set(0)
        self._stdscr.border()
        max_y, max_x = self._stdscr.getmaxyx()
        self._stdscr.hline(2, 1, '=', max_x-2)
        self._stdscr.vline(1, 3*max_x/4, '|', max_y-2)
        self._stdscr.vline(1, max_x/4, '|', max_y-2)
        self._stdscr.addstr(1,max_x/8 - 4,"Traffic")
        self._stdscr.addstr(1,max_x/2 - 2,"Alerts")
        self._stdscr.addstr(1,7*max_x/8 - 5,"Statistics")
        self._stdscr.refresh()

    def update(self):
        """Update the output with new values."""
        max_y, max_x = self._stdscr.getmaxyx()
        # Update total traffic in top left
        hits, seconds = self._stats.get_total_traffic()
        self._stdscr.addstr(3,3, "Last {seconds} seconds:".format(seconds=seconds))
        self._stdscr.addstr(4,7, "{hits} hits.".format(hits=hits))
        # Update miscellaneous self._stats on right side
        # Update hits by section on left side
        section_dict = self._stats.get_hits_by_section()
        if section_dict is not None:
            line = 6
            self._stdscr.addstr(line, 3, "Hits by section:")
            line += 1
            for index, domain in enumerate(section_dict):
                self._stdscr.addstr(line, 3, "{domain}/:".format(domain=domain))
                line += 1
                for section, count in section_dict[domain]:
                    self._stdscr.addstr(line, 7, "{section}: {count}".format(section=section, count=count))
                    line += 1
        # Update alerts in middle
        alerts = self._stats.get_alerts()
        line = 3
        for alert in alerts:
            if alert[2] is None and curses.has_colors():
                self._stdscr.addstr(line, max_x/4 + 3, "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=alert[0], time=alert[1]), curses.A_BOLD)
            else:
                self._stdscr.addstr(line, max_x/4 + 3, "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=alert[0], time=alert[1]))
            line += 1
            if alert[2] is not None:
                self._stdscr.addstr(line, max_x/4 + 7, "Recovered at {time}.".format(time=alert[2]))
            line += 1
        self._stdscr.refresh()
