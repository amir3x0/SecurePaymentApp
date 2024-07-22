# EC_DH.py

class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

# EC parameters (example values, use proper cryptographic parameters in production)
a = 2
b = 3
p = 97  # A small prime number for the field

# Generator point on the curve
G = Point(3, 6)

def is_point_on_curve(point):
    """Check if a point lies on the elliptic curve."""
    return (point.y**2) % p == (point.x**3 + a * point.x + b) % p

def inv_mod(k, p):
    """Compute the modular inverse of k modulo p."""
    k = k % p
    for x in range(1, p):
        if (k * x) % p == 1:
            return x
    return None

def add_points(P, Q):
    """Add two points P and Q on the elliptic curve."""
    if P.x == Q.x and P.y == -Q.y:
        return Point(0, 0)
    if P.x == Q.x and P.y == Q.y:
        s = (3 * P.x * P.x + a) * inv_mod(2 * P.y, p) % p
    else:
        s = (Q.y - P.y) * inv_mod(Q.x - P.x, p) % p
    x_r = (s * s - P.x - Q.x) % p
    y_r = (s * (P.x - x_r) - P.y) % p
    return Point(x_r, y_r)

def scalar_mult(k, P):
    """Multiply point P by scalar k on the elliptic curve."""
    R = Point(0, 0)
    Q = P
    while k > 0:
        if k % 2 == 1:
            R = add_points(R, Q)
        Q = add_points(Q, Q)
        k = k // 2
    return R
