# Secure Payment Application

This project implements a secure payment application using the following cryptographic mechanisms:
- IDEA algorithm in OFB mode for encryption and decryption.
- Elliptic Curve Diffie-Hellman (EC DH) for secure key generation.
- Schnorr signature scheme for digital signatures.

## Project Structure

- `main.py`: Main application file with PyQt6 GUI.
- `idea.py`: Implementation of the IDEA algorithm.
- `ecdh.py`: Implementation of EC DH key exchange.
- `schnorr.py`: Implementation of the Schnorr signature scheme.

## How to Run

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
