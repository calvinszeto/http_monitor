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
def monitor(stdscr):
    """
    Runs the monitor output loop.
    
    Should be run in curses.wrapper() to initialize curses settings and ensure
    proper exception handling.
    """
    start = time.time()
    end = time.time() + 10
    while True:
        time.sleep(start + 10 - end)
        start = time.time()
        # Run alert logic to get back values
        # Update output 
        end = time.time()

if __name__ == "__main__":
    database = "default.db"
    log = "default.log"
    for index, arg in enumerate(sys.argv):
        if arg == "-d":
            pass
        elif arg == "-l":
            pass
    pid = os.fork()
    if pid == 0:
        dbcursor = httpdb.connectdb(database)
        for line in filewatcher.watch(log):
            hit = parser.parse_w3log(line)
            if hit is not None:
                httpdb.add_hit(hit)
    else:
        # Ensure that child process is killed
        atexit.register(os.kill, pid, 9)
        curses.wrapper(monitor) # TODO: Add other arguments
