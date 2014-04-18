import sys
import sqlite3
import curses
import atexit
import os

from filewatcher import filewatcher
from parser import parser

USAGE = (
    "Usage: python http_monitor.py -d database -l log"
)

# Separate DB functionality into functions here
def connectdb(database):
    """Connect to database, create a Hit table if it doesn't exist, and return the cursor."""
    dbconn = sqlite3.connect(database)
    dbcursor = dbconn.cursor()
    dbcurser.execute("create table if not exists Hit (host text, logname text, authuser text, date integer, request_type text, domain text, section text, trail text, version text, status text, bites integer)")

def add_hit(dbcursor, hit):
    """Adds a hit to the database."""
    dbcursor.execute()

# Separate curses functionality
def initialize_out(stdscr):
    curses.curs_set(0)
    stdscr.border()
    max_y, max_x = stdscr.getmaxyx()
    stdscr.hline(max_y/3, 1, '_', max_x-2)
    stdscr.vline(1, max_x/4, '_', max_x-2)
    stdscr.refresh()

# Monitor Loop
def monitor(stdscr):
    while True:
        # Every 10s:
            # Run alert logic to get back values
            # Update output 
        pass

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
        dbcursor = connectdb(database)
        for line in filewatcher.watch(log):
            hit = parser.parse_w3log(line)
            if hit is not None:
                add_hit(hit)
    else:
        # Ensure that child process is killed
        atexit.register(os.kill, pid, 9)
        curses.wrapper(monitor) # TODO: Add other arguments
