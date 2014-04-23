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

Naturally, as a console application, there are limitations on what this monitor can do in comparison to an application running on X or on the web. A graphical UI would allow better visualization, such as plotted or graphed traffic statistics. Interactivity to a more detailed degree would be possible, for example with a Google Analytics-style application.

Minor issues and improvements are documented in the Github Issues page. In addition, the monitor may be competing with other monitoring applications on a server - a possible improvement would be converting the monitor to a service which can continue to run in the background, while still creating alerts as necessary.

## Screenshots

![Monitor displays resolved alerts as well as new alerts in bold.](./static/multiple_alerts.jpeg?raw=true)
