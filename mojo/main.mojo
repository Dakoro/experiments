from math import iota
def main():
    var robots = 12
    var x_grid_size = 5
    var y_grid_size = 7
    
    #(x,y) positions for n robots: 🅧1️⃣,🆈1️⃣,🅧2️⃣,🆈2️⃣,..
    var robot_pos = SIMD[DType.int8, 128](
        0,0, 3,1, 1,4, 2,6, 0,0, 1,4, 
        1,4, 4,0, 3,3, 3,6, 1,1, 6,6 
    )
    #(➕x,➕y) speeds for n robots
    var robot_speeds = SIMD[DType.int8, 128](
        1,-2, -2,-5, -1,3, 1,-3, 2,4, -3,-1,
        3,-5, -4,-1, 3,3, -1,2, 1,-4, -4,-1
    )
    wrap_values = SIMD[DType.int8, 128]() #wrap values for 🅧 🆈
    for i in range(128):
        if i%2==0: 
            wrap_values[i]=x_grid_size   # 🅧
        else: 
            wrap_values[i]=y_grid_size   # 🆈
    
    # 🤖 the robots moves for 100 seconds
    for i in range(100):
        robot_pos+=robot_speeds
        robot_pos%=wrap_values # 🔁 wrap 🅧 and 🆈
    
    all_indexes = iota[DType.int8, 128](0)
    all_indexes_remainder = all_indexes%2 # 0️⃣ == x, 1️⃣ == y
    all_robots = (all_indexes<robots*2).select(robot_pos,-1)
    all_robots_x = (all_indexes_remainder==0).select(all_robots, -1)
    all_robots_y = (all_indexes_remainder==1).select(all_robots, -1).rotate_left[1]()

    quadrants = SIMD[DType.int8, 4](0) # 🔠
    x_grid_separator = (x_grid_size//2)# 💠 +1 not needed (index starts at 0)
    y_grid_separator = (y_grid_size//2)# so 3//2 == 1, index of the center!
    for y in range(y_grid_size):
        for x in range(x_grid_size):
            robots_on_x_y = (
                (all_robots_x == x)&(all_robots_y==y)
            ).cast[DType.int8]().reduce_add()
            if x == x_grid_separator or y == y_grid_separator: #💠
                robots_on_x_y = 0
            quadrants[(y>y_grid_separator)*2+(x>x_grid_separator)]+=robots_on_x_y
            print(robots_on_x_y, end="\t")
        print()
    print(quadrants, quadrants.reduce_mul())