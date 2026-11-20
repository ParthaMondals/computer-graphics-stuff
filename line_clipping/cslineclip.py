import matplotlib.pyplot as plt

# ============================================================
# 1. CLIPPING WINDOW CONSTANTS
# ============================================================

# Define the fixed boundaries of the clipping window.
X_MIN = 50
X_MAX = 200
Y_MIN = 50
Y_MAX = 150
print(f"The Clipping window: from ({X_MIN},{Y_MIN}) to ({X_MAX},{Y_MAX})\n")

# ============================================================
# 2. REGION CODE BIT FLAGS
# ============================================================

# Each flag represents one bit of the 4-bit region code.
LEFT = 1       # 0001: Point is to the left of the window.
RIGHT = 2      # 0010: Point is to the right of the window.
BOTTOM = 4     # 0100: Point is below the window.
TOP = 8        # 1000: Point is above the window.


def compute_code(x, y):
##    """Return a 4-bit region code describing a point's position relative to the window."""
    code = 0

    # Check whether the point is to the left.
    if x < X_MIN:
        code |= LEFT

    # Check whether the point is to the right.
    if x > X_MAX:
        code |= RIGHT

    # Check whether the point is below the window.
    if y < Y_MIN:
        code |= BOTTOM

    # Check whether the point is above the window.
    if y > Y_MAX:
        code |= TOP

    # Return the calculated 4-bit region code.
    return code


def compute_intersection(x1, y1, x2, y2, code_out):
##    """Find where a line segment intersects the window edge indicated by code_out."""
    
    if code_out & LEFT:
        # The intersection must lie on X_MIN.
        x_int = X_MIN

        # A vertical line has no change in X-coordinate.
        if x1 == x2:
            y_int = y1

        # Calculate the Y-coordinate using the line equation.
        else:
            y_int = y1 + (y2 - y1) * (X_MIN - x1) / (x2 - x1)


    elif code_out & RIGHT:

        # The intersection must lie on X_MAX.
        x_int = X_MAX

        # A vertical line has no change in X-coordinate.
        if x1 == x2:
            y_int = y1

        # Calculate the Y-coordinate using the line equation.
        else:
            y_int = y1 + (y2 - y1) * (X_MAX - x1) / (x2 - x1)


    elif code_out & BOTTOM:

        # The intersection must lie on Y_MIN.
        y_int = Y_MIN

        # A horizontal line has no change in Y-coordinate.
        if y1 == y2:
            x_int = x1

        # Calculate the X-coordinate using the line equation.
        else:
            x_int = x1 + (x2 - x1) * (Y_MIN - y1) / (y2 - y1)


    elif code_out & TOP:

        # The intersection must lie on Y_MAX.
        y_int = Y_MAX

        # A horizontal line has no change in Y-coordinate.
        if y1 == y2:
            x_int = x1

        # Calculate the X-coordinate using the line equation.
        else:
            x_int = x1 + (x2 - x1) * (Y_MAX - y1) / (y2 - y1)

    # Return the intersection point as a tuple.
    return (x_int, y_int)


def clip_line(p1, p2):
##    """Clip a line segment to the window; return its visible portion or None if rejected."""

    # Extract coordinates from the endpoint tuples.
    x1, y1 = p1
    x2, y2 = p2


    # Calculate region codes for both endpoints.
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    while True:

        # Trivially Accept
        if (code1 | code2) == 0:

            # Return the entire line segment.
            return ((x1, y1), (x2, y2))

        # Trivially Reject
        elif (code1 & code2) != 0:
            return None

        # Partially visible
        else:
            # Prefer the first endpoint if it is outside.
            if code1 != 0:
                code_out = code1

            # Otherwise, select the second endpoint.
            else:
                code_out = code2

            intersection_point = compute_intersection(
                x1, y1, x2, y2, code_out
            )

            # Extract the intersection coordinates.
            x_int, y_int = intersection_point


            # Replace the first endpoint if it was outside.
            if code_out == code1:

                x1 = x_int
                y1 = y_int

                # Recalculate its region code.
                code1 = compute_code(x1, y1)

            # Otherwise, replace the second endpoint.
            else:

                x2 = x_int
                y2 = y_int

                # Recalculate its region code.
                code2 = compute_code(x2, y2)


class line:
    def __init__(self):
        pass
    
    def input(self):
        self.xstart = int(input("Enter x1: "))
        self.ystart = int(input("Enter y1: "))
        self.xend = int(input("Enter x2: "))
        self.yend = int(input("Enter y2: "))

        for val in [self.xstart, self.xend, self.ystart, self.yend]:
            if val < 0 or val > 500:
                print("Error: All coordinates must be in range 0-100.")
                return None
        return ((self.xstart, self.ystart), (self.xend, self.yend))


def get_line_input():
##    """Read the line's endpoints, check their coordinate range, and return them."""
    lines_list = []
    num = int(input("How many lines: "))
    for i in range(num):
        l = line()
        print(f"\nEnter line {i+1}: \n")
        pts = l.input()
        lines_list.append(pts)
        
    return lines_list


def display_result(original_line, clipped_line,ax,first):
    # Extract the original endpoint coordinates.
    (x1, y1), (x2, y2) = original_line

    # Print the original line information.
    print("\nOriginal Line:")
    print("P1 =", (x1, y1))
    print("P2 =", (x2, y2))

    if clipped_line is None:
        # The line lies completely outside the window.
        print("\nStatus: Rejected")
        print("The line is completely outside the clipping window.")

    else:

        # Extract the resulting clipped endpoints.
        p1_new, p2_new = clipped_line

        # Check whether the resulting endpoints are unchanged.
        if p1_new == original_line[0] and p2_new == original_line[1]:

            print("\nStatus: Trivially Accepted")

        else:

            print("\nStatus: Clipped")

        # Display the resulting endpoints.
        print("Clipped P1 =", p1_new)
        print("Clipped P2 =", p2_new)

    # Display the original line using a dashed red line.
    ax.plot(
        [x1, x2],
        [y1, y2],
        color="red",
        linestyle="--",
        linewidth=1.5,
        label="Input Line" if first else "_nolegend_"
    )
    
    # Draw the resulting line only if it was accepted.
    if clipped_line is not None:

        # Extract the clipped endpoint coordinates.
        (cx1, cy1), (cx2, cy2) = clipped_line

        # Highlight the clipped portion using a blue line.
        ax.plot(
            [cx1, cx2],
            [cy1, cy2],
            color="blue",
            linewidth=3,
            label="Part kept after clipping" if first else "_nolegend_"
        )


## MAIN FUNCTION BEGINES
    
# Get the original line segment from the keyboard.
all_lines = get_line_input()

fig, ax = plt.subplots(figsize=(8, 8))

# Draw clipping window only once
ax.plot(
    [X_MIN, X_MAX, X_MAX, X_MIN, X_MIN],
    [Y_MIN, Y_MIN, Y_MAX, Y_MAX, Y_MIN],
    color="black",
    linewidth=2,
    label=f"Clipping Window: ({X_MIN},{Y_MIN}) to ({X_MAX},{Y_MAX})"
)
for i,aline in enumerate(all_lines):
    clipped_line = clip_line(aline[0], aline[1])
    display_result(aline, clipped_line, ax,i==0,)

# Configure graph only once
ax.set_xlim(0, 250)
ax.set_ylim(0, 200)
ax.set_xlabel("X-coordinate")
ax.set_ylabel("Y-coordinate")
ax.set_title("Cohen-Sutherland Line Clipping Algorithm")
ax.grid(True)
ax.set_aspect("equal")

# Display legend only once
plt.legend()

plt.show()
