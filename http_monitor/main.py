import atexit
import curses
import itertools
import os
import sys
import sqlite3
import time

from http_monitor.filewatcher import filewatcher
from http_monitor.parser import parser
from http_monitor.httpdb import httpdb
from http_monitor.httpoutput import httpoutput
from http_monitor.stats import stats

def monitor(stdscr, database, interval, threshold_time, threshold_amount):
    """
    Runs the monitor output loop.
    
    Should be run in curses.wrapper() to initialize curses settings and ensure
    proper exception handling.
    """
    # Set up database, stats, and output
    dbconn, dbcursor = httpdb.connectdb(database)
    calc = stats.Stats(dbconn, dbcursor, threshold_time, threshold_amount)
    output = httpoutput.Output(stdscr, calc)
    # Set up loop for INTERVAL seconds
    end = time.time()
    start = time.time() - interval 
    while True:
        time.sleep(start + interval - end)
        start = time.time()
        output.update()
        end = time.time()

def main(log, database = "default.db", interval = 10, 
        threshold_time = 120, threshold_amount = 20):
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
        curses.wrapper(monitor, database, interval, threshold_time, threshold_amount)
