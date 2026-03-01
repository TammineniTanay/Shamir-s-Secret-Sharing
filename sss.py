import secrets
from typing import List, Tuple

# We use a Mersenne Prime (2^127 - 1) for high security
PRIME = 2**127 - 1

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Helper for division in finite fields."""
    if a == 0: return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    return gcd, y1 - (b // a) * x1, x1

def mod_inverse(n: int, p: int) -> int:
    """Calculates the modular inverse."""
    _, x, _ = extended_gcd(n, p)
    return x % p

def create_shares(secret: int, threshold: int, total_shares: int) -> List[Tuple[int, int]]:
    """Splits a secret into N shares, requiring K to reconstruct."""
    if threshold > total_shares:
        raise ValueError("Error: Threshold cannot be higher than total shares.")
    
    # Randomly generate coefficients for the math
    coeffs = [secret] + [secrets.randbelow(PRIME) for _ in range(threshold - 1)]
    
    shares = []
    for x in range(1, total_shares + 1):
        y = sum(c * (x**i) for i, c in enumerate(coeffs)) % PRIME
        shares.append((x, y))
    return shares

def reconstruct_secret(shares: List[Tuple[int, int]]) -> int:
    """Uses Lagrange Interpolation to get the secret back."""
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        num, den = 1, 1
        for j, (xj, _) in enumerate(shares):
            if i == j: continue
            num = (num * -xj) % PRIME
            den = (den * (xi - xj)) % PRIME
        
        term = (yi * num * mod_inverse(den, PRIME)) % PRIME
        secret = (secret + term) % PRIME
    return secret

# --- TEST SECTION ---
if __name__ == "__main__":
    MY_SECRET = 987654321
    shares = create_shares(MY_SECRET, 3, 5)
    print(f"Shares created: {len(shares)}")
    recovered = reconstruct_secret(shares[:3])
    print(f"Original Secret: {MY_SECRET}")
    print(f"Recovered Secret: {recovered}")