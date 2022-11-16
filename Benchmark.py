import statistics
import time
from collections import defaultdict
from functools import wraps


class Benchmark:

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        self.__log_function_execution_statistics(self.tag, self.start, end)
        self.__add_function_execution_statistics(self.tag, self.start, end)

    def __init__(self):
        self.durations = defaultdict(list)
        self.tag = None

    def __call__(self, function=None, tag=None):
        # Have to account for this being used as both context manager and decorator
        # Plus double entry into this method when using @benchmark(tag = 'experiment')
        if not function:
            self.tag = tag
            return self

        if self.tag:
            tag = self.tag
            self.tag = None
        else:
            tag = function.__name__

        @wraps(function)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()
            self.__log_function_execution_statistics(tag, start, end)
            self.__add_function_execution_statistics(tag, start, end)
            return result

        return wrapper

    def summary(self):
        for tag, execution_times in self.durations.items():
            average = statistics.mean(execution_times)
            # Could use NumPy here but it would be a bit overkill in my opinion
            variance = sum((x - average) ** 2 for x in execution_times)
            print(f'For the tag {tag}, '
                  f'the average execution time was {average} and the variance was {variance}')

    def __log_function_execution_statistics(self, tag, start, end):
        duration = end - start
        print(f'Execution for tag {tag} took {duration} ms')

    def __add_function_execution_statistics(self, tag, start, end):
        duration = end - start
        self.durations[tag].append(duration)
