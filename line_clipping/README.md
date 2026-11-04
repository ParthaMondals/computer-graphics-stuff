# Cohen–Sutherland Line Clipping Algorithm

A Python implementation of the **Cohen–Sutherland Line Clipping Algorithm** using explicit 4-bit region codes and bitwise operations. The program clips a given line segment against a predefined rectangular clipping window and visualizes the result using Matplotlib.

## Overview

In Computer Graphics, line clipping is the process of removing portions of a line that lie outside a specified viewing area.

The Cohen–Sutherland algorithm is a classical line clipping algorithm that uses region codes to determine whether a line segment should be:

- **Trivially Accepted:** Both endpoints lie inside the clipping window.
- **Trivially Rejected:** Both endpoints lie outside a common boundary.
- **Clipped:** The line intersects one or more boundaries of the clipping window.

This project implements the algorithm from scratch in Python without using any built-in or library-based clipping functions.

## Features

- Implements the Cohen–Sutherland line clipping algorithm.
- Uses explicit 4-bit region codes.
- Uses bitwise AND (`&`) and OR (`|`) operations for acceptance and rejection decisions.
- Supports keyboard input for a single line segment.
- Uses a fixed rectangular clipping window.
- Handles zero-length, vertical, and horizontal lines.
- Validates input coordinates and clipping window boundaries.
- Displays the original line and clipped portion using Matplotlib.
- Displays the clipping status and resulting endpoints in the console.

## Clipping Window

The clipping window is predefined using four constants:

```python
X_MIN = 20
X_MAX = 80
Y_MIN = 20
Y_MAX = 80
```

Therefore, the clipping window extends from `(20, 20)` to `(80, 80)`.

## Region Codes

Each endpoint is assigned a 4-bit region code based on its position relative to the clipping window.

| Bit | Flag   | Condition | Meaning |
| --- | ------ | --------- | ------- |
| 1   | LEFT   | x < X_MIN | Left    |
| 2   | RIGHT  | x > X_MAX | Right   |
| 3   | BOTTOM | y < Y_MIN | Below   |
| 4   | TOP    | y > Y_MAX | Above   |

### Region Code Representation

| Region | Binary Code |
| ------ | ----------- |
| Inside | `0000`      |
| Left   | `0001`      |
| Right  | `0010`      |
| Below  | `0100`      |
| Above  | `1000`      |

A point may have multiple bits set if it lies outside the window in more than one direction.

## Algorithm

The implementation follows these steps:

1. Calculate the region codes of both endpoints.
2. Check for trivial acceptance using bitwise OR.
3. Check for trivial rejection using bitwise AND.
4. If neither condition is satisfied, select an endpoint outside the clipping window.
5. Determine the clipping boundary using its region code.
6. Calculate the intersection point.
7. Replace the selected endpoint with the intersection point.
8. Recalculate its region code.
9. Repeat until the line is accepted or rejected.

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Cohen-Sutherland-Line-Clipping.git
```

### 2. Navigate to the project directory

```bash
cd Cohen-Sutherland-Line-Clipping
```

### 3. Install the required library

```bash
pip install matplotlib
```

### 4. Run the program

```bash
python main.py
```

## Input Format

The program accepts four integer coordinates from the keyboard:

- `x1` – X-coordinate of the first endpoint.
- `y1` – Y-coordinate of the first endpoint.
- `x2` – X-coordinate of the second endpoint.
- `y2` – Y-coordinate of the second endpoint.

**Input constraints:**

- All coordinates must be integers.
- All coordinates must lie within the range `0–100`.
- Only one line segment is processed per execution.

## Sample Execution

### Example 1: Partially Clipped Line

**Input:**

```text
Enter x1: 10
Enter y1: 30
Enter x2: 60
Enter y2: 70
```

**Output:**

```text
Status: Clipped
Clipped P1 = (20.0, 38.0)
Clipped P2 = (60.0, 70.0)
```

### Example 2: Trivially Accepted Line

**Input:**

```text
Enter x1: 30
Enter y1: 32
Enter x2: 70
Enter y2: 73
```

**Output:**

```text
Status: Trivially Accepted
Clipped P1 = (30.0, 32.0)
Clipped P2 = (70.0, 73.0)
```

### Example 3: Trivially Rejected Line

**Input:**

```text
Enter x1: 5
Enter y1: 10
Enter x2: 10
Enter y2: 15
```

**Output:**

```text
Status: Rejected
The line is completely outside the clipping window.
```

###
