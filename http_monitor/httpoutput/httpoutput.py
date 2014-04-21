import curses

class Output:

    _stdscr = None
    _trafficscr = None
    _alertsscr = None
    _statsscr = None
    _stats = None

    def __init__(self, stdscr, stats):
        self._stdscr = stdscr
        self._stats = stats
        self.initialize()

    def initialize_borders(self):
        """Draw borders on output to divide the different windows."""
        max_y, max_x = self._stdscr.getmaxyx()
        self._stdscr.border()
        self._stdscr.vline(1, 3*max_x/4, '|', max_y-2)
        self._stdscr.vline(1, max_x/4, '|', max_y-2)
        self._stdscr.refresh()

    def initialize_traffic(self):
        """Initializes the traffic window on the left."""
        max_y, max_x = self._stdscr.getmaxyx()
        self._trafficscr = curses.newwin(max_y-2, max_x/4-1, 1, 1)
        t_y, t_x = self._trafficscr.getmaxyx()
        self._trafficscr.addstr(0,t_x/2 - 4,"Traffic")
        self._trafficscr.hline(1, 0, '=', t_x)
        self._trafficscr.noutrefresh()

    def initialize_alerts(self):
        """Initializes the alerts window in the middle."""
        max_y, max_x = self._stdscr.getmaxyx()
        self._alertsscr = curses.newwin(max_y-2, max_x/2-1, 1, max_x/4+1)
        a_y, a_x = self._alertsscr.getmaxyx()
        self._alertsscr.addstr(0,a_x/2 - 2,"Alerts")
        self._alertsscr.hline(1, 0, '=', a_x)
        self._alertsscr.noutrefresh()

    def initialize_statistics(self):
        """Initializes the statistics window on the right."""
        max_y, max_x = self._stdscr.getmaxyx()
        self._statsscr = curses.newwin(max_y-2, max_x/4-1, 1, 3*max_x/4+1)
        s_y, s_x = self._statsscr.getmaxyx()
        self._statsscr.addstr(0,s_x/2 - 5,"Statistics")
        self._statsscr.hline(1, 0, '=', s_x)
        self._statsscr.noutrefresh()

    def initialize(self):
        """Sets up the windows for console output."""
        curses.curs_set(0)
        self.initialize_borders()
        self.initialize_traffic()
        self.initialize_alerts()
        self.initialize_statistics()
        curses.doupdate()

    def update_traffic(self):
        """Updates the traffic information."""
        self._trafficscr.erase()
        t_y, t_x = self._trafficscr.getmaxyx()
        self._trafficscr.addstr(0,t_x/2 - 4,"Traffic")
        self._trafficscr.hline(1, 0, '=', t_x)
        hits, seconds = self._stats.get_total_traffic()
        self._trafficscr.addstr(3,3, "Last {seconds} seconds:".format(seconds=seconds))
        self._trafficscr.addstr(4,7, "{hits} hits.".format(hits=hits))
        section_dict = self._stats.get_hits_by_section()
        if section_dict is not None:
            line = 6
            self._trafficscr.addstr(line, 3, "Hits by section:")
            line += 1
            for index, domain in enumerate(section_dict):
                self._trafficscr.addstr(line, 3, "{domain}/:".format(domain=domain))
                line += 1
                for section, count in section_dict[domain]:
                    self._trafficscr.addstr(line, 7, "{section}: {count}".format(section=section, count=count))
                    line += 1
        self._trafficscr.noutrefresh()

    def update_alerts(self):
        """Update alerts output."""
        self._alertsscr.erase()
        a_y, a_x = self._alertsscr.getmaxyx()
        self._alertsscr.addstr(0,a_x/2 - 2,"Alerts")
        self._alertsscr.hline(1, 0, '=', a_x)
        alerts = self._stats.get_alerts()
        line = 3
        for alert in alerts:
            if alert[2] is None and curses.has_colors():
                self._alertsscr.addstr(line, 3, "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=alert[0], time=alert[1]), curses.A_BOLD)
            else:
                self._alertsscr.addstr(line, 3, "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=alert[0], time=alert[1]))
            line += 1
            if alert[2] is not None:
                self._alertsscr.addstr(line, 7, "Recovered at {time}.".format(time=alert[2]))
            line += 1
        self._alertsscr.noutrefresh()

    def update(self):
        """Update the output with new values."""
        self.update_traffic()
        # Update miscellaneous self._stats on right side
        self.update_alerts()
        curses.doupdate()
