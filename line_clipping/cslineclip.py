
import matplotlib.pyplot as plt


# ============================================================
# 1. CLIPPING WINDOW CONSTANTS
# ============================================================

# Define the fixed boundaries of the clipping window.
X_MIN = 20
X_MAX = 80
Y_MIN = 20
Y_MAX = 80

print(f"The Clipping window: from ({X_MIN},{Y_MIN}) to ({X_MAX},{Y_MAX})\n")

# ============================================================
# 2. REGION CODE BIT FLAGS
# ============================================================

# Each flag represents one bit of the 4-bit region code.
LEFT = 1       # 0001: Point is to the left of the window.
RIGHT = 2      # 0010: Point is to the right of the window.
BOTTOM = 4     # 0100: Point is below the window.
TOP = 8        # 1000: Point is above the window.


# ============================================================
# 3. FUNCTION: compute_code()
# ============================================================

def compute_code(x, y):
    """
    Purpose:
        Calculate the 4-bit region code of a point.

    Parameters:
        x: X-coordinate of the point.
        y: Y-coordinate of the point.

    Returns:
        Integer region code between 0 and 15.

    Logic:
        Check whether the point lies outside any of the
        four boundaries of the clipping window.
        Set the corresponding bits using bitwise OR.
    """

    # Initially assume that the point is inside the window.
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


# ============================================================
# 4. FUNCTION: compute_intersection()
# ============================================================

def compute_intersection(x1, y1, x2, y2, code_out):
    """
    Purpose:
        Calculate the intersection point between a line
        and the clipping boundary indicated by code_out.

    Parameters:
        x1, y1: First endpoint coordinates.
        x2, y2: Second endpoint coordinates.
        code_out: Region code of the outside endpoint.

    Returns:
        Tuple (x, y) containing the intersection coordinates.

    Logic:
        Use if/elif to identify exactly one clipping boundary.
        Handle vertical and horizontal lines explicitly
        to avoid division by zero.
    """

    # --------------------------------------------------------
    # CASE 1: LEFT BOUNDARY
    # --------------------------------------------------------

    if code_out & LEFT:

        # The intersection must lie on X_MIN.
        x_int = X_MIN

        # A vertical line has no change in X-coordinate.
        if x1 == x2:
            y_int = y1

        # Calculate the Y-coordinate using the line equation.
        else:
            y_int = y1 + (y2 - y1) * (X_MIN - x1) / (x2 - x1)

    # --------------------------------------------------------
    # CASE 2: RIGHT BOUNDARY
    # --------------------------------------------------------

    elif code_out & RIGHT:

        # The intersection must lie on X_MAX.
        x_int = X_MAX

        # A vertical line has no change in X-coordinate.
        if x1 == x2:
            y_int = y1

        # Calculate the Y-coordinate using the line equation.
        else:
            y_int = y1 + (y2 - y1) * (X_MAX - x1) / (x2 - x1)

    # --------------------------------------------------------
    # CASE 3: BOTTOM BOUNDARY
    # --------------------------------------------------------

    elif code_out & BOTTOM:

        # The intersection must lie on Y_MIN.
        y_int = Y_MIN

        # A horizontal line has no change in Y-coordinate.
        if y1 == y2:
            x_int = x1

        # Calculate the X-coordinate using the line equation.
        else:
            x_int = x1 + (x2 - x1) * (Y_MIN - y1) / (y2 - y1)

    # --------------------------------------------------------
    # CASE 4: TOP BOUNDARY
    # --------------------------------------------------------

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


# ============================================================
# 5. FUNCTION: clip_line()
# ============================================================

def clip_line(p1, p2):
    """
    Purpose:
        Implement the Cohen-Sutherland line clipping algorithm.

    Parameters:
        p1: First endpoint as a tuple (x1, y1).
        p2: Second endpoint as a tuple (x2, y2).

    Returns:
        Tuple containing the clipped endpoints:
            (p1_new, p2_new)

        Returns None if the line is completely outside.

    Logic:
        1. Handle zero-length lines.
        2. Calculate endpoint region codes.
        3. Apply trivial acceptance.
        4. Apply trivial rejection.
        5. Calculate intersection with the relevant boundary.
        6. Replace the outside endpoint.
        7. Repeat until accepted or rejected.
    """

    # Extract coordinates from the endpoint tuples.
    x1, y1 = p1
    x2, y2 = p2

    # --------------------------------------------------------
    # CASE 1: ZERO-LENGTH LINE
    # --------------------------------------------------------

    # Check whether both endpoints represent the same point.
    if p1 == p2:

        # Calculate the region code of the single point.
        code = compute_code(x1, y1)

        # Accept if the point is inside the clipping window.
        if code == 0:
            return (p1, p2)

        # Otherwise, reject the point.
        return None

    # --------------------------------------------------------
    # STEP 1: COMPUTE INITIAL REGION CODES
    # --------------------------------------------------------

    # Calculate region codes for both endpoints.
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    # --------------------------------------------------------
    # STEP 2: ACCEPT / REJECT / CLIP LOOP
    # --------------------------------------------------------

    while True:

        # ----------------------------------------------------
        # CASE A: TRIVIALLY ACCEPT
        # ----------------------------------------------------

        # Bitwise OR checks whether both endpoints are inside.
        if (code1 | code2) == 0:

            # Return the entire line segment.
            return ((x1, y1), (x2, y2))

        # ----------------------------------------------------
        # CASE B: TRIVIALLY REJECT
        # ----------------------------------------------------

        # Bitwise AND checks whether both endpoints share
        # at least one outside region.
        elif (code1 & code2) != 0:

            # The line cannot enter the clipping window.
            return None

        # ----------------------------------------------------
        # CASE C: PARTIAL ACCEPTANCE / CLIPPING REQUIRED
        # ----------------------------------------------------

        else:

            # Prefer the first endpoint if it is outside.
            if code1 != 0:
                code_out = code1

            # Otherwise, select the second endpoint.
            else:
                code_out = code2

            # ------------------------------------------------
            # CALCULATE INTERSECTION POINT
            # ------------------------------------------------

            # Use the selected endpoint's region code to
            # determine which boundary must be intersected.
            intersection = compute_intersection(
                x1, y1, x2, y2, code_out
            )

            # Extract the intersection coordinates.
            x_int, y_int = intersection

            # ------------------------------------------------
            # REPLACE THE SELECTED OUTSIDE ENDPOINT
            # ------------------------------------------------

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


# ============================================================
# 6. FUNCTION: validate_window()
# ============================================================

def validate_window():
    """
    Purpose:
        Validate the clipping window constants.

    Returns:
        True if the window is valid.

    Logic:
        X_MIN must be smaller than X_MAX.
        Y_MIN must be smaller than Y_MAX.
    """

    # Check whether the horizontal boundaries are valid.
    if X_MIN >= X_MAX:
        return False

    # Check whether the vertical boundaries are valid.
    if Y_MIN >= Y_MAX:
        return False

    return True


# ============================================================
# 7. FUNCTION: get_line_input()
# ============================================================

def get_line_input():
    """
    Purpose:
        Accept four integer coordinates from the keyboard.

    Returns:
        A tuple containing two endpoint tuples:
            ((x1, y1), (x2, y2))

    Logic:
        1. Read four values.
        2. Convert them into integers.
        3. Validate the coordinate range (0-100).
        4. Display an error and exit for invalid input.
    """

    try:

        # Read the four coordinates from the keyboard.
        x1 = int(input("Enter x1: "))
        y1 = int(input("Enter y1: "))
        x2 = int(input("Enter x2: "))
        y2 = int(input("Enter y2: "))

    except ValueError:

        # Handle non-integer input.
        print("Error: All coordinates must be integers.")
        raise SystemExit

    # Store all four coordinates for range validation.
    coordinates = (x1, y1, x2, y2)

    # Check whether every coordinate lies between 0 and 100.
    for value in coordinates:

        if value < 0 or value > 100:

            print("Error: All coordinates must be in range 0-100.")
            raise SystemExit

    # Return the line as a tuple of two points.
    return ((x1, y1), (x2, y2))


# ============================================================
# 8. FUNCTION: display_result()
# ============================================================

def display_result(original_line, clipped_line):
    """
    Purpose:
        Display the original line and its clipping result.

    Parameters:
        original_line: Original endpoint tuple.
        clipped_line: Clipped endpoint tuple or None.

    Output:
        Console status and a Matplotlib visualization.
    """

    # Extract the original endpoint coordinates.
    (x1, y1), (x2, y2) = original_line

    # Print the original line information.
    print("\nOriginal Line:")
    print("P1 =", (x1, y1))
    print("P2 =", (x2, y2))

    # --------------------------------------------------------
    # DISPLAY CONSOLE RESULT
    # --------------------------------------------------------

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

        # Display the resulting endpoints as floating-point values.
        print("Clipped P1 =", tuple(map(float, p1_new)))
        print("Clipped P2 =", tuple(map(float, p2_new)))

    # --------------------------------------------------------
    # CREATE MATPLOTLIB FIGURE
    # --------------------------------------------------------

    # Create a figure and its plotting axes.
    fig = plt.subplots(figsize=(8, 8))

    # --------------------------------------------------------
    # DRAW THE CLIPPING WINDOW
    # --------------------------------------------------------

    # Plot the four sides of the rectangular clipping window.
    plt.plot(
        [X_MIN, X_MAX, X_MAX, X_MIN, X_MIN],
        [Y_MIN, Y_MIN, Y_MAX, Y_MAX, Y_MIN],
        color="black",
        linewidth=2,
        label="Clipping Window"
    )

    # --------------------------------------------------------
    # DRAW THE ORIGINAL LINE
    # --------------------------------------------------------

    # Display the original line using a dashed red line.
    plt.plot(
        [x1, x2],
        [y1, y2],
        color="red",
        linestyle="--",
        linewidth=1.5,
        label="Original Line"
    )

    # --------------------------------------------------------
    # DRAW THE CLIPPED LINE
    # --------------------------------------------------------

    # Draw the resulting line only if it was accepted.
    if clipped_line is not None:

        # Extract the clipped endpoint coordinates.
        (cx1, cy1), (cx2, cy2) = clipped_line

        # Highlight the clipped portion using a blue line.
        plt.plot(
            [cx1, cx2],
            [cy1, cy2],
            color="blue",
            linewidth=3,
            label="Clipped Line"
        )

    # --------------------------------------------------------
    # GRAPH CONFIGURATION
    # --------------------------------------------------------

    # Set the coordinate system limits.
    plt.xlim(0, 100)
    plt.ylim(0, 100)

    # Add labels to the coordinate axes.
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")

    # Add the graph title.
    plt.title("Cohen-Sutherland Line Clipping Algorithm")

    # Display a grid for easier coordinate observation.
    plt.grid(True)

    # Maintain equal scaling on both axes.
##    plt.aspect("equal", adjustable="box")

    # Display the legend.
    plt.legend()

    # Display the graph window.
    plt.show()


# ============================================================
# 9. MAIN PROGRAM
# ============================================================

def main():
    """
    Purpose:
        Control the overall execution of the program.

    Logic:
        1. Validate the clipping window.
        2. Accept line coordinates.
        3. Execute the clipping algorithm.
        4. Display the result.
    """

    # Validate the predefined clipping window.
    if not validate_window():

        print("Error: Invalid clipping window boundaries.")
        raise SystemExit

    # Get the original line segment from the keyboard.
    original_line = get_line_input()

    # Execute the Cohen-Sutherland clipping algorithm.
    clipped_line = clip_line(
        original_line[0],
        original_line[1]
    )

    # Display the clipping result and graphical output.
    display_result(original_line, clipped_line)


# Execute the main function when the program runs directly.
if __name__ == "__main__":
    main()
