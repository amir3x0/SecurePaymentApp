import hashlib
import random
from sympy import isprime, nextprime, mod_inverse
import sympy 

class SchnorrSignature:
    def __init__(self, p, q, g):
        self.p = p
        self.q = q
        self.g = g
        self.x = None  # Private key
        self.y = None  # Public key

    def generate_keys(self):
        """Generate private key x and public key y."""
        self.x = random.randint(1, self.q - 1)  # Private key
        self.y = pow(self.g, self.x)%self.p  # Public key
        print(f"Generated keys - Private key (x): {self.x}, Public key (y): {self.y}")

    def hash_function(self, data):
        """Hash function H"""
        return int(hashlib.sha256(data.encode()).hexdigest(), 16)

    def sign(self, M):
        """Generate a Schnorr signature for the message M."""
        if self.x is None:
            raise ValueError("Private key x is not initialized. Generate keys first.")

        # Choose a random integer k (nonce)
        k = random.randint(1, self.q - 1)
        print(f"Generated k: {k}")
        
        # Compute r
        r = pow(self.g, k)
        print(f"Computed r: {r}")

        # Compute e
        e = self.hash_function(str(r) + str(M))
        print(f"Computed e: {e}")

        # Compute s
        s = (k + self.x * e)
        print(f"Computed s: {s}")
        
        return r, s
    
    def verify(self, M, r, s, y):
        """Verify a Schnorr signature."""
        
        # Compute e
        e = self.hash_function(str(r) + str(M))
        print(f"Computed e: {e}")

        # Compute v1
        v1 = pow(self.g, s, self.p)
        print(f"Computed v1: {v1}")

        # Compute v2
        v2 = (pow(y, e,self.p) * r) % self.p
        print(f"Computed v2: {v2}")

        return v1 == v2


def generate_schnorr_parameters(bits):
    """Generates Schnorr parameters p, q, and a."""

    while True:
        # Generate a random prime p of specified bit length
        p = sympy.randprime(2**(bits-1), 2**bits)
        
        # Compute p-1
        p_minus_one = p - 1

        # Factorize p-1
        factors = sympy.factorint(p_minus_one)

        # Find a large prime divisor q
        q_candidates = [factor for factor, exponent in factors.items() if sympy.isprime(factor)]
        
        if not q_candidates:
            continue  # If no prime factors found, generate a new p

        q = max(q_candidates)

        # Ensure 1 < q < p-1
        if 1 < q < p - 1:
            break

    # Choose a generator a
    # a should be a primitive root mod p. Here, 2 is often used as a starting point.
    a = 2

    return p, q, a


#used generate_schnorr_parameters(8) to create difrrent public keys and stored them in 2d array
import numpy as np
# p , q , g=2
# Define the 2D array with the provided values
schnorr_public_keys = [
    [211, 7, 2],
    [163, 3, 2],
    [181, 5, 2],
    [223, 37, 2],
    [157, 13, 2],
    [173, 43, 2],
    [137, 17, 2],
    [251, 5, 2],
    [211, 7, 2],
    [251, 5, 2],
    [223, 37, 2],
    [173, 43, 2],
    [137, 17, 2],
    [251, 5, 2],
    [223, 37, 2],
    [163, 3, 2],
    [139, 23, 2],
    [251, 5, 2],
    [137, 17, 2],
    [227, 113, 2]
]