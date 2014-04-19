import sys
import time
import random
from datetime import datetime

USAGE = "Usage: python log_generator.py log_filename"
# List of possible domain, section pairs
SECTIONS = [
    ("http://www.example.com","section1"),
    ("http://www.example.com","section2"),
    ("http://www.example.com","section3"),
    ("http://www.example.com","section4"),
    ("http://www.sample.com","section1"),
    ("http://www.sample.com","section2"),
    ("http://www.sample.com","section3"),
    ("http://www.sample.com","section4")
]
TRAILS = [
    "/test.html",
    "/test.txt",
    "/test.pdf",
    "/1/test.md"
]

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print USAGE
        sys.exit(0)
    with open(sys.argv[1], 'a') as log:
        while True:
            # Wait a random amount of time      
            sleep = random.randint(0,5)
            print "Waiting {sleep} seconds.".format(sleep=sleep)
            time.sleep(sleep)
            # Write a random number of log lines
            lines = random.randint(0,10)
            print "Writing {lines} lines.".format(lines=lines)
            for idx in range(lines):
                values = {}
                values["host"] = "192.169.{first}.{second}".format(first = random.randint(0,50), 
                                                                    second = random.randint(0,20))
                values["logname"] = "testuser"
                values["authuser"] = "testuser"
                values["date"] = datetime.now()
                domain, section = SECTIONS[random.randint(0,len(SECTIONS)-1)]
                trail = TRAILS[random.randint(0,len(TRAILS)-1)]
                values["request"] = "GET {domain}/{section}{trail} HTTP/1.1".format(domain = domain,
                    section = section, trail = trail)
                values["status"] = 200
                values["bites"] = random.randint(0, 8192)
                # 192.168.1.3 - - [18/Feb/2000:13:33:37 -0600] "GET / HTTP/1.0" 200 5073
                line = '{host} {logname} {authuser} [{date}] "{request}" {status} {bites}\n'.format(**values)
                log.write(line)
            log.flush()
