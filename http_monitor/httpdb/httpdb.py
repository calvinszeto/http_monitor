"""Contains functions for accessing and modifying the database."""

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
    """Connect to database, create a Hit table, and return the cursor."""
    dbconn = sqlite3.connect(database)
    dbcursor = dbconn.cursor()
    create_string = (
        "CREATE TABLE IF NOT EXISTS Hit "
        "(host text, logname text, authuser text, date integer, "
        "request_type text, domain text, section text, trail text, "
        "version text, status text, bites integer)")
    dbcursor.execute(create_string)
    return dbconn, dbcursor

def add_hit(dbconn, dbcursor, hit):
    """Adds a hit to the database."""
    dbcursor.execute("INSERT INTO Hit VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        , [hit[attr] for attr in HIT_ATTR])
    dbconn.commit()
    return dbcursor

def get_hits_by_section(dbcursor):
    """Returns a list of (domain, section, number of hits) tuples."""
    query_string = (
        "SELECT domain, section, COUNT(*) "
        "FROM Hit "
        "GROUP BY domain, section"
    )
    return dbcursor.execute(query_string).fetchall()

def get_total_traffic(dbcursor, seconds):
    """Returns a count of the total traffic within the last given seconds."""
    oldest = int(time.time() - seconds)
    newest = int(time.time())
    query_string = (
        "SELECT count(*) "
        "FROM Hit "
        "WHERE date BETWEEN ? AND ?"
    )
    # Query is returned as [(hits,)]
    return dbcursor.execute(query_string, [oldest, newest]).fetchall()[0][0]

def get_all_traffic(dbcursor):
    """Returns the total number of recorded hits."""
    query_string = (
        "SELECT count(*) "
        "FROM Hit "
    )
    return dbcursor.execute(query_string).fetchall()[0][0]

def get_time_period(dbcursor):
    """Returns the dates of the earliest and latest recorded hits."""
    query_oldest = (
        "SELECT MIN(date)"
        "FROM Hit"
    )
    query_newest = (
        "SELECT MAX(date)"
        "FROM Hit"
    )
    oldest = dbcursor.execute(query_oldest).fetchall()[0][0]
    newest = dbcursor.execute(query_newest).fetchall()[0][0]
    return oldest, newest

def get_total_bites(dbcursor):
    """Returns the total number of bytes transferred."""
    query_string = (
        "SELECT SUM(bites)"
        "FROM Hit"
    )
    return dbcursor.execute(query_string).fetchall()[0][0]

def get_max_traffic(dbcursor, interval):
    """Returns the maximum traffic experienced in a given time interval."""
    query_string = (
        "SELECT ( "
        "   SELECT COUNT(*) "
        "   FROM Hit hi "
        "   WHERE hi.date BETWEEN h.date - ? AND h.date + ? "
        "   ) AS maxvalue "
        "FROM Hit h "
        "ORDER BY maxvalue DESC "
        "LIMIT 1"
    )
    return dbcursor.execute(query_string, [interval/2]*2).fetchall()[0][0]
