# BISB Log Parser

This was a real world problem that the BlackBerry team once faced and is now given as a DSA and coding challenge to interns/co-op students. My solution came in 1st place with the fastest time of any of the other submitted algorithms with a runtime of 10 seconds on the full datset.

## Challenge

This was an actual problem posed to the BlackBerry team a number of years ago. In this GitHub repository, there is a sample log file `bisb.log` that can be found [here](https://github.com/jarell-santella/bisb-log-parser/blob/main/bisb.log).

It contains some browsing traffic over the course of a given hour, in csv format with the following columns:
- `timestamp`
- `request_id`
- `pin`
- `bytes_transferred`
- `url`

Write a script in Python3 that parses the log file and generates a text report containing the second of the hour, number of active connections in that second, and the number of bytes transferred in that second. Each line of the report should be in the format:
```
second: active_connections, bytes_transferred
```

Bytes transferred should be self-explanatory.

Active connections is a bit more complicated. When a device (represented uniquely by its `pin`) makes a request, it opens a new connection into BlackBerry's data center. It will reuse that connection for the next request, regardless of the requested URL, as long as the request is made within the next 2 minutes. This will reset the 2 minute timeout. If more than 2 minutes pass between request, the device will close the connection at 2 minutes.  The connection is considered active for the duration that it is open. And to clarify, if a connection is opened in second 1, it will still be open in second 120, but closed in 121.

The sample input log file is ~10 MB in size. The actual one your algorithm will be tested against is ~3 GB in size.

Constraints:
- The `timestamp` is expressed in `HH:MM:SS` format
- The `request_id` is always 14 characters
- A pin uniquely identifies a mobile device. The `pin` is normally an 8 character hex number, however, sometimes, the logging system couldn’t collect the device pin, in which case, this field is empty. Lines missing a `pin` should be skipped
- `bytes_transferred` is specified in decimal and can vary in size.  Sometimes a connection was made, but no data was transferred due to a request error. In this case, the `bytes_transferred` field is set to `-1`. When this happens, a connection was still made
- The url can vary in size
- The log file is sorted by `pin` and then by `timestamp`
- Your algorithm must use <8 GB memory at all times, as that is the RAM installed on the VM that the algorithm will be tested on
