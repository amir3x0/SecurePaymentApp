from EC_DH import Point, scalar_mult, add_points, p, G, n
import hashlib
import random

class Schnorr:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = scalar_mult(private_key, G)

    def sign(self, message):
        # Generate a random integer k such that 1 <= k <= n-1
        k = random.SystemRandom().randint(1, n - 1)
        
        # Calculate r = g^k mod p
        R = scalar_mult(k, G)
        r = R.x % p
        
        # Calculate e = hash(r || M), where || denotes concatenation
        e = int.from_bytes(hashlib.sha256((str(r) + message).encode()).digest(), byteorder='big') % p
        
        # Calculate s = (k - x * e) mod n
        s = (k - self.private_key * e) % n
        
        print(f"Signing Debug - k: {k}, R: ({R.x}, {R.y}), r: {r}, e: {e}, s: {s}")
        return (r, s)

    def verify(self, message, signature):
        r, s = signature

        # Verify that 1 <= r <= p-1 and 1 <= s <= n-1
        if not (1 <= r <= p - 1 and 1 <= s <= n - 1):
            print("Verification failed: r or s out of range.")
            return False
        
        # Calculate e = hash(r || M)
        e = int.from_bytes(hashlib.sha256((str(r) + message).encode()).digest(), byteorder='big') % p
        
        # Calculate v = g^(s + x * e) mod p
        S = scalar_mult(s, G)
        E = scalar_mult(e, self.public_key)
        V = add_points(S, E)
        v = V.x % p
        
        print(f"Verification Debug - r: {r}, s: {s}, e: {e}, S: ({S.x}, {S.y}), E: ({E.x}, {E.y}), V: ({V.x}, {V.y}), v: {v}")
        
        # If v = r, the signature is valid. Otherwise, the signature is invalid.
        return v == r
