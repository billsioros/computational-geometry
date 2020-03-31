#############################################
# Homework 1
# Exercise 1
# Christina Andrinopoulou 1115201500006
# Vasileios Sioros 1115201500144
#############################################

from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np

# points at 2D
def plot_2D_points(points, polyg=False):
    fig, ax = plt.subplots()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0)) # set position of x spine to x=0
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))   # set position of y spine to y=0

    for point in points:
        plt.scatter(point[0], point[1], color="g")    
        plt.text(point[0]+0.2, point[1]+0.2, f'({point[0]},{point[1]})' , fontsize=11)

    if polyg == False:
        plt.show()


# draw triangle
def plot_triangle(points):
    plot_2D_points(points, polyg=True)

    triangle_points = np.array(points)
    triangle_plot = plt.Polygon(triangle_points, color='g')
    plt.gca().add_patch(triangle_plot)

    plt.show()


# calculate the area o a triangle
def calc_triangle_area(x0, y0, x1, y1, x2, y2):
    return abs((x0 * (y1 - y2) + x1 * (y2 - y0) + x2 * (y0 - y1))/2)


# check if point (0,0) is inside the triangle
def check_origin_in(x0, y0, x1, y1, x2, y2):
    # calculate triangle areas for:
    triangle_area1 = calc_triangle_area(x0, y0, x1, y1, 0, 0) # Point0, Point1, (0.0)
    triangle_area2 = calc_triangle_area(x0, y0, 0, 0, x2, y2) # Point0,(0.0), Point2
    triangle_area3 = calc_triangle_area(0, 0, x1, y1, x2, y2) # (0,0), Point1, Point2
    triangle_area = calc_triangle_area(x0, y0, x1, y1, x2, y2)

    if(triangle_area1 + triangle_area2 + triangle_area3 == triangle_area): 
        print('The interior of the triangle contains the origin (0, 0)')
    else: 
        print('The interior of the triangle does not contain the origin (0, 0)')


#check if 3 points form a triangle
def check_for_triangle(x0, y0, x1, y1, x2, y2):
    # area of triangle
    # if area is 0, the points are in the same straight line
    triangle_area = calc_triangle_area(x0, y0, x1, y1, x2, y2)
  
    if (triangle_area != 0): 
        return True
    else: 
        return False
  

if __name__ == "__main__":  

    # read 3 points from user
    print("Give 3 points.")
    points = list(tuple(map(int,input('Give a point: ').split())) for r in range(3)) 

    #check if these points form a triangle
    if check_for_triangle(points[0][0], points[0][1],
                        points[1][0], points[1][1],
                        points[2][0], points[2][1]):           
        print ('These points form a triangle')
        check_origin_in(points[0][0], points[0][1],
                        points[1][0], points[1][1],
                        points[2][0], points[2][1])
        plot_triangle(points)                
    else:
        print ('These points don\'t form a triangle')
        plot_2D_points(points)                    
