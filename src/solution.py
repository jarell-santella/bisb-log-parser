"""A solution that attempts to solve the problem in O(n) time and O(n) space"""

from collections import defaultdict
from datetime import datetime
# import heapq
import os
from time import perf_counter_ns
# from typing import Tuple


# class HeapDictionary:


#     def __init__(self):
#         self.__heap = []
#         self.__dictionary = {}


#     def get(self, key: int) -> int:
#         return self.__dictionary[key]


#     def insert(self, key: int, value: int) -> None:
#         if not self.contains(key):
#             heapq.heappush(self.__heap, key)
#         self.__dictionary[key] = value


#     def pop(self) -> Tuple[int, int]:
#         key = heapq.heappop(self.__heap)
#         return key, self.__dictionary.pop(key)
    
    
#     def contains(self, key) -> bool:
#         return key in self.__dictionary


def solution():
    connections_started = defaultdict(int)
    connections_ended = defaultdict(int)

    # TODO: This will consume a lot of memory. Look into a better way of doing this
    bytes_transferred = [0] * 3600

    prev_pin = None
    prev_second = float("-infinity")

    with open("bisb.log", "r", encoding="UTF-8") as log_file:
        while line := log_file.readline():
            # If pin is missing, 25th character must be a comma. Skip this line
            if line[24] == ",":
                continue

            if prev_pin is None:
                hour = datetime.strptime(line[:8], "%H:%M:%S").hour

            curr_second = int(
                (
                    datetime.strptime(line[:8], "%H:%M:%S")
                    - datetime(1900, 1, 1, hour)
                ).total_seconds()
            )

            b_transferred = int(line[33:].split(",")[0])
            bytes_transferred[curr_second] += b_transferred if b_transferred > 0 else 0

            curr_pin = line[24:32]
            if curr_pin == prev_pin:
                # Case where we are still on the same pin
                if curr_second - prev_second >= 120:
                    connections_started[curr_second] += 1
                else:
                    connections_ended[prev_second + 120] -= 1
            else:
                # Case where we made it to the next unique pin
                connections_started[curr_second] += 1
                prev_pin = curr_pin

            connections_ended[prev_second + 120] += 1
            prev_second = curr_second

    active_connections = 0

    # Iterate through and produce output
    with open("src/output.txt", "a", encoding="UTF-8") as output_file:
        for i, total_bytes in enumerate(bytes_transferred):
            active_connections += connections_started[i] - connections_ended[i]
            output_file.write(f"{i + 1}: {active_connections}, {total_bytes}\n")

def main():
    # Delete output file if exists so output is produced from scratch and nothing is
    # appeneded
    if os.path.exists("src/output.txt"):
        os.remove("src/output.txt")

    with open("src/output.txt", "x", encoding="UTF-8") as _:
        pass

    start = perf_counter_ns()
    solution()
    end = perf_counter_ns()

    print(f"The script took {end - start} ns to finish.")


if __name__ == "__main__":
    main()
