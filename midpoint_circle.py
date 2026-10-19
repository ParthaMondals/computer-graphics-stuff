import matplotlib.pyplot as plt

center = []
points_x = []
points_y = []

def visualize(r): ## A method to visualize the circle
    plt.figure(figsize=(6, 6))
    plt.plot(points_x, points_y, linestyle='none', marker='o', color='black', markersize=3)
    plt.axhline(0, color="black", linewidth=2)
    plt.axvline(0, color="black", linewidth=2)
    plt.title(f"Midpoint Circle Algorithm (r = {r})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


def set_pixel(x, y): ## A method to set the pixels points
    points_x.append(x + center[0])
    points_y.append(y + center[1])


def midpoint_circle(r): ## Method that determines the x and y coordinates
    x = 0
    y = r
    p = 1 - r

    while x <= y:
        set_pixel(x, y)
        set_pixel(y, x)
        set_pixel(-x, y)
        set_pixel(-y, x)
        set_pixel(-x, -y)
        set_pixel(-y, -x)
        set_pixel(x, -y)
        set_pixel(y, -x)

        x += 1
        if p > 0:
            y -= 1
            p = p + (2 * x) - (2 * y) + 1
        else:
            p = p + (2 * x) + 1



r = int(input("Enter radius: "))

xc = int(input("Enter x coordinate of center: "))
yc = int(input("Enter y coordinate of center: "))
center.append(xc)
center.append(yc)

midpoint_circle(r)
visualize(r)





