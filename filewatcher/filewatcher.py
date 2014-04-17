import time
import os

def watch(filename):
    """Generates lines from a file as the file is updated."""
    with open(filename) as f:
        # Move to the end of the file
        file_size = os.stat(filename)[6]
        f.seek(file_size)
        while True:
            last_location = f.tell()
            line = f.readline()
            if not line:
                time.sleep(1)
                f.seek(last_location)
            else:
                yield line
