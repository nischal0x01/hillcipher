import numpy as np
from math import gcd

class HillCipher:
    def __init__(self, key_matrix):
        self.key_matrix = np.array(key_matrix)
        self.n = len(key_matrix)
        self.m = 26
        if not self._is_invertible():
            raise ValueError("Matrix not invertible mod 26")

    def _is_invertible(self):
        det = int(round(np.linalg.det(self.key_matrix))) % self.m
        return gcd(det, self.m) == 1

    def _modinv(self, a, m):
        g, x, _ = self._egcd(a % m, m)
        if g != 1: raise ValueError("No inverse")
        return x % m

    def _egcd(self, a, b):
        return (b, 0, 1) if a == 0 else (lambda g, x, y: (g, y - (b//a) * x, x))(*self._egcd(b % a, a))

    def _matrix_inv(self):
        det = int(round(np.linalg.det(self.key_matrix))) % self.m
        inv_det = self._modinv(det, self.m)
        adj = np.round(det * np.linalg.inv(self.key_matrix)).astype(int)
        return (inv_det * adj) % self.m

    def _text_to_nums(self, text):
        return [ord(c) - 65 for c in text.upper() if c.isalpha()]

    def _nums_to_text(self, nums):
        return ''.join(chr(n % self.m + 65) for n in nums)

    def _pad(self, nums):
        while len(nums) % self.n: nums.append(23)
        return nums

    def encrypt(self, text: str) -> str:
        text = text.upper().replace(" ", "")
        numbers = self._text_to_numbers(text)

        # 🔧 Pad with 'X' to fit block size
        if len(numbers) % self.n != 0:
            padding = self.n - len(numbers) % self.n
            numbers += [ord('X') - ord('A')] * padding

        blocks = np.array(numbers).reshape(-1, self.n)
        result = (blocks @ self.key_matrix.T) % 26
        return self._numbers_to_text(result.flatten())

    def decrypt(self, text):
        nums = self._text_to_nums(text)
        inv = self._matrix_inv()
        res = []
        for i in range(0, len(nums), self.n):
            res += (inv @ nums[i:i+self.n]) % self.m
        return self._nums_to_text(res)