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

USAGE = (
    "Usage: python http_monitor.py -d database -l log"
)

# Monitor Loop
def monitor(stdscr, database):
    """
    Runs the monitor output loop.
    
    Should be run in curses.wrapper() to initialize curses settings and ensure
    proper exception handling.
    """
    dbconn, dbcursor = httpdb.connectdb(database)
    httpoutput.initialize(stdscr)
    end = time.time()
    start = time.time() - 10
    while True:
        time.sleep(start + 10 - end)
        start = time.time()
        # Run alert logic to get back aggregated values
        # Pull out functions: should read db and output dict of aggregated values
        hits = httpdb.get_total_traffic(dbcursor, 120)        
        # Update output 
        values = {'total_traffic': hits, 'seconds': 120}
        httpoutput.update(stdscr, values)
        # httpoutput.update(...)
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
