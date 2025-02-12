#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <limits.h>

#define CPU_FREQ 5.0
#define COUNT 4096
#define ITERATIONS 100000

// Function to calculate the sum of elements in an array
typedef unsigned int u32;
u32 SingleScalar(u32 Count, u32 *Input)
{
	u32 SumA = 0;
    u32 SumB = 0;
	u32 SumC = 0;
	u32 SumD = 0;
	for(u32 Index = 0; Index < Count; Index += 4)
	{
		SumA += Input[Index];
        SumB += Input[Index + 1];
        SumC += Input[Index + 2];
		SumD += Input[Index + 3];
	}
	
	return SumA + SumB + SumC + SumD;
}

int main() {
    u32* numbers = (u32*)malloc(COUNT * sizeof(u32));
    long long* runtimes = (long long*)malloc(ITERATIONS * sizeof(long long));

    // Initialize the array with values from 0 to COUNT-1
    for (int i = 0; i < COUNT; i++) {
        numbers[i] = i;
    }

    // Measure the runtime of SingleScalar ITERATIONS times
    for (int n = 0; n < ITERATIONS; n++) {
        struct timespec start, end;
        clock_gettime(CLOCK_MONOTONIC, &start); // Start timing
        SingleScalar(COUNT, numbers);
        clock_gettime(CLOCK_MONOTONIC, &end); // End timing

        // Calculate runtime in nanoseconds
        long long runtime = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);
        runtimes[n] = runtime;
    }

    // Find the best runtime (minimum value in runtimes array)
    long long best_runtime = LLONG_MAX;
    for (int i = 0; i < ITERATIONS; ++i) {
        if (runtimes[i] < best_runtime) {
            best_runtime = runtimes[i];
        }
    }

    // Calculate derived metrics
    double ncycles = best_runtime * CPU_FREQ;
    double ncycleadd = ncycles / COUNT;
    double naddcycle = 1 / ncycleadd;

    // Print results
    printf("Best runtime: %lld ns\n", best_runtime);
    printf("ncycles: %.2f\n", ncycles);
    printf("ncycleadd: %.2f\n", ncycleadd);
    printf("naddcycle: %.5f\n", naddcycle);

    // Free allocated memory
    free(numbers);
    free(runtimes);

    return 0;
}