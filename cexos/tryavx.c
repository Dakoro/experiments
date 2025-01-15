#include <immintrin.h>
#include <stdio.h>

int main() {
    __m256 v1 = _mm256_set_ps(1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f);
    __m256 v2 = _mm256_set_ps(9.0f, 10.0f, 11.0f, 12.0f, 13.0f, 14.0f, 15.0f, 16.0f);

    __m256 result = _mm256_add_ps(v1, v2);

    // Store the result
    float* arr = (float*)aligned_alloc(sizeof(float) * 8, 32);
    _mm256_storeu_ps(arr, result);

    // Print the result
    for (int i = 0; i < 8; i++) {
        printf("%f ", arr[i]);
    }
    printf("\n");

    return 0;
}