"""Contains the Stats class for stats and alert logic."""

from http_monitor.httpdb import httpdb
import time

class Stats(object):
    """Holds state and methods for stat calculation and alerts."""

    _alerts = []
    _dbconn = None
    _dbcursor = None
    _threshold_time = 0
    _threshold_amount = 0

    def __init__(self, dbconn, dbcursor, threshold_time, threshold_amount):
        self._dbconn = dbconn
        self._dbcursor = dbcursor
        self._threshold_time = threshold_time
        self._threshold_amount = threshold_amount

    def get_total_traffic(self):
        """Get total traffic for threshold from db and return it."""
        return (httpdb.get_total_traffic(self._dbcursor, self._threshold_time)
            , self._threshold_time)

    def get_alerts(self):
        """Updates any existing alerts or adds new ones if necessary."""
        open_alert = None
        if len(self._alerts) > 0  and self._alerts[0][2] == None:
            open_alert = self._alerts[0]
        total_traffic = self.get_total_traffic()[0]
        if open_alert is not None and total_traffic < self._threshold_amount:
            self._alerts[0][2] = time.strftime("%X")
        elif open_alert is None and total_traffic > self._threshold_amount:
            # Keep alerts in descending time order
            self._alerts.insert(0, [total_traffic, time.strftime("%X"), None])
        return self._alerts

    def get_hits_by_section(self):
        """Get hits by section from db and return them organized.

        Returns hits in a {domain: [(section, hit),...]} structure."""
        section_hits = httpdb.get_hits_by_section(self._dbcursor)
        if not section_hits: # No hits in the database yet
            return None
        section_dict = {}
        for domain, section, count in section_hits:
            if domain in section_dict:
                section_dict[domain] += [(section, count)]
            else:
                section_dict[domain] = list([(section, count)])
        return section_dict

    #def get_misc_stats(self):
        ## Calculate miscellaneous stats here and return them
        #pass
