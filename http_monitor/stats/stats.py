from http_monitor.httpdb import httpdb

THRESHOLD_TIME = 120 # seconds
THRESHOLD_AMOUNT = 20 # hits

class Stats:
    
    _alerts = []
    _dbconn = None
    _dbcursor = None
     
    def __init__(self, dbconn, dbcursor):
        self._dbconn = dbconn
        self._dbcursor = dbcursor

    def get_total_traffic(self):
        """Get total traffic for threshold from db and return it."""
        return (httpdb.get_total_traffic(self._dbcursor, THRESHOLD_TIME), THRESHOLD_TIME)

    def get_alerts(self):
        """Updates any existing alerts or adds new ones if threshold is passed."""
        open_alert = None
        if len(self._alerts) > 0  and self._alerts[0][2] == 0:
            open_alert = self._alerts[0]
        total_traffic = self.get_total_traffic()
        if open_alert is not None and total_traffic < THRESHOLD_AMOUNT:
            self._alerts[2] = time.time()
        elif open_alert is None and total_traffic > TRESHOLD_AMOUNT:
            # Keep alerts in descending time order
            self._alerts.insert(0, (total_traffic, time.time(), 0))
        return self._alerts

    def get_hits_by_section(self):
        """Get hits by section from db and return them in a {domain: [(section, hit),...]} structure."""
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

    def get_misc_stats(self):
        # Calculate miscellaneous stats here and return them
        pass
