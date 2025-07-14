# Hill Cipher Application

A Python implementation of the Hill Cipher encryption/decryption algorithm with a Streamlit web interface. Demonstrates numerical linear algebra operations including matrix multiplication, modular arithmetic, and matrix inversion.

## Features

- **Hill Cipher Implementation**: Encrypt/decrypt text using 2x2, 3x3, or 4x4 key matrices
- **Matrix Operations**: NumPy-based matrix computations with mod 26 arithmetic
- **Interactive Web UI**: Clean Streamlit interface with step-by-step visualizations
- **Key Validation**: Automatically validates key matrices (must be invertible mod 26)
- **Visual Steps**: Shows matrix operations and numerical transformations

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the web app:**
```bash
streamlit run app.py
```

3. **Use the interface:**
   - Enter text to encrypt/decrypt
   - Set a key matrix (or generate random)
   - View results with step-by-step matrix operations

## Files

- `cipher.py` - Core Hill Cipher implementation
- `app.py` - Streamlit web interface  
- `requirements.txt` - Python dependencies

## Hill Cipher Algorithm

**Encryption**: C = K × P (mod 26)  
**Decryption**: P = K⁻¹ × C (mod 26)

Where K is the key matrix, P is plaintext vector, C is ciphertext vector.

### Example
```python
from cipher import HillCipher
import numpy as np

cipher = HillCipher()
key = np.array([[3, 2], [5, 7]])

encrypted, _ = cipher.encrypt("HELLO", key)
decrypted, _ = cipher.decrypt(encrypted, key)

print(f"HELLO → {encrypted} → {decrypted}")
# Output: HELLO → DLDCKX → HELLOX
```

The implementation handles:
- Matrix validation (must be invertible mod 26)
- Text preprocessing (uppercase, remove spaces)
- Automatic padding with 'X'
- Step-by-step visualization of matrix operations
