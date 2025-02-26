#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <limits.h>
#include <x86intrin.h>
#include <emmintrin.h>
#include <smmintrin.h>

#define CPU_FREQ 5.0
#define COUNT 4096
#define ITERATIONS 100000

// Function to calculate the sum of elements in an array
typedef unsigned int u32;
u32 SingleScalar(u32 Count, u32 *Input)
{
	u32 SumA = 0;
	for(u32 Index = 0; Index < Count; Index++)
	{
		SumA += Input[Index];
	}
	
	return SumA;
}

typedef unsigned int u32;
u32 __attribute__((target("ssse3"))) SingleSSE(u32 Count, u32 *Input)
{
    __m128i Sum = _mm_setzero_si128();
    for(u32 Index = 0; Index < Count; Index += 4)
    {
        Sum = _mm_add_epi32(Sum, _mm_load_si128((__m128i *)&Input[Index]));
    }

    Sum = _mm_hadd_epi32(Sum, Sum);
    Sum = _mm_hadd_epi32(Sum, Sum);
    
    return _mm_cvtsi128_si32(Sum);
}

typedef unsigned int u32;
u32 __attribute__((target("avx2"))) SingleAVX(u32 Count, u32 *Input)
{
	__m256i Sum = _mm256_setzero_si256();
	for(u32 Index = 0; Index < Count; Index += 8)
	{
		Sum = _mm256_add_epi32(Sum, _mm256_loadu_si256((__m256i *)&Input[Index]));
	}

	Sum = _mm256_hadd_epi32(Sum, Sum);
	Sum = _mm256_hadd_epi32(Sum, Sum);
	__m256i SumS = _mm256_permute2x128_si256(Sum, Sum, 1 | (1 << 4));
	Sum = _mm256_add_epi32(Sum, SumS);
	
	return _mm256_cvtsi256_si32(Sum);
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