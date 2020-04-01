from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np
import random
from exercise1 import check_for_triangle
from exercise1 import plot_2D_points


def remove_duplicates(lst):   
    return [item for item in (set(tuple(i) for i in lst))] 


# select a point from avaliable points (for ccw)
def select_random_point(current_hull_points, point1, point2):
    random_point = current_hull_points[0][0]
    if random_point == point1 or random_point == point2:
        random_points = [p[0] for p in current_hull_points if p[0] != point1 and p[0] != point2]
        random_point = random_points[0]
    return random_point


# makes thw final plot with all points and the convex hull
def plot_2D_hull(current_hull, all_points):
    points = []
    for line in current_hull:
        points.append(line[0])
        points.append(line[1])

    plot_2D_points(points+all_points, polyg=True)

    line_of_hull = []
    for k in current_hull:
        line_of_hull.append(k[0])
        line_of_hull.append(k[1])
        hull = np.array(line_of_hull)
        hull_plot = plt.Polygon(hull, fill=False)
        plt.gca().add_patch(hull_plot)
        del line_of_hull[:]
    plt.show()


# returns the sign of det
def ccw(A, B, C):
    return (B[0] - A[0]) * (C[1] - A[1]) > (B[1] - A[1]) * (C[0] - A[0])


def check_ccw(p, previous_point, end_point, random_point):
    if ccw(previous_point, end_point, random_point):
        if not ccw(previous_point, end_point, p):
            return True
        else:
            return False
    else:
        if ccw(previous_point, end_point, p):
            return True
        else:
            return False


def beneath_beyond(points):
    # Step 1: sort points in descending
    sorted_points = sorted(points, key=lambda x: (x[0], x[1]), reverse=True)

    # Step 2: initial hull = triangle
    current_hull_points = []
    current_hull = []
    # if first 3 points are collinear, select (x,min(y)) and (x,max(y))
    if not check_for_triangle(sorted_points[0][0], sorted_points[0][1],
                          sorted_points[1][0], sorted_points[1][1],
                          sorted_points[2][0], sorted_points[2][1]):
        for p in sorted_points[1:]:
            if p[0] == sorted_points[0][0]:
                last = p
                sorted_points.remove(p)
        sorted_points.append(last)
        sorted_points = sorted(sorted_points, key=lambda x: x[0], reverse=True)

    for p in sorted_points[0:2]:
        current_hull_points.append([p, 'blue'])
    current_hull_points.append([sorted_points[2], 'red'])
        
    current_hull.append([sorted_points[0], sorted_points[1], 'blue'])
    current_hull.append([sorted_points[0], sorted_points[2], 'blue'])
    current_hull.append([sorted_points[1], sorted_points[2], 'blue'])
        
    del sorted_points[0:3]
    previous_point = current_hull_points[-1][0]

    # Step 3: 
    color = []   
    purple_points = []
    for p in sorted_points:
        # Step 3B: find all red lines
        # check every blue line in hull, if it's red now
        for line in current_hull:
            if line[2] == 'blue':
                random_point = select_random_point(current_hull_points, line[0], line[1])
                if check_ccw(p, line[0], line[1], random_point):
                    line[2] = 'red'
                else:
                    line[2] = 'blue'      

        # Step 3B: find two purple points
        # re-coloring points
        for point1 in current_hull_points:
            del color[:]
            for point2 in current_hull:
                if point2[0] == point1[0] or point2[1] == point1[0]:
                    color.append(point2[2]) 
            if len(color) > 0:
                if color[0] != 'purple' and color[1] != 'purple':
                    if color[0] != color[1]: # red + blue = purple
                        point1[1] = 'purple'               
        
        del purple_points[:]
        for point in current_hull_points:
            if point[1] == 'purple':
                purple_points.append(point[0])

        # Step 3C: remove all red lines
        for line in current_hull:
            if line[2] == 'red':
                line[2] = 'delete_line'
        current_hull = [elem for elem in current_hull if elem[2] != 'delete_line']

        # Step 3C: put two lines from p to purple1 and purple2 point
        current_hull.append([p, purple_points[0], 'blue'])  
        current_hull.append([p, purple_points[1], 'blue'])  

        # initialize for next step
        current_hull_points.append([p,'red'])
        for point in current_hull_points:
            if point[1] == 'purple':
                point[1] = 'blue'
    plot_2D_hull(current_hull, points)




if __name__ == "__main__":
    # read points from user(input choice 1)
    # number_of_points = input('Give the number of points: ')
    # if int(number_of_points) < 3:
    #     print('Error: Program needs 3 points at least.')
    #     exit()
    # points = list(tuple(map(int,input("Give a point: ").split())) for r in range(int(number_of_points)))
    
    # random poinsts(input choice 2)
    for i in range(10):
        points = [(random.randrange(-100, 100), random.randrange(-100, 100)) for i in range(20)]
        points = remove_duplicates(points)

    # call beneath_beyond algorithm
        beneath_beyond(points)
