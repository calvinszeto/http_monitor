import atexit
import curses
import itertools
import os
import sys
import sqlite3
import time

# Why don't these imports work?
import http_monitor
from http_monitor.filewatcher import filewatcher
from http_monitor.parser import parser
from http_monitor.httpdb import httpdb
from http_monitor.httpoutput import httpoutput
from http_monitor.stats import stats

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
    calc = stats.Stats(dbconn, dbcursor, 120, 20)
    httpoutput.initialize(stdscr)
    # Set up loop for INTERVAL seconds
    end = time.time()
    start = time.time() - INTERVAL
    while True:
        time.sleep(start + INTERVAL - end)
        start = time.time()
        httpoutput.update(stdscr, calc)
        end = time.time()

def main(database, log):
    database = database or "default.db"
    log = log or "default.log"
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
