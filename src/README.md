# My Algorithm/Solution

My algorithm came in 1st place with the least runtime among fellow interns/co-op students who attempted the problem. This solution finished in 10 seconds with the full dataset, with the second fastest having a runtime of 14 seconds.

## Approach

First and foremost, the provided log file could not be read in all at once. By doing this, we will exceed the memory limit of the VM that will run this solution on the full dataset.

Knowing that each line in the file represents a single request, and a request has a set format, allows us to parse each line by indexing the line to get the information we want. This is extremely useful as this allows us to do several things:
1. Skip requests with a missing PIN, avoiding unnecessary processing on these lines
2. Get the current minute and second from the timestamp of the request, which we can then convert to seconds since the hour started
3. Get the bytes transferred from a request

While iterating through each line in the file, we can keep track of the bytes transferred and save that in a list. By creating a list of 0s of length 3600, we can keep track of the bytes transferred for each second in an hour. We are also keeping track of when connections start as well as end by using 2 dictionaries, where the keys are the second that the connections are starting or ending, and the values are how many connections are starting or ending at that particular key.

By keeping track of the current and previous PIN, and given that the file is already sorted by PIN and then by timestamp, we can determine whether or not a request was made 120 seconds or more after the last request for the same PIN. There are 2 cases:
1. If it was made 120 seconds or more after the last request, then we can say that we start a connection at the current second, and that this connection will end
2. If it was made less than 120 seconds than the last request, then we can say that the previous connection will be extended. We can remove that the previous connection will end at its original time, and move it to the time when it will actually end as it has been refreshed

Furthermore, if the PIN was different from the previous PIN, we can then say a new connection has started (see case 1 in the above).

Writing the report to the file is pretty straightforward now. We can iterate through each second, keeping track of the current number of active connections and modify that value as we iterate. The index used for iteration represents the second in the hour, and the list keeping track of the bytes transferred can be accessed by index to determine the number of bytes transferred in that second. We also write the current value of current number of active connections. We modify this value as we iterate by accessing the 2 dictionaries storing the data of how many connections are starting or ending at any second. We can just add the number of connections starting at that particular second and subtract the number of connection ending at that particular second. Since we are using a default dictionary, if there are no connections starting and/or ending at that particular second, 0 will be added and/or subtracted, not changing the number of active connections.

## Algorithm complexity analysis

Time: O(n)

Space: O(1)

By iterating through all of the requests in the file, the runtime is dependent on how many lines there are in the file. Therefore, it runs in linear time.

The sizes of the list and the 2 dictionaries are fixed, and we are not reading in the entire file at once. Therefore, it runs in constant time.

## Ending comments

I do feel like this solution can still be improved further. By a lot, actually. There are probably some micro-optimizations that can be made to decrease the runtime even further.

There is some commented code that shows some of my previous approaches. There was a time when I wanted to use a binary heap to be used as a priority queue to get the next lowest second in the hour, but I eventually found that the better data structure was just a default dictionary.
