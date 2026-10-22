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


def ceil_int(value):
    """Smallest integer that is not below value."""
    whole = int(value)
    return whole if value <= whole else whole + 1


def ellipse_points(center_x, center_y, radius_x, radius_y, steps):
    """Float points around an ellipse, to be joined into a polyline."""
    return [(center_x + radius_x * cosine(2 * PI * step / steps),
             center_y + radius_y * sine(2 * PI * step / steps)) for step in range(steps)]


def line_polygon(x0, y0, x1, y1, width):
    """Corners of the rectangle that a line of a given thickness covers."""
    length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    if length == 0:
        return [(x0 - width / 2, y0 - width / 2), (x0 + width / 2, y0 - width / 2),
                (x0 + width / 2, y0 + width / 2), (x0 - width / 2, y0 + width / 2)]
    offset_x = -(y1 - y0) / length * width / 2
    offset_y = (x1 - x0) / length * width / 2
    return [(x0 + offset_x, y0 + offset_y), (x1 + offset_x, y1 + offset_y),
            (x1 - offset_x, y1 - offset_y), (x0 - offset_x, y0 - offset_y)]


def polygon_spans(points):
    """Pixel spans (y, first_x, end_x) whose centers lie inside a polygon (even-odd rule).

    A pixel (x, y) has its center at (x + 0.5, y + 0.5); end_x is exclusive.
    """
    top = min(y for _, y in points)
    bottom = max(y for _, y in points)
    spans = []
    for y in range(int(top - 1), int(bottom) + 2):
        center_y = y + 0.5
        crossings = []
        for index, (x0, y0) in enumerate(points):
            x1, y1 = points[(index + 1) % len(points)]
            if y0 != y1 and min(y0, y1) <= center_y < max(y0, y1):
                crossings.append(x0 + (center_y - y0) * (x1 - x0) / (y1 - y0))
        crossings.sort()
        for left, right in zip(crossings[0::2], crossings[1::2]):
            first, end = ceil_int(left - 0.5), ceil_int(right - 0.5)
            if end > first:
                spans.append((y, first, end))
    return spans


def ellipse_spans(center_x, center_y, radius_x, radius_y):
    """Pixel spans (y, first_x, end_x) whose centers lie inside an ellipse."""
    spans = []
    if radius_x <= 0 or radius_y <= 0:
        return spans
    for y in range(int(center_y - radius_y) - 1, int(center_y + radius_y) + 2):
        ratio = (y + 0.5 - center_y) / radius_y
        if ratio * ratio <= 1:
            half_width = radius_x * (1 - ratio * ratio) ** 0.5
            first = ceil_int(center_x - half_width - 0.5)
            end = ceil_int(center_x + half_width - 0.5)
            if end > first:
                spans.append((y, first, end))
    return spans
