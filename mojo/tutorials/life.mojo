from gridv1 import Grid

def main():
    num_rows = 8
    num_cols = 8
    glider = List(
        List(0, 1, 0, 0, 0, 0, 0, 0),
        List(0, 0, 1, 0, 0, 0, 0, 0),
        List(1, 1, 1, 0, 0, 0, 0, 0),
        List(0, 0, 0, 0, 0, 0, 0, 0),
        List(0, 0, 0, 0, 0, 0, 0, 0),
        List(0, 0, 0, 0, 0, 0, 0, 0),
        List(0, 0, 0, 0, 0, 0, 0, 0),
        List(0, 0, 0, 0, 0, 0, 0, 0),
    )

    start = Grid(8, 8, glider)
    print(String(start))