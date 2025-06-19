#!/usr/bin/env python3

import sys
import secrets

PRIME = 340282366920938463463374607431768211457

def main():
    if len(sys.argv) != 4:
        print(f"Usage {sys.argv[0]} m n secret", file=sys.stderr)
        sys.exit(1)

    hex_string = sys.argv[3]

    try:
        m = int(sys.argv[1])
        n = int(sys.argv[2])
    except ValueError:
        print("Error: m and n must be integers.", file=sys.stderr)
        sys.exit(1)

    try:
        byte_data = bytes.fromhex(hex_string.replace(':', ''))
        secret_int = int.from_bytes(byte_data, 'big')
    except ValueError:
        print("Error: Invalid secret hex format.", file=sys.stderr)
        sys.exit(1)

    coefficients = [secret_int]
    for number in range(n - 1):
        random_num = secrets.randbelow(PRIME)
        coefficients.append(random_num)

    shares = []
    for x in range(1, m + 1):
        y = 0
        for exp, coeff in enumerate(coefficients):
            y += coeff * (x ** exp)
        y %= PRIME     
        shares.append((x, y))

    for x, y in shares:
        x_bytes = x.to_bytes(2, 'big')
        y_bytes = y.to_bytes(17, 'big')

        share_bytes = x_bytes + y_bytes # Unimos los bytes
    
        hex_string = ':'.join(f'{b:02X}' for b in share_bytes)
        print(hex_string)

if __name__ == "__main__":
    main()



