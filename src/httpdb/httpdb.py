HIT_ATTR = [
    "host",
    "logname",
    "authuser",
    "date",
    "request_type",
    "domain",
    "section",
    "trail",
    "version",
    "status",
    "bites"
]

def connectdb(database):
    """Connect to database, create a Hit table if it doesn't exist, and return the cursor."""
    dbconn = sqlite3.connect(database)
    dbcursor = dbconn.cursor()
    dbcurser.execute("CREATE TABLE IF NOT EXISTS Hit (host text, logname text, authuser text, date integer, request_type text, domain text, section text, trail text, version text, status text, bites integer)")

def add_hit(dbcursor, hit):
    """Adds a hit to the database."""
    dbcursor.execute("INSERT INTO Hit VALUES (?,?,?,?,?,?,?,?,?,?,?)",[hit[attr] for attr in HIT_ATTR])
