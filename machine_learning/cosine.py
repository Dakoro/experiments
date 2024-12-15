import math
import numpy as np
import timeit

def cosine_distance(a, b):
    dot_product = sum(ai * bi for ai, bi in zip(a, b))
    magnitude_a = math.sqrt(sum(ai * ai for ai in a))
    magnitude_b = math.sqrt(sum(bi * bi for bi in b))
    cosine_similarity = dot_product / (magnitude_a * magnitude_b)
    return 1 - cosine_similarity

def cosine_distance_v2(a, b):
    dot_product = 0
    magnitude_a = 0
    magnitude_b = 0
    for ai, bi in zip(a, b):
        dot_product += ai * bi
        magnitude_a += ai * ai
        magnitude_b += bi * bi
    cosine_similarity = dot_product / (math.sqrt(magnitude_a )* math.sqrt(magnitude_b))
    return 1 - cosine_similarity


if __name__ == '__main__':
    np.random.seed(0)
    a_list = np.random.rand(1536).tolist()
    b_list = np.random.rand(1536).tolist()
    result = timeit.timeit(lambda: cosine_distance(a_list, b_list), number=100)
    result2 = timeit.timeit(lambda: cosine_distance_v2(a_list, b_list), number=100)
    print(result, result2)