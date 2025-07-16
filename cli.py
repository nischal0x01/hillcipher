#!/usr/bin/env python3
"""
Command Line Interface for Hill Cipher
"""

import argparse
import numpy as np
import sys
import json
from cipher import HillCipher


def parse_matrix(matrix_str):
    """
    Parse matrix string into numpy array
    Format: "[[1,2],[3,4]]" or "1,2;3,4"
    """
    try:
        if matrix_str.startswith('['):
            # JSON format
            return np.array(json.loads(matrix_str))
        else:
            # Semicolon format
            rows = matrix_str.split(';')
            matrix = []
            for row in rows:
                matrix.append([int(x.strip()) for x in row.split(',')])
            return np.array(matrix)
    except:
        raise ValueError("Invalid matrix format. Use '[[1,2],[3,4]]' or '1,2;3,4'")


def main():
    """
    Main CLI function
    """
    parser = argparse.ArgumentParser(description='Hill Cipher CLI')
    parser.add_argument('operation', choices=['encrypt', 'decrypt', 'validate', 'generate'], 
                       help='Operation to perform')
    parser.add_argument('--text', '-t', help='Text to encrypt/decrypt')
    parser.add_argument('--key', '-k', help='Key matrix (format: "[[1,2],[3,4]]" or "1,2;3,4")')
    parser.add_argument('--size', '-s', type=int, default=2, 
                       help='Size for random key generation (default: 2)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Show detailed steps')
    
    args = parser.parse_args()
    
    cipher = HillCipher()
    
    if args.operation == 'generate':
        # Generate random key matrix
        key_matrix = cipher.generate_random_key_matrix(args.size)
        print(f"Generated {args.size}x{args.size} key matrix:")
        print(key_matrix)
        print(f"Valid: {cipher.is_valid_key_matrix(key_matrix)}")
        return
    
    if args.operation == 'validate':
        if not args.key:
            print("Error: Key matrix required for validation")
            return
        
        key_matrix = parse_matrix(args.key)
        is_valid = cipher.is_valid_key_matrix(key_matrix)
        
        print(f"Key matrix:\n{key_matrix}")
        print(f"Valid: {is_valid}")
        
        if not is_valid:
            det = int(np.round(np.linalg.det(key_matrix)))
            print(f"Determinant: {det}")
            print(f"Determinant mod 26: {det % 26}")
            print(f"GCD(det mod 26, 26): {np.gcd(det % 26, 26)}")
        return
    
    # Encrypt or decrypt
    if not args.text or not args.key:
        print("Error: Both text and key matrix are required")
        return
    
    try:
        text = args.text
        key_matrix = parse_matrix(args.key)
        
        if not cipher.is_valid_key_matrix(key_matrix):
            print("Error: Invalid key matrix (not invertible mod 26)")
            return
        
        if args.operation == 'encrypt':
            result, steps = cipher.encrypt(text, key_matrix)
            print(f"Plaintext: '{text}'")
            print(f"Ciphertext: '{result}'")
            
            if args.verbose:
                print(f"\nDetailed steps:")
                print(f"Original: '{steps['original_text']}'")
                print(f"Padded: '{steps['padded_text']}'")
                print(f"Numbers: {steps['text_numbers']}")
                print(f"Blocks: {steps['blocks']}")
                print(f"Encrypted blocks: {steps['encrypted_blocks']}")
        
        elif args.operation == 'decrypt':
            result, steps = cipher.decrypt(text, key_matrix)
            print(f"Ciphertext: '{text}'")
            print(f"Plaintext: '{result}'")
            
            if args.verbose:
                print(f"\nDetailed steps:")
                print(f"Inverse key matrix:\n{steps['inverse_key_matrix']}")
                print(f"Numbers: {steps['cipher_numbers']}")
                print(f"Blocks: {steps['blocks']}")
                print(f"Decrypted blocks: {steps['decrypted_blocks']}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
