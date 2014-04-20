import atexit
import curses
import itertools
import os
import sys
import sqlite3
import time

from filewatcher import filewatcher
from parser import parser
from httpdb import httpdb
from httpoutput import httpoutput
from stats import stats

USAGE = (
    "Usage: python http_monitor.py -d database -l log"
)
INTERVAL = 10 # seconds

# Monitor Loop
def monitor(stdscr, database):
    """
    Runs the monitor output loop.
    
    Should be run in curses.wrapper() to initialize curses settings and ensure
    proper exception handling.
    """
    # Set up database, stats, and output
    dbconn, dbcursor = httpdb.connectdb(database)
    calc = stats.Stats(dbconn, dbcursor)
    httpoutput.initialize(stdscr)
    # Set up loop for INTERVAL seconds
    end = time.time()
    start = time.time() - INTERVAL
    while True:
        time.sleep(start + INTERVAL - end)
        start = time.time()
        httpoutput.update(stdscr, calc)
        end = time.time()

if __name__ == "__main__":
    database = "default.db"
    log = "default.log"
    # TODO: Add error handling
    for index, arg in enumerate(sys.argv):
        if arg == "-d":
            database = sys.argv[index+1]
        elif arg == "-l":
            log = sys.argv[index+1]
    pid = os.fork()
    if pid == 0:
        dbconn, dbcursor = httpdb.connectdb(database)
        # Make sure to close the db connection
        atexit.register(dbconn.close)
        for line in filewatcher.watch(log):
            hit = parser.parse_w3log(line)
            if hit is not None:
                httpdb.add_hit(dbconn, dbcursor, hit)
    else:
        # Ensure that child process is killed
        atexit.register(os.kill, pid, 9)
        curses.wrapper(monitor, database)
