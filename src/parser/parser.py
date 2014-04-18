import re
from dateutil import parser
from dateutil import tz
import datetime

log_pattern = re.compile('(.*?) (.*?) (.*?) \[(.*?)\] "(.*?)" (.*?) (.*)')
request_pattern = re.compile('([A-Z]+) (.*?)\/(.*?)((?:\/.+)*) (.*)')

def parse_w3log(line):
    """Parses a W3C Log line and returns the resulting values or None if not properly formed."""
    # Parse the given line with a regex
    results = log_pattern.match(line).groups()
    # Check if the given line is a proper log line
    wrong_date = datetime.datetime(datetime.MINYEAR,1,1, tzinfo=tz.tzlocal())
    has_date = parser.parse(results[3], fuzzy=True, default=wrong_date) != wrong_date
    has_proper_request = request_pattern.match(results[4]) is not None
    if results is not None and has_date and has_proper_request:
        host, logname, authuser, date, request, status, bites = results
        # Clean up parsed strings
        values = {} 
        values['host'] = host if host != '' else None
        values['logname'] = logname if logname != '-' and logname != '' else None
        values['authuser'] = authuser if authuser != '-' and authuser != '' else None
        values['date'] = parser.parse(date, fuzzy=True)
        request_type, domain, section, trail, version = request_pattern.match(request).groups()
        values['request_type'] = request_type
        values['domain'] = domain if domain != '' else None
        values['section'] = section if section != '' else None
        values['trail'] = trail if trail != '' else None
        values['version'] = version
        values['status'] = status if status != '' else None
        values['bites'] = int(bites) if bites != '' else None
        return values
    else:
        # Nothing to see here
        return None
