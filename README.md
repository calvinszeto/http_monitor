# HTTP Monitor

## Overview

HTTP Monitor is a console application that consumes updates to an access log and outputs statistics and alerts regarding the site traffic. Currently, the monitor supports W3C Common Log format as specified here: http://www.w3.org/Daemon/User/Config/Logging.html. The monitor runs on a console continuously, checking log updates at regular intervals and outputting summary statistics as well as alerts if traffic surpasses a given threshold.

## Running HTTP Monitor

Currently, the monitor is not packaged for installation. It can instead be run by cloning the source code and running the `run` script as follows:

```
git clone https://github.com/calvinszeto/http_monitor.git
cd http_monitor
pip install -r requirements.txt
./run [-l log_file] [-d database_file] [-i interval_time] [-t threshold_time threshold_amount]
```

As usual, it is recommended to use a virtualenv.

By default, the `run` script will read from a sample log in the `sample_logs` directory called `sample.log`. The `sample_logs` directory also contains a log generator for periodically updating a dummy access log. You can run this script as follows:

```
python sample_logs/log_generator.py sample_logs/sample.log
```

Running this in a separate console will allow you to test the monitor.

## Testing

There is a small test suite in the `test` directory. These can be run easily with:

```
py.test
```

Assuming you have py.test installed (included in requirements.txt).

## Improvements
