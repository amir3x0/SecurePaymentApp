class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def __str__(self):
        return f"({self.x}, {self.y})"

# EC parameters (updated values)
a = 2
b = 3
p = 101  # A different small prime number for the field

# Generator point on the curve
G = Point(3, 6)

def is_point_on_curve(point):
    """Check if a point lies on the elliptic curve."""
    return (point.y**2) % p == (point.x**3 + a * point.x + b) % p

def extended_gcd(a, b):
    """Extended Euclidean Algorithm to find the GCD of a and b."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def inv_mod(a, p):
    """Compute the modular inverse of a mod p using the Extended Euclidean Algorithm."""
    lm, hm = 1, 0
    low, high = a % p, p
    while low > 1:
        ratio = high // low
        nm, new = hm - lm * ratio, high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % p


def add_points(P, Q):
    """Add two points P and Q on the elliptic curve."""
    if P.x == Q.x and P.y == -Q.y % p:
        return Point(0, 0)  # Point at infinity

    if P.x == Q.x and P.y == Q.y:
        # Point doubling
        if P.y == 0:
            return Point(0, 0)
        s = (3 * P.x * P.x + a) * inv_mod(2 * P.y, p) % p
    else:
        if Q.x == P.x:
            raise ValueError(f"Points {P} and {Q} have the same x-coordinate, causing a zero denominator.")
        inv = inv_mod((Q.x - P.x) % p, p)
        if inv is None:
            raise ValueError(f"No modular inverse for {(Q.x - P.x) % p} mod {p}")
        s = (Q.y - P.y) * inv % p

    x_r = (s * s - P.x - Q.x) % p
    y_r = (s * (P.x - x_r) - P.y) % p
    return Point(x_r, y_r)

def scalar_mult(k, P):
    """Multiply point P by scalar k on the elliptic curve."""
    if k < 0:
        return scalar_mult(-k, Point(P.x, -P.y % p))
    
    R = Point(0, 0)
    Q = P

    while k > 0:
        if k % 2 == 1:
            R = add_points(R, Q)
        Q = add_points(Q, Q)
        k //= 2

    return R

