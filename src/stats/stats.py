from httpdb import httpdb

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
        # Check for an open alert
        # Check if total traffic is over threshold
        # If alert is open and traffic is under threshold, find time when traffic went under
        # If no open alert and traffic is over threshold, find time when traffic went over
            # Add a new open alert
        # Return all alerts in order
        pass

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
