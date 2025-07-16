"""
Hill Cipher Demo Script
This script demonstrates the Hill Cipher with various examples
"""

import numpy as np
from cipher import HillCipher


def demo_basic_encryption():
    """
    Demonstrate basic Hill Cipher encryption and decryption.
    """
    print("🔐 Hill Cipher Demo")
    print("=" * 60)
    
    cipher = HillCipher()
    
    # Demo 1: Simple 2x2 example
    print("\n📝 Demo 1: 2x2 Key Matrix")
    print("-" * 40)
    
    key_matrix = np.array([[3, 2], [5, 7]])
    plaintext = "HELLO WORLD"
    
    print(f"Key Matrix:\n{key_matrix}")
    print(f"Plaintext: '{plaintext}'")
    
    # Show character mapping
    print("\nCharacter Mapping (A=0, B=1, ..., Z=25):")
    mapping = cipher.get_character_mapping()
    sample_chars = ['H', 'E', 'L', 'O', 'W', 'R', 'D']
    for char in sample_chars:
        print(f"{char} = {mapping[char]}", end="  ")
    print()
    
    # Encrypt
    ciphertext, encrypt_steps = cipher.encrypt(plaintext, key_matrix)
    print(f"\n🔒 Encrypted: '{ciphertext}'")
    
    # Show encryption steps
    print("\nEncryption Steps:")
    print(f"1. Text preprocessing: '{plaintext}' → '{encrypt_steps['padded_text']}'")
    print(f"2. Numerical conversion: {encrypt_steps['text_numbers']}")
    print(f"3. Block processing:")
    for i, (plain_block, cipher_block) in enumerate(zip(encrypt_steps['blocks'], encrypt_steps['encrypted_blocks'])):
        print(f"   Block {i+1}: {plain_block} → {cipher_block}")
    print(f"4. Final ciphertext: '{ciphertext}'")
    
    # Decrypt
    decrypted_text, decrypt_steps = cipher.decrypt(ciphertext, key_matrix)
    print(f"\n🔓 Decrypted: '{decrypted_text}'")
    
    # Show decryption steps
    print("\nDecryption Steps:")
    print(f"1. Inverse key matrix:\n{decrypt_steps['inverse_key_matrix']}")
    print(f"2. Block processing:")
    for i, (cipher_block, plain_block) in enumerate(zip(decrypt_steps['blocks'], decrypt_steps['decrypted_blocks'])):
        print(f"   Block {i+1}: {cipher_block} → {plain_block}")
    print(f"3. Final plaintext: '{decrypted_text}'")


def demo_3x3_encryption():
    """
    Demonstrate 3x3 Hill Cipher encryption.
    """
    print("\n\n📝 Demo 2: 3x3 Key Matrix")
    print("-" * 40)
    
    cipher = HillCipher()
    
    key_matrix = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
    plaintext = "MATHEMATICS"
    
    print(f"Key Matrix:\n{key_matrix}")
    print(f"Plaintext: '{plaintext}'")
    
    # Encrypt
    ciphertext, encrypt_steps = cipher.encrypt(plaintext, key_matrix)
    print(f"\n🔒 Encrypted: '{ciphertext}'")
    
    # Decrypt
    decrypted_text, decrypt_steps = cipher.decrypt(ciphertext, key_matrix)
    print(f"🔓 Decrypted: '{decrypted_text}'")
    
    # Show matrix operations
    print("\nMatrix Operations:")
    print(f"Original text blocks: {encrypt_steps['blocks']}")
    print(f"Encrypted blocks: {encrypt_steps['encrypted_blocks']}")
    print(f"Decrypted blocks: {decrypt_steps['decrypted_blocks']}")


def demo_key_validation():
    """
    Demonstrate key matrix validation.
    """
    print("\n\n📝 Demo 3: Key Matrix Validation")
    print("-" * 40)
    
    cipher = HillCipher()
    
    # Valid key matrix
    valid_key = np.array([[3, 2], [5, 7]])
    print(f"Valid key matrix:\n{valid_key}")
    print(f"Is valid: {cipher.is_valid_key_matrix(valid_key)}")
    
    # Invalid key matrix (not invertible mod 26)
    invalid_key = np.array([[2, 4], [6, 8]])
    print(f"\nInvalid key matrix:\n{invalid_key}")
    print(f"Is valid: {cipher.is_valid_key_matrix(invalid_key)}")
    
    # Show determinant calculation
    det_valid = int(np.round(np.linalg.det(valid_key)))
    det_invalid = int(np.round(np.linalg.det(invalid_key)))
    
    print(f"\nDeterminant calculations:")
    print(f"Valid key det: {det_valid}, gcd({det_valid % 26}, 26) = {np.gcd(det_valid % 26, 26)}")
    print(f"Invalid key det: {det_invalid}, gcd({det_invalid % 26}, 26) = {np.gcd(det_invalid % 26, 26)}")


def demo_random_key_generation():
    """
    Demonstrate random key generation.
    """
    print("\n\n📝 Demo 4: Random Key Generation")
    print("-" * 40)
    
    cipher = HillCipher()
    
    for size in [2, 3, 4]:
        print(f"\nGenerating {size}x{size} random key matrix:")
        random_key = cipher.generate_random_key_matrix(size)
        print(random_key)
        print(f"Valid: {cipher.is_valid_key_matrix(random_key)}")
        
        # Test with sample text
        if size == 2:
            test_text = "TEST"
            try:
                encrypted, _ = cipher.encrypt(test_text, random_key)
                decrypted, _ = cipher.decrypt(encrypted, random_key)
                print(f"Test: '{test_text}' → '{encrypted}' → '{decrypted}'")
            except Exception as e:
                print(f"Error: {e}")


def demo_edge_cases():
    """
    Demonstrate edge cases and error handling.
    """
    print("\n\n📝 Demo 5: Edge Cases")
    print("-" * 40)
    
    cipher = HillCipher()
    key_matrix = np.array([[3, 2], [5, 7]])
    
    # Empty text
    print("1. Empty text handling:")
    try:
        result, _ = cipher.encrypt("", key_matrix)
        print(f"   Empty text result: '{result}'")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Single character
    print("\n2. Single character:")
    result, _ = cipher.encrypt("A", key_matrix)
    decrypted, _ = cipher.decrypt(result, key_matrix)
    print(f"   'A' → '{result}' → '{decrypted}'")
    
    # Text with spaces and punctuation
    print("\n3. Text with spaces and punctuation:")
    messy_text = "Hello, World! 123"
    result, steps = cipher.encrypt(messy_text, key_matrix)
    print(f"   '{messy_text}' → cleaned: '{steps['padded_text']}'")
    print(f"   Encrypted: '{result}'")
    
    # Non-square matrix
    print("\n4. Non-square matrix:")
    non_square = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"   Matrix shape: {non_square.shape}")
    print(f"   Valid: {cipher.is_valid_key_matrix(non_square)}")


if __name__ == "__main__":
    demo_basic_encryption()
    demo_3x3_encryption()
    demo_key_validation()
    demo_random_key_generation()
    demo_edge_cases()
    
    print("\n\n🎉 All demos completed!")
    print("\nTo run the interactive Streamlit app:")
    print("streamlit run app.py")
