"""Contains the watch function for tracking log files."""

import time
import os

def watch(filename):
    """Generates lines from a file as the file is updated."""
    with open(filename) as log:
        # Move to the end of the file
        file_size = os.stat(filename)[6]
        log.seek(file_size)
        while True:
            last_location = log.tell()
            line = log.readline()
            if not line:
                time.sleep(0.1)
                log.seek(last_location)
            else:
                yield line
