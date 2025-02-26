from time import perf_counter_ns
def SingleScalar(Count, Input):
    Sum = 0
    for Index in range(0, Count, 2):
        Sum += Input[Index]
        Sum += Input[Index + 1]
    return Sum


def main():
    CPU_FREQ = 5.0
    COUNT = 4096
    numbers = [n for n in range(COUNT)]
    runtimes = []
    for n in range(100_000):
        start = perf_counter_ns()
        SingleScalar(COUNT, numbers)
        end = perf_counter_ns()
        runtime = end - start
        runtimes.append(runtime)
    best_runtime = min(runtimes)
    ncycles = best_runtime * CPU_FREQ
    ncycleadd = ncycles / COUNT
    naddcycle = 1 / ncycleadd
    
    print(best_runtime)
    print(ncycles)
    print(ncycleadd)
    print(naddcycle)

if __name__ == '__main__':
    main()