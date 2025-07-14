"""
Hill Cipher Implementation
This module contains the core logic for Hill Cipher encryption and decryption
using numerical linear algebra operations.
"""

import numpy as np
from typing import List, Tuple, Optional
import math


class HillCipher:
    """
    Hill Cipher implementation with support for different key matrix sizes.
    Uses modulo 26 arithmetic for English alphabet.
    """
    
    def __init__(self, alphabet_size: int = 26):
        """
        Initialize Hill Cipher with specified alphabet size.
        
        Args:
            alphabet_size: Size of the alphabet (default: 26 for English)
        """
        self.alphabet_size = alphabet_size
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def text_to_numbers(self, text: str) -> List[int]:
        """
        Convert text to list of numbers (A=0, B=1, ..., Z=25).
        
        Args:
            text: Input text string
            
        Returns:
            List of integers representing the text
        """
        text = text.upper().replace(' ', '')
        # Keep only alphabetic characters
        text = ''.join(char for char in text if char.isalpha())
        return [ord(char) - ord('A') for char in text]
    
    def numbers_to_text(self, numbers: List[int]) -> str:
        """
        Convert list of numbers back to text.
        
        Args:
            numbers: List of integers
            
        Returns:
            Text string
        """
        return ''.join(chr(num + ord('A')) for num in numbers)
    
    def pad_text(self, text: str, block_size: int) -> str:
        """
        Pad text to make it divisible by block size.
        
        Args:
            text: Input text
            block_size: Size of cipher blocks
            
        Returns:
            Padded text
        """
        while len(text) % block_size != 0:
            text += 'X'
        return text
    
    def create_text_blocks(self, numbers: List[int], block_size: int) -> List[np.ndarray]:
        """
        Create blocks of text for matrix operations.
        
        Args:
            numbers: List of numbers representing text
            block_size: Size of each block
            
        Returns:
            List of numpy arrays representing text blocks
        """
        blocks = []
        for i in range(0, len(numbers), block_size):
            block = numbers[i:i + block_size]
            # Ensure block has correct size
            if len(block) == block_size:
                blocks.append(np.array(block).reshape(-1, 1))
        return blocks
    
    def gcd_extended(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm to find gcd and coefficients.
        
        Args:
            a, b: Input integers
            
        Returns:
            Tuple of (gcd, x, y) where ax + by = gcd
        """
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.gcd_extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def mod_inverse(self, a: int, m: int) -> Optional[int]:
        """
        Calculate modular inverse of a modulo m.
        
        Args:
            a: Number to find inverse of
            m: Modulus
            
        Returns:
            Modular inverse if exists, None otherwise
        """
        gcd, x, _ = self.gcd_extended(a, m)
        if gcd != 1:
            return None
        return (x % m + m) % m
    
    def matrix_mod_inverse(self, matrix: np.ndarray) -> Optional[np.ndarray]:
        """
        Calculate modular inverse of a matrix modulo alphabet_size.
        
        Args:
            matrix: Input matrix
            
        Returns:
            Inverse matrix if exists, None otherwise
        """
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = self.mod_inverse(det, self.alphabet_size)
        
        if det_inv is None:
            return None
        
        # Calculate adjugate matrix
        if matrix.shape[0] == 2:
            adj = np.array([[matrix[1, 1], -matrix[0, 1]], 
                           [-matrix[1, 0], matrix[0, 0]]])
        else:
            # For larger matrices, use numpy's inverse and scale
            try:
                adj = np.linalg.inv(matrix) * det
                adj = np.round(adj).astype(int)
            except:
                return None
        
        # Calculate modular inverse
        inv_matrix = (det_inv * adj) % self.alphabet_size
        return inv_matrix.astype(int)
    
    def is_valid_key_matrix(self, key_matrix: np.ndarray) -> bool:
        """
        Check if key matrix is valid (invertible mod 26).
        
        Args:
            key_matrix: Key matrix to validate
            
        Returns:
            True if valid, False otherwise
        """
        if key_matrix.shape[0] != key_matrix.shape[1]:
            return False
        
        det = int(np.round(np.linalg.det(key_matrix)))
        det_mod = det % self.alphabet_size
        
        return math.gcd(det_mod, self.alphabet_size) == 1
    
    def encrypt(self, plaintext: str, key_matrix: np.ndarray) -> Tuple[str, dict]:
        """
        Encrypt plaintext using Hill Cipher.
        
        Args:
            plaintext: Text to encrypt
            key_matrix: Encryption key matrix
            
        Returns:
            Tuple of (ciphertext, steps_info)
        """
        if not self.is_valid_key_matrix(key_matrix):
            raise ValueError("Invalid key matrix: not invertible mod 26")
        
        block_size = key_matrix.shape[0]
        
        # Store original text before padding
        original_text = plaintext
        
        # Prepare text
        plaintext = self.pad_text(plaintext, block_size)
        numbers = self.text_to_numbers(plaintext)
        blocks = self.create_text_blocks(numbers, block_size)
        
        # Encryption steps info
        steps_info = {
            'original_text': original_text,
            'padded_text': plaintext,
            'text_numbers': numbers,
            'key_matrix': key_matrix,
            'blocks': [],
            'encrypted_blocks': [],
            'final_numbers': [],
            'ciphertext': ''
        }
        
        encrypted_numbers = []
        
        for i, block in enumerate(blocks):
            # Matrix multiplication
            encrypted_block = np.dot(key_matrix, block) % self.alphabet_size
            encrypted_numbers.extend(encrypted_block.flatten())
            
            # Store step info
            steps_info['blocks'].append(block.flatten())
            steps_info['encrypted_blocks'].append(encrypted_block.flatten())
        
        steps_info['final_numbers'] = encrypted_numbers
        ciphertext = self.numbers_to_text(encrypted_numbers)
        steps_info['ciphertext'] = ciphertext
        
        return ciphertext, steps_info
    
    def decrypt(self, ciphertext: str, key_matrix: np.ndarray) -> Tuple[str, dict]:
        """
        Decrypt ciphertext using Hill Cipher.
        
        Args:
            ciphertext: Text to decrypt
            key_matrix: Decryption key matrix
            
        Returns:
            Tuple of (plaintext, steps_info)
        """
        if not self.is_valid_key_matrix(key_matrix):
            raise ValueError("Invalid key matrix: not invertible mod 26")
        
        # Calculate inverse key matrix
        inv_key_matrix = self.matrix_mod_inverse(key_matrix)
        if inv_key_matrix is None:
            raise ValueError("Cannot find inverse of key matrix")
        
        block_size = key_matrix.shape[0]
        
        # Prepare text
        numbers = self.text_to_numbers(ciphertext)
        blocks = self.create_text_blocks(numbers, block_size)
        
        # Decryption steps info
        steps_info = {
            'ciphertext': ciphertext,
            'cipher_numbers': numbers,
            'key_matrix': key_matrix,
            'inverse_key_matrix': inv_key_matrix,
            'blocks': [],
            'decrypted_blocks': [],
            'final_numbers': [],
            'plaintext': ''
        }
        
        decrypted_numbers = []
        
        for i, block in enumerate(blocks):
            # Matrix multiplication with inverse
            decrypted_block = np.dot(inv_key_matrix, block) % self.alphabet_size
            decrypted_numbers.extend(decrypted_block.flatten())
            
            # Store step info
            steps_info['blocks'].append(block.flatten())
            steps_info['decrypted_blocks'].append(decrypted_block.flatten())
        
        steps_info['final_numbers'] = decrypted_numbers
        plaintext = self.numbers_to_text(decrypted_numbers)
        steps_info['plaintext'] = plaintext
        
        return plaintext, steps_info
    
    def generate_random_key_matrix(self, size: int) -> np.ndarray:
        """
        Generate a random valid key matrix of given size.
        
        Args:
            size: Size of the square matrix
            
        Returns:
            Valid key matrix
        """
        max_attempts = 100
        for _ in range(max_attempts):
            matrix = np.random.randint(0, self.alphabet_size, (size, size))
            if self.is_valid_key_matrix(matrix):
                return matrix
        
        # Fallback: create a simple valid matrix
        if size == 2:
            return np.array([[3, 2], [5, 7]])
        elif size == 3:
            return np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
        else:
            # For larger sizes, create identity-like matrix with some modifications
            matrix = np.eye(size, dtype=int)
            matrix[0, 0] = 3
            matrix[1, 1] = 5
            return matrix
    
    def get_character_mapping(self) -> dict:
        """
        Get character to number mapping.
        
        Returns:
            Dictionary mapping characters to numbers
        """
        return {chr(i + ord('A')): i for i in range(26)}


def demo_hill_cipher():
    """
    Demonstration of Hill Cipher functionality.
    """
    cipher = HillCipher()
    
    # Example with 2x2 key matrix
    key_matrix = np.array([[3, 2], [5, 7]])
    plaintext = "HELLO"
    
    print("Hill Cipher Demonstration")
    print("=" * 50)
    print(f"Key Matrix:\n{key_matrix}")
    print(f"Plaintext: {plaintext}")
    
    # Encrypt
    ciphertext, encrypt_steps = cipher.encrypt(plaintext, key_matrix)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt
    decrypted_text, decrypt_steps = cipher.decrypt(ciphertext, key_matrix)
    print(f"Decrypted: {decrypted_text}")
    
    # Show character mapping
    print("\nCharacter Mapping:")
    mapping = cipher.get_character_mapping()
    for char, num in list(mapping.items())[:10]:  # Show first 10
        print(f"{char} = {num}")
    print("...")


if __name__ == "__main__":
    demo_hill_cipher()
