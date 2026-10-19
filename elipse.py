import matplotlib.pyplot as plt

# Separate lists so the two regions can be drawn in different colours
region1_x, region1_y = [], []
region2_x, region2_y = [], []
center = []


def visualize(rx,ry):
    plt.figure(figsize=(7, 6))
    
    plt.plot(region1_x, region1_y, linestyle="none", marker="o",
             color="blue", markersize=3,label="Region 1")
    plt.plot(region2_x, region2_y, linestyle="none", marker="o",
             color="green", markersize=3 , label="Region 2")

    ## Mark the center
    plt.plot(xc, yc, marker="o", color="red", markersize=10,label="Center")

    ## Mark the X and Y axis along the origin
    plt.axhline(0, color="black", linewidth=2)
    plt.axvline(0, color="black", linewidth=2)

    plt.title(f"Midpoint Ellipse Algorithm (rx = {rx}, ry = {ry})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()


def set_pixel(x, y, xlist, ylist):
    xlist.extend([center[0] + x, center[0] - x, center[0] + x, center[0] - x])
    ylist.extend([center[1] + y, center[1] + y, center[1] - y, center[1] - y])


def midpoint_ellipse(rx, ry):
    rx2 = rx * rx
    ry2 = ry * ry

    # For Region 1 (slope < -1)
    x = 0
    y = ry
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    while (2 * ry2 * x) < (2 * rx2 * y):
        set_pixel(x, y, region1_x, region1_y)
        x += 1
        if p1 < 0:
            p1 = p1 + (2 * ry2 * x) + ry2
        else:
            y -= 1
            p1 = p1 + (2 * ry2 * x) - (2 * rx2 * y) + ry2

    # For Region 1 (slope > -1)
    p2 = (ry2 * (x + 0.5) ** 2) + (rx2 * (y - 1) ** 2) - (rx2 * ry2)

    while y >= 0:
        set_pixel(x, y, region2_x, region2_y)
        y -= 1
        if p2 > 0:
            p2 = p2 + rx2 - (2 * rx2 * y)
        else:
            x += 1
            p2 = p2 + (2 * ry2 * x) - (2 * rx2 * y) + rx2



xc = int(input("Enter centre x (xc): "))
center.append(xc)
yc = int(input("Enter centre y (yc): "))
center.append(yc)
rx = int(input("Enter x-radius (rx): "))
ry = int(input("Enter y-radius (ry): "))

midpoint_ellipse(rx, ry)
visualize(rx,ry)


