import matplotlib.pyplot as plt

# Define the fixed boundaries of the clipping window.
X_MIN = 50
X_MAX = 200
Y_MIN = 50
Y_MAX = 150
print(f"The Clipping window: from ({X_MIN},{Y_MIN}) to ({X_MAX},{Y_MAX})\n")

BOUNDARIES = ["Left", "Right", "Bottom", "Top"]

def is_inside(x, y, boundary):
    if boundary == "Left":
        return x >= X_MIN
    elif boundary == "Right":
        return x <= X_MAX
    elif boundary == "Bottom":
        return y >= Y_MIN
    elif boundary == "Top":
        return y <= Y_MAX

def get_polygon_vertices():
    try:
        n = int(input("Enter the number of vertices of the polygon: "))
        if n < 3:
            raise ValueError("A polygon must have at least 3 vertices.")
    except ValueError as e:
        print(e)
        return get_polygon_vertices()  # Prompt the user again for valid input
       
    polygon = [] ## List that stores the vertices of the polygon
    for i in range(n):
        x = int(input(f"Enter x-coordinate of vertex {i + 1}: "))
        y = int(input(f"Enter y-coordinate of vertex {i + 1}: "))
        polygon.append((x, y))
    polygon.append(polygon[0])  # Close the polygon by adding the first vertex at the end
    xs = [vertex[0] for vertex in polygon] # List that stores the x-coordinates of the vertices
    ys = [vertex[1] for vertex in polygon] # List that stores the y-coordinates of the vertices
    return polygon,xs,ys

def compute_intersection(s, p, boundary):
    x1, y1 = s
    x2, y2 = p
    if boundary == "Left":
        x_int = X_MIN
        y_int = y1 + (y2 - y1) * (X_MIN - x1) / (x2 - x1)
    elif boundary == "Right":
        x_int = X_MAX
        y_int = y1 + (y2 - y1) * (X_MAX - x1) / (x2 - x1)
    elif boundary == "Bottom":
        y_int = Y_MIN
        x_int = x1 + (x2 - x1) * (Y_MIN - y1) / (y2 - y1)
    elif boundary == "Top":
        y_int = Y_MAX
        x_int = x1 + (x2 - x1) * (Y_MAX - y1) / (y2 - y1)

    return (x_int, y_int)

def clip_polygon(polygon,boundary):
    clipped_polygon = []
    s = polygon[-1]  # Start with the first vertex of the polygon
    for p in polygon:
        s_inside = is_inside(s[0], s[1], boundary)
        p_inside = is_inside(p[0], p[1], boundary)
    
        if p_inside:
            if s_inside:
                clipped_polygon.append(p) ## Both vertices are inside,so output is p (Current vertex)
            else:
                 ## s is outside and p is inside, so output the intersection point and p
                intersection = compute_intersection(s, p, boundary)
                clipped_polygon.append(intersection)
                clipped_polygon.append(p)
        else:
            if s_inside:
                # s is inside and p is outside
                clipped_polygon.append(compute_intersection(s, p, boundary))

        s = p  # Move to the next edge

        polygon = clipped_polygon
    print(f"\nThe vertices of the polygon after clipping at {boundary} boundary are: ")
    for vertex in polygon:
        print(vertex)
    return polygon

def get_clipped_polygon(polygon):
    for boundary in BOUNDARIES:
        polygon = clip_polygon(polygon, boundary)
    return polygon


original_polygon ,oxs,oys= get_polygon_vertices()

print("\nThe vertices of the original polygon are: ")
for vertex in original_polygon:
    print(vertex)

polygon = get_clipped_polygon(original_polygon)

print("\nThe vertices of the clipped polygon are: ")
for vertex in polygon:
    print(vertex)

nxs = [vertex[0] for vertex in polygon] # List that stores the x-coordinates of the clipped polygon vertices
nys = [vertex[1] for vertex in polygon] # List that stores the y-coordinates of the clipped polygon vertices


fig , ax = plt.subplots()
ax.plot(oxs, oys, 'b--')
ax.plot(nxs, nys, 'g-o')
ax.fill(nxs, nys, color='green', alpha=0.3)
ax.plot([X_MIN, X_MAX, X_MAX, X_MIN, X_MIN], [Y_MIN, Y_MIN, Y_MAX, Y_MAX, Y_MIN], 'r')
fig.savefig(f"clipped_polygon.png", dpi=300)
plt.show()
