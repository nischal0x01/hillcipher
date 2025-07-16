"""
Test file for Hill Cipher implementation
"""

import numpy as np
from cipher import HillCipher


def test_hill_cipher():
    """
    Test basic Hill Cipher functionality.
    """
    print("Testing Hill Cipher Implementation")
    print("=" * 50)
    
    cipher = HillCipher()
    
    # Test 1: Basic encryption/decryption with 2x2 matrix
    print("\nTest 1: 2x2 Key Matrix")
    key_matrix_2x2 = np.array([[3, 2], [5, 7]])
    plaintext = "HELLO"
    
    print(f"Key Matrix:\n{key_matrix_2x2}")
    print(f"Plaintext: {plaintext}")
    
    # Test if key matrix is valid
    is_valid = cipher.is_valid_key_matrix(key_matrix_2x2)
    print(f"Key matrix valid: {is_valid}")
    
    if is_valid:
        # Encrypt
        ciphertext, encrypt_steps = cipher.encrypt(plaintext, key_matrix_2x2)
        print(f"Ciphertext: {ciphertext}")
        
        # Decrypt
        decrypted_text, decrypt_steps = cipher.decrypt(ciphertext, key_matrix_2x2)
        print(f"Decrypted: {decrypted_text}")
        
        # Verify
        original_cleaned = plaintext.upper().replace(' ', '')
        decrypted_cleaned = decrypted_text.rstrip('X')  # Remove padding
        print(f"Test 1 Result: {'PASS' if original_cleaned == decrypted_cleaned else 'FAIL'}")
    
    # Test 2: 3x3 key matrix
    print("\nTest 2: 3x3 Key Matrix")
    key_matrix_3x3 = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
    plaintext = "MATHEMATICS"
    
    print(f"Key Matrix:\n{key_matrix_3x3}")
    print(f"Plaintext: {plaintext}")
    
    is_valid = cipher.is_valid_key_matrix(key_matrix_3x3)
    print(f"Key matrix valid: {is_valid}")
    
    if is_valid:
        ciphertext, _ = cipher.encrypt(plaintext, key_matrix_3x3)
        print(f"Ciphertext: {ciphertext}")
        
        decrypted_text, _ = cipher.decrypt(ciphertext, key_matrix_3x3)
        print(f"Decrypted: {decrypted_text}")
        
        # Verify
        original_cleaned = plaintext.upper().replace(' ', '')
        decrypted_cleaned = decrypted_text.rstrip('X')
        print(f"Test 2 Result: {'PASS' if original_cleaned == decrypted_cleaned else 'FAIL'}")
    
    # Test 3: Invalid key matrix
    print("\nTest 3: Invalid Key Matrix")
    invalid_key = np.array([[2, 4], [6, 8]])  # Not invertible mod 26
    print(f"Invalid Key Matrix:\n{invalid_key}")
    
    is_valid = cipher.is_valid_key_matrix(invalid_key)
    print(f"Key matrix valid: {is_valid}")
    print(f"Test 3 Result: {'PASS' if not is_valid else 'FAIL'}")
    
    # Test 4: Random key generation
    print("\nTest 4: Random Key Generation")
    for size in [2, 3, 4]:
        random_key = cipher.generate_random_key_matrix(size)
        is_valid = cipher.is_valid_key_matrix(random_key)
        print(f"Random {size}x{size} key matrix valid: {is_valid}")
    
    # Test 5: Character mapping
    print("\nTest 5: Character Mapping")
    mapping = cipher.get_character_mapping()
    print(f"A = {mapping['A']}, Z = {mapping['Z']}")
    print(f"Character mapping test: {'PASS' if mapping['A'] == 0 and mapping['Z'] == 25 else 'FAIL'}")
    
    print("\nAll tests completed!")


if __name__ == "__main__":
    test_hill_cipher()
