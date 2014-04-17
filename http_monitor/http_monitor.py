import sys
import sqlite3

USAGE = (
    "Usage: python http_monitor.py -d database -l log"
)

# Separate DB functionality into functions here
# Initialize Database Connection
# Initialize table if it doesn't exist

if __name__ == "__main__":
    for index, arg in enumerate(sys.argv):
        if arg == "-d":
            pass
        elif arg == "-l":
            pass
    # Set up db, watcher, output
    # In child process:
        # For each line from watching log file
        # Save to database
        # Ensure that child process is killed if anything goes wrong
    # Every 10s:
        # Run alert logic to get back values
        # Update output 
