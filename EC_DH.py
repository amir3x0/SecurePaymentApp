import random

class EllipticCurve:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

    def mod_inv(self, k, p):
        """Modular inverse using Extended Euclidean Algorithm."""
        if k == 0:
            raise ZeroDivisionError("division by zero")
        if k < 0:
            return p - self.mod_inv(-k, p)
        s, old_s = 0, 1
        t, old_t = 1, 0
        r, old_r = p, k
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
        gcd, x, y = old_r, old_s, old_t
        return x % p

    def point_add(self, P, Q):
        """Add two points P and Q on the elliptic curve."""
        if P is None:
            return Q
        if Q is None:
            return P
        if P == Q:
            return self.point_double(P)
        if P[0] == Q[0] and P[1] != Q[1]:
            return None

        # slope (lambda) = (y2 - y1) / (x2 - x1)
        lam = ((Q[1] - P[1]) * self.mod_inv(Q[0] - P[0], self.p)) % self.p
        x_r = (lam ** 2 - P[0] - Q[0]) % self.p
        y_r = (lam * (P[0] - x_r) - P[1]) % self.p
        return (x_r, y_r)

    def point_double(self, P):
        """Double a point P on the elliptic curve."""
        if P is None:
            return None

        # slope (lambda) = (3*x^2 + a) / (2*y)
        lam = ((3 * P[0] ** 2 + self.a) * self.mod_inv(2 * P[1], self.p)) % self.p
        x_r = (lam ** 2 - 2 * P[0]) % self.p
        y_r = (lam * (P[0] - x_r) - P[1]) % self.p
        return (x_r, y_r)

    def scalar_mult(self, k, P):
        """Multiply point P by scalar k using the double-and-add method."""
        result = None
        addend = P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1

        return result

# SECP256k1 parameters
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

curve = EllipticCurve(p, a, b)
G = (Gx, Gy)

# Static private keys
Ka = 1234567890
Kb = 9876543210

