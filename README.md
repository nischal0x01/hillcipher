# Hill Cipher - Encryption & Decryption

A simple Python implementation of the Hill Cipher with a web interface to encrypt and decrypt text using matrix operations.

## What You Get

- **Encrypt/Decrypt text** using Hill Cipher algorithm
- **Web interface** to input text and key matrices
- **Visual step-by-step** matrix operations
- **Supports 2x2, 3x3, and 4x4** key matrices

## Quick Setup

1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd hillcipher
   ```

2. **Install Python packages**
   ```bash
   pip install numpy streamlit
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** - it will automatically open at `http://localhost:8501`

## How to Use

1. **Enter your text** in the input box
2. **Choose operation**: Encrypt or Decrypt
3. **Set key matrix**: Enter numbers or click "Generate Random Key Matrix"
4. **View results** with step-by-step matrix operations

## Example

```python
# You can also use it directly in Python
from cipher import HillCipher
import numpy as np

cipher = HillCipher()
key = np.array([[3, 2], [5, 7]])

# Encrypt
encrypted, _ = cipher.encrypt("HELLO", key)
print(f"Encrypted: {encrypted}")  # Output: DLDCKX

# Decrypt
decrypted, _ = cipher.decrypt(encrypted, key)
print(f"Decrypted: {decrypted}")  # Output: HELLOX
```

## Files

- `cipher.py` - Hill Cipher implementation
- `app.py` - Streamlit web interface
- `requirements.txt` - Python dependencies

## Troubleshooting

- **ModuleNotFoundError**: Run `pip install numpy streamlit`
- **Port already in use**: Try `streamlit run app.py --server.port 8502`
- **Matrix not invertible**: The key matrix must be invertible mod 26

That's it! 🎉
