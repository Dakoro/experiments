import numpy as np
import timeit


def matmul(A, B):
    return np.dot(A, B)


def main():
    N = [128, 256, 1024]
    for n in N:
        x = np.random.randn(n, n).astype(np.float32)
        y = np.random.randn(n, n).astype(np.float32)
        print(timeit.timeit(lambda: matmul(x, y), number=10000, ))
if __name__ == '__main__':
    main()
    