#!/usr/bin/env python3

import sys

PRIME = 340282366920938463463374607431768211457

def modular_inverse(a, m):
    return pow(a, -1, m)

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} share1 share2 [share3...]", file=sys.stderr)
        sys.exit(1)

    shares_hex = sys.argv[1:]
    points = []

    for hex_share in shares_hex:
        try:
            share_bytes = bytes.fromhex(hex_share.replace(':', ''))
            
            if len(share_bytes) != 19:
                print(f"Error: Invalid share format for '{hex_share}'", file=sys.stderr)
                sys.exit(1)

            x = int.from_bytes(share_bytes[0:2], 'big')
            y = int.from_bytes(share_bytes[2:19], 'big')
            
            points.append((x, y))
        except ValueError:
            print(f"Error: Invalid hex characters in share '{hex_share}'", file=sys.stderr)
            sys.exit(1)

    secret = 0
    k = len(points)

    for i in range(k):
        xi, yi = points[i]
        
        numerator = 1
        denominator = 1
        
        for j in range(k):
            if i == j:
                continue
            xj, _ = points[j]
            
            numerator = (numerator * xj) % PRIME
            denominator = (denominator * (xj - xi)) % PRIME
        
        lagrange_poly = (numerator * modular_inverse(denominator, PRIME)) % PRIME
        
        secret = (secret + yi * lagrange_poly) % PRIME

    secret_bytes = secret.to_bytes(16, 'big')
    hex_output = ':'.join(f'{b:02X}' for b in secret_bytes)
    
    print(hex_output)


if __name__ == "__main__":
    main()
