"""
Integration test for the complete Hill Cipher application
"""

import numpy as np
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cipher import HillCipher


def test_complete_workflow():
    """
    Test the complete workflow from encryption to decryption
    """
    print("🧪 Hill Cipher Integration Test")
    print("=" * 50)
    
    cipher = HillCipher()
    
    # Test cases with different matrix sizes and texts
    test_cases = [
        {
            'name': 'Basic 2x2 Test',
            'key_matrix': np.array([[3, 2], [5, 7]]),
            'plaintext': 'HELLO',
            'expected_length': 6  # HELLO -> HELLOX (padded)
        },
        {
            'name': 'Long Text 2x2 Test',
            'key_matrix': np.array([[9, 4], [5, 7]]),
            'plaintext': 'THISISALONGMESSAGE',
            'expected_length': 18  # Should be exactly divisible by 2
        },
        {
            'name': '3x3 Matrix Test',
            'key_matrix': np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]]),
            'plaintext': 'MATHEMATICS',
            'expected_length': 12  # MATHEMATICS -> MATHEMATICSX (11 + 1 padding)
        },
        {
            'name': 'Text with Spaces',
            'key_matrix': np.array([[3, 2], [5, 7]]),
            'plaintext': 'HELLO WORLD',
            'expected_length': 12  # HELLOWORLD -> HELLOWORLDX (11 + 1 padding)
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            # Test encryption
            plaintext = test_case['plaintext']
            key_matrix = test_case['key_matrix']
            
            print(f"Plaintext: '{plaintext}'")
            print(f"Key Matrix:\n{key_matrix}")
            
            # Validate key matrix
            if not cipher.is_valid_key_matrix(key_matrix):
                print("❌ FAIL: Invalid key matrix")
                all_passed = False
                continue
            
            # Encrypt
            ciphertext, encrypt_steps = cipher.encrypt(plaintext, key_matrix)
            print(f"Encrypted: '{ciphertext}'")
            
            # Verify encryption steps
            if len(encrypt_steps['final_numbers']) != len(ciphertext):
                print("❌ FAIL: Encryption steps inconsistent")
                all_passed = False
                continue
            
            # Decrypt
            decrypted, decrypt_steps = cipher.decrypt(ciphertext, key_matrix)
            print(f"Decrypted: '{decrypted}'")
            
            # Verify decryption
            original_clean = plaintext.upper().replace(' ', '')
            decrypted_clean = decrypted.rstrip('X')
            
            if original_clean == decrypted_clean:
                print("✅ PASS: Encryption/Decryption successful")
            else:
                print(f"❌ FAIL: Original '{original_clean}' != Decrypted '{decrypted_clean}'")
                all_passed = False
            
            # Verify matrix operations
            if 'inverse_key_matrix' in decrypt_steps:
                # Test that K * K^-1 = I (mod 26)
                inv_key = decrypt_steps['inverse_key_matrix']
                identity_check = np.dot(key_matrix, inv_key) % 26
                expected_identity = np.eye(key_matrix.shape[0], dtype=int)
                
                if np.allclose(identity_check, expected_identity):
                    print("✅ PASS: Matrix inverse verification")
                else:
                    print("❌ FAIL: Matrix inverse verification")
                    all_passed = False
            
        except Exception as e:
            print(f"❌ FAIL: Exception occurred: {e}")
            all_passed = False
    
    # Test random key generation
    print(f"\n🔍 Test {len(test_cases) + 1}: Random Key Generation")
    print("-" * 30)
    
    try:
        for size in [2, 3, 4]:
            random_key = cipher.generate_random_key_matrix(size)
            is_valid = cipher.is_valid_key_matrix(random_key)
            
            if is_valid:
                print(f"✅ PASS: Valid {size}x{size} random key generated")
            else:
                print(f"❌ FAIL: Invalid {size}x{size} random key generated")
                all_passed = False
    except Exception as e:
        print(f"❌ FAIL: Random key generation failed: {e}")
        all_passed = False
    
    # Test error handling
    print(f"\n🔍 Test {len(test_cases) + 2}: Error Handling")
    print("-" * 30)
    
    try:
        # Test invalid key matrix
        invalid_key = np.array([[2, 4], [6, 8]])
        try:
            cipher.encrypt("TEST", invalid_key)
            print("❌ FAIL: Should have raised exception for invalid key")
            all_passed = False
        except ValueError:
            print("✅ PASS: Correctly rejected invalid key matrix")
        
        # Test non-square matrix
        non_square = np.array([[1, 2, 3], [4, 5, 6]])
        if not cipher.is_valid_key_matrix(non_square):
            print("✅ PASS: Correctly rejected non-square matrix")
        else:
            print("❌ FAIL: Should have rejected non-square matrix")
            all_passed = False
    
    except Exception as e:
        print(f"❌ FAIL: Error handling test failed: {e}")
        all_passed = False
    
    # Final result
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 ALL TESTS PASSED! Hill Cipher implementation is working correctly.")
        print("\nThe application is ready to use:")
        print("• Run 'python demo.py' for a demonstration")
        print("• Run 'streamlit run app.py' for the web interface")
        print("• Use 'from cipher import HillCipher' to import the module")
    else:
        print("❌ SOME TESTS FAILED! Please check the implementation.")
    
    return all_passed


if __name__ == "__main__":
    test_complete_workflow()
