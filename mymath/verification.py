"""Library self-test: compares sine and cosine against known values."""

from mymath.trigonometry import cosine, degrees_to_radians, sine

TOLERANCE = 1e-6

# Known values: (degrees, expected sine, expected cosine)
KNOWN_VALUES = [
    (0, 0.0, 1.0),
    (30, 0.5, 0.8660254037844386),
    (45, 0.7071067811865476, 0.7071067811865476),
    (60, 0.8660254037844386, 0.5),
    (90, 1.0, 0.0),
    (180, 0.0, -1.0),
    (270, -1.0, 0.0),
    (360, 0.0, 1.0),
]


def compare(name, obtained, expected):
    """Print OK or FALLÓ for one value and return True if it passes the test."""
    passed = abs(obtained - expected) <= TOLERANCE
    status = "OK" if passed else "FALLÓ"
    print(f"  {name}: obtenido={obtained:.9f} esperado={expected:.9f} -> {status}")
    return passed


def verify_library():
    """Self-test: compares sine and cosine against known values."""
    print("AUTOTEST de la librería mymath (tolerancia 1e-6):")
    results = []
    for degrees, expected_sine, expected_cosine in KNOWN_VALUES:
        radians = degrees_to_radians(degrees)
        results.append(compare(f"seno({degrees} gr)", sine(radians), expected_sine))
        results.append(compare(f"coseno({degrees} gr)", cosine(radians), expected_cosine))
    if all(results):
        print("Resultado global: OK")
    else:
        print("Resultado global: FALLÓ")
