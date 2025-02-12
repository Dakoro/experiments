from time import perf_counter_ns
from python import Python
from python import PythonObject


fn SingleScalar(Count: Int, Input: List[Int]) -> Int:
    var SumA: Int = 0
    var SumB: Int = 0
    var SumC: Int = 0
    var SumD: Int = 0
    for Index in range(0, Count, 4):
        SumA += Input[Index]
        SumB += Input[Index + 1]
        SumC += Input[Index + 2];
        SumD += Input[Index + 3];
    return SumA + SumB + SumC + SumD

fn main()raises:
    var np = Python.import_module("numpy")
    var perf = Python.import_module("time")
    var CPU_FREQ: Float64 = 5.0
    var COUNT: Int = 4096
    var runtimes: PythonObject = Python.list()
    var numbers: List[Int] = List[Int]()
    for n in range(COUNT):
        numbers.append(n)

    for n in range(100_000):
        var start: PythonObject  = perf.perf_counter_ns()
        var result = SingleScalar(COUNT, numbers)
        var end: PythonObject = perf.perf_counter_ns()
        var runtime: PythonObject = end - start
        runtimes.append(runtime)
    
    var best_runtime: Int = np.min(runtimes)
    var ncycles: Float64 = best_runtime * CPU_FREQ
    var ncycleadd: Float64 = ncycles / COUNT
    var naddcycle: Float64 = 1 / ncycleadd
    
    print(best_runtime)
    print(ncycles)
    print(ncycleadd)
    print(naddcycle)