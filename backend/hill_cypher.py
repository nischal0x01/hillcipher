import numpy as np
from math import gcd

class HillCipher:
    def __init__(self, key_matrix):
        """
        Initialize Hill Cipher with a key matrix
        key_matrix: 2x2 or 3x3 numpy array representing the encryption key
        """
        self.key_matrix = np.array(key_matrix)
        self.n = len(key_matrix)  # Matrix size (2x2 or 3x3)
        self.alphabet_size = 26
        
        # Verify key matrix is invertible mod 26
        if not self._is_invertible():
            raise ValueError("Key matrix is not invertible modulo 26")
    
    def _is_invertible(self):
        """Check if matrix is invertible modulo 26"""
        det = int(np.round(np.linalg.det(self.key_matrix))) % self.alphabet_size
        return gcd(det, self.alphabet_size) == 1
    
    def _text_to_numbers(self, text):
        """Convert text to numbers (A=0, B=1, ..., Z=25)"""
        text = text.upper().replace(' ', '')
        return [ord(char) - ord('A') for char in text if char.isalpha()]
    
    def _numbers_to_text(self, numbers):
        """Convert numbers back to text"""
        return ''.join([chr(num + ord('A')) for num in numbers])
    
    def _pad_text(self, numbers):
        """Pad text to make it divisible by matrix size"""
        while len(numbers) % self.n != 0:
            numbers.append(23)  # Padding with 'X'
        return numbers
    
    def _matrix_mod_inverse(self, matrix, mod):
        """Calculate modular inverse of matrix"""
        det = int(np.round(np.linalg.det(matrix))) % mod
        det_inv = self._mod_inverse(det, mod)
        
        if self.n == 2:
            # For 2x2 matrix: inverse = (1/det) * [[d, -b], [-c, a]]
            a, b, c, d = matrix[0,0], matrix[0,1], matrix[1,0], matrix[1,1]
            inv_matrix = np.array([[d, -b], [-c, a]])
        else:
            # For 3x3 matrix: use adjugate matrix
            inv_matrix = np.linalg.inv(matrix) * np.linalg.det(matrix)
        
        return (det_inv * inv_matrix) % mod
    
    def _mod_inverse(self, a, m):
        """Calculate modular multiplicative inverse using Extended Euclidean Algorithm"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using Hill Cipher"""
        # Convert text to numbers and pad
        numbers = self._text_to_numbers(plaintext)
        numbers = self._pad_text(numbers)
        
        # Split into blocks and encrypt
        encrypted_numbers = []
        for i in range(0, len(numbers), self.n):
            block = np.array(numbers[i:i+self.n])
            encrypted_block = (self.key_matrix @ block) % self.alphabet_size
            encrypted_numbers.extend(encrypted_block.astype(int))
        
        return self._numbers_to_text(encrypted_numbers)
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext using Hill Cipher"""
        # Calculate inverse key matrix
        inverse_key = self._matrix_mod_inverse(self.key_matrix, self.alphabet_size)
        
        # Convert text to numbers
        numbers = self._text_to_numbers(ciphertext)
        
        # Split into blocks and decrypt
        decrypted_numbers = []
        for i in range(0, len(numbers), self.n):
            block = np.array(numbers[i:i+self.n])
            decrypted_block = (inverse_key @ block) % self.alphabet_size
            decrypted_numbers.extend(decrypted_block.astype(int))
        
        return self._numbers_to_text(decrypted_numbers)

# Example usage and testing
def main():
    # Example 1: 2x2 Hill Cipher
    print("=== 2x2 Hill Cipher Example ===")
    key_2x2 = [[3, 2], [5, 7]]
    hill_2x2 = HillCipher(key_2x2)
    
    plaintext = "HELLO WORLD"
    print(f"Original text: {plaintext}")
    
    encrypted = hill_2x2.encrypt(plaintext)
    print(f"Encrypted: {encrypted}")
    
    decrypted = hill_2x2.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: 3x3 Hill Cipher
    print("=== 3x3 Hill Cipher Example ===")
    key_3x3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    hill_3x3 = HillCipher(key_3x3)
    
    plaintext2 = "CRYPTOGRAPHY"
    print(f"Original text: {plaintext2}")
    
    encrypted2 = hill_3x3.encrypt(plaintext2)
    print(f"Encrypted: {encrypted2}")
    
    decrypted2 = hill_3x3.decrypt(encrypted2)
    print(f"Decrypted: {decrypted2}")

# Key matrix validation function
def validate_key_matrix(matrix):
    """Validate if a matrix can be used as Hill Cipher key"""
    try:
        hill = HillCipher(matrix)
        return True, "Valid key matrix"
    except ValueError as e:
        return False, str(e)

# Generate random valid key matrix
def generate_random_key(size=2):
    """Generate a random valid key matrix for Hill Cipher"""
    import random
    
    while True:
        matrix = [[random.randint(0, 25) for _ in range(size)] for _ in range(size)]
        is_valid, _ = validate_key_matrix(matrix)
        if is_valid:
            return matrix

if __name__ == "__main__":
    main()
    
    # Test with random key
    print("\n=== Random Key Test ===")
    random_key = generate_random_key(2)
    print(f"Random 2x2 key: {random_key}")
    
    hill_random = HillCipher(random_key)
    test_text = "NUMERICAL LINEAR ALGEBRA"
    encrypted_random = hill_random.encrypt(test_text)
    decrypted_random = hill_random.decrypt(encrypted_random)
    
    print(f"Original: {test_text}")
    print(f"Encrypted: {encrypted_random}")
    print(f"Decrypted: {decrypted_random}")