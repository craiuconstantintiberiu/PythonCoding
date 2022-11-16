import time
from Benchmark import Benchmark

def run_benchmark_decorator():
    benchmark = Benchmark()

    @benchmark(tag='my-function-experiment')
    def f():
        time.sleep(0.1)

    @benchmark()
    def g():
        time.sleep(0.1)

    fns_to_benchmark = [f, f, g, g]
    for fn in fns_to_benchmark:
        fn()

    benchmark.summary()


def run_benchmark_context_mngr():
    def f():
        time.sleep(1)

    def g():
        time.sleep(1)

    benchmark = Benchmark()

    fns_to_benchmark = [f, f, g, g]
    for fn in fns_to_benchmark:
        with benchmark(tag=f'{fn.__name__}'):
            fn()

    benchmark.summary()


if __name__ == '__main__':
    run_benchmark_decorator()
    run_benchmark_context_mngr()
