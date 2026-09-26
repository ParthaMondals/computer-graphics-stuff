import matplotlib.pyplot as plt

x_points = []
y_points = []

## Function to generate x and y co-ordinates for a line

def linebresenham(x0,y0,xend,yend):
    dx = abs(xend - x0)
    dy = abs(yend - y0)

    x = x0
    y = y0
    if(dy < dx):
        p = (2*dy - dx)
        for i in range(1,dx+1):
            if (p < 0):
                p = p + (2 * dy)
            else:
                p = p + (2 * dy - 2 * dx)
                y = y +1
            x = x + 1
            x_points.append(x)
            y_points.append(y)
    else:
        p = (2*dx - dy)
        for i in range(1,dy+1):
            if (p < 0):
                p = p + (2 * dx)
            else:
                p = p + (2 * dx - 2 * dy)
                x = x +1
            y = y + 1 
            x_points.append(x)
            y_points.append(y)


x_init = int(input("Enter initial x corodinate: "))
y_init = int(input("Enter initial y corodinate: "))
x_final = int(input("Enter final x corodinate: "))
y_final = int(input("Enter final y corodinate: "))

linebresenham(x_init , y_init , x_final , y_final)

## Plotting the line

plt.plot(x_points,y_points)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid(True)
plt.show()
