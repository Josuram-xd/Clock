"""Raster primitives on a pixel grid: lines, rectangles, and ellipses (pure geometry).

Ellipse outlines use our own sine and cosine (mymath), not a standard library.
"""

from mymath.trigonometry import PI, cosine, sine


def line_points(x0, y0, x1, y1):
    """Pixels of the line between two points (Bresenham's algorithm)."""
    x0, y0, x1, y1 = round(x0), round(y0), round(x1), round(y1)
    delta_x = abs(x1 - x0)
    delta_y = -abs(y1 - y0)
    step_x = 1 if x0 < x1 else -1
    step_y = 1 if y0 < y1 else -1
    error = delta_x + delta_y
    points = []
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return points
        doubled = 2 * error
        if doubled >= delta_y:
            error += delta_y
            x0 += step_x
        if doubled <= delta_x:
            error += delta_x
            y0 += step_y


def ellipse_outline(x0, y0, x1, y1):
    """Pixels of the ellipse inscribed in a bounding box."""
    center_x, center_y = (x0 + x1) / 2, (y0 + y1) / 2
    radius_x, radius_y = abs(x1 - x0) / 2, abs(y1 - y0) / 2
    steps = max(16, round(6 * (radius_x + radius_y)))
    points = []
    for step in range(steps):
        angle = 2 * PI * step / steps
        points.append((round(center_x + radius_x * cosine(angle)),
                       round(center_y + radius_y * sine(angle))))
    return points


def ellipse_fill(x0, y0, x1, y1):
    """Pixels inside the ellipse inscribed in a bounding box, row by row."""
    center_x, center_y = (x0 + x1) / 2, (y0 + y1) / 2
    radius_x, radius_y = abs(x1 - x0) / 2, abs(y1 - y0) / 2
    points = []
    if radius_y == 0:
        return points
    for y in range(round(center_y - radius_y), round(center_y + radius_y) + 1):
        ratio = (y - center_y) / radius_y
        if ratio * ratio <= 1:
            half_width = radius_x * (1 - ratio * ratio) ** 0.5
            for x in range(round(center_x - half_width), round(center_x + half_width) + 1):
                points.append((x, y))
    return points


def rectangle_outline(x0, y0, x1, y1):
    """Pixels of the four sides of a rectangle."""
    x0, x1 = sorted((round(x0), round(x1)))
    y0, y1 = sorted((round(y0), round(y1)))
    points = [(x, y) for x in range(x0, x1 + 1) for y in (y0, y1)]
    points += [(x, y) for y in range(y0 + 1, y1) for x in (x0, x1)]
    return points


def rectangle_fill(x0, y0, x1, y1):
    """Pixels inside a rectangle."""
    x0, x1 = sorted((round(x0), round(x1)))
    y0, y1 = sorted((round(y0), round(y1)))
    return [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
