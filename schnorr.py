from EC_DH import Point, scalar_mult, add_points, p, G
import hashlib
import random

class Schnorr:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = scalar_mult(private_key, G)

    def sign(self, message):
        # Generate a random nonce
        k = random.SystemRandom().randint(1, p - 1)
        R = scalar_mult(k, G)
        r = R.x % p

        # Hash the message and r
        e = int.from_bytes(hashlib.sha256((str(r) + message).encode()).digest(), byteorder='big') % p

        # Compute s
        s = (k + e * self.private_key) % p

        print(f"Signing Debug - k: {k}, R: ({R.x}, {R.y}), r: {r}, e: {e}, s: {s}")
        return (r, s)

    def verify(self, message, signature):
        r, s = signature
        e = int.from_bytes(hashlib.sha256((str(r) + message).encode()).digest(), byteorder='big') % p
        R1 = scalar_mult(s, G)
        R2 = scalar_mult(-e, self.public_key)
        R = add_points(R1, R2)

        print(f"Verification Debug - r: {r}, s: {s}, e: {e}, R1: ({R1.x}, {R1.y}), R2: ({R2.x}, {R2.y}), R: ({R.x}, {R.y}), R.x % p: {R.x % p}")
        return R.x % p == r

