import sqlite3
import time

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
    dbcursor.execute("CREATE TABLE IF NOT EXISTS Hit (host text, logname text, authuser text, date integer, request_type text, domain text, section text, trail text, version text, status text, bites integer)")
    return dbconn, dbcursor

def add_hit(dbconn, dbcursor, hit):
    """Adds a hit to the database."""
    dbcursor.execute("INSERT INTO Hit VALUES (?,?,?,?,?,?,?,?,?,?,?)",[hit[attr] for attr in HIT_ATTR])
    dbconn.commit()
    return dbcursor

def get_hits_by_section(dbcursor):
    """Returns a list of (domain, section, number of hits) tuples."""
    return dbcursor.execute("SELECT domain, section, COUNT(*) FROM Hit GROUP BY domain, section").fetchall()

def get_total_traffic(dbcursor, seconds):
    """Returns a count of the total traffic within the last given seconds."""
    oldest = int(time.time() - seconds)
    newest = int(time.time())
    # with open("test.log", 'a') as test:
    #     test.write("Checking between : " + str(oldest) + " and " + str(newest))
    return dbcursor.execute("SELECT count(*) FROM Hit WHERE date BETWEEN ? AND ?", [oldest, newest]).fetchall()[0][0] # Query is returned as [(hits,)]
