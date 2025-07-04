import React, { useState, useEffect } from 'react';
import { Lock, Unlock, Key, AlertCircle, CheckCircle, RefreshCw } from 'lucide-react';

const HillCipherApp = () => {
  const [keyMatrix, setKeyMatrix] = useState([[3, 2], [5, 7]]);
  const [matrixSize, setMatrixSize] = useState(2);
  const [plaintext, setPlaintext] = useState('');
  const [ciphertext, setCiphertext] = useState('');
  const [encryptedResult, setEncryptedResult] = useState('');
  const [decryptedResult, setDecryptedResult] = useState('');
  const [isValidKey, setIsValidKey] = useState(true);
  const [keyError, setKeyError] = useState('');
  const [activeTab, setActiveTab] = useState('encrypt');

  // Hill Cipher Implementation
  const gcd = (a, b) => {
    while (b !== 0) {
      const temp = b;
      b = a % b;
      a = temp;
    }
    return a;
  };

  const modInverse = (a, m) => {
    const extendedGcd = (a, b) => {
      if (a === 0) return [b, 0, 1];
      const [gcd, x1, y1] = extendedGcd(b % a, a);
      const x = y1 - Math.floor(b / a) * x1;
      const y = x1;
      return [gcd, x, y];
    };

    const [gcd, x] = extendedGcd(((a % m) + m) % m, m);
    if (gcd !== 1) throw new Error('Modular inverse does not exist');
    return ((x % m) + m) % m;
  };

  const determinant = (matrix) => {
    const n = matrix.length;
    if (n === 2) {
      return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
    } else if (n === 3) {
      return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
        matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
        matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
      );
    }
    return 0;
  };

  const matrixInverse = (matrix) => {
    const n = matrix.length;
    const det = ((determinant(matrix) % 26) + 26) % 26;
    const detInv = modInverse(det, 26);

    if (n === 2) {
      const [[a, b], [c, d]] = matrix;
      const invMatrix = [[d, -b], [-c, a]];
      return invMatrix.map(row => 
        row.map(val => (((detInv * val) % 26) + 26) % 26)
      );
    } else if (n === 3) {
      const adjugate = [
        [
          matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1],
          -(matrix[0][1] * matrix[2][2] - matrix[0][2] * matrix[2][1]),
          matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]
        ],
        [
          -(matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]),
          matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0],
          -(matrix[0][0] * matrix[1][2] - matrix[0][2] * matrix[1][0])
        ],
        [
          matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0],
          -(matrix[0][0] * matrix[2][1] - matrix[0][1] * matrix[2][0]),
          matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        ]
      ];
      return adjugate.map(row => 
        row.map(val => (((detInv * val) % 26) + 26) % 26)
      );
    }
    return matrix;
  };

  const textToNumbers = (text) => {
    return text.toUpperCase().replace(/[^A-Z]/g, '').split('').map(c => c.charCodeAt(0) - 65);
  };

  const numbersToText = (numbers) => {
    return numbers.map(n => String.fromCharCode(n + 65)).join('');
  };

  const padText = (numbers, size) => {
    while (numbers.length % size !== 0) {
      numbers.push(23); // X
    }
    return numbers;
  };

  const matrixMultiply = (matrix, vector) => {
    return matrix.map(row => 
      row.reduce((sum, val, i) => sum + val * vector[i], 0) % 26
    );
  };

  const validateKeyMatrix = (matrix) => {
    try {
      const det = ((determinant(matrix) % 26) + 26) % 26;
      if (gcd(det, 26) !== 1) {
        throw new Error('Matrix determinant and 26 are not coprime');
      }
      return { valid: true, error: '' };
    } catch (error) {
      return { valid: false, error: error.message };
    }
  };

  const encryptText = (text, matrix) => {
    const numbers = textToNumbers(text);
    const paddedNumbers = padText([...numbers], matrix.length);
    const encrypted = [];

    for (let i = 0; i < paddedNumbers.length; i += matrix.length) {
      const block = paddedNumbers.slice(i, i + matrix.length);
      const encryptedBlock = matrixMultiply(matrix, block);
      encrypted.push(...encryptedBlock);
    }

    return numbersToText(encrypted);
  };

  const decryptText = (text, matrix) => {
    const invMatrix = matrixInverse(matrix);
    const numbers = textToNumbers(text);
    const decrypted = [];

    for (let i = 0; i < numbers.length; i += matrix.length) {
      const block = numbers.slice(i, i + matrix.length);
      const decryptedBlock = matrixMultiply(invMatrix, block);
      decrypted.push(...decryptedBlock);
    }

    return numbersToText(decrypted);
  };

  const generateRandomKey = () => {
    const newMatrix = Array(matrixSize).fill().map(() => 
      Array(matrixSize).fill().map(() => Math.floor(Math.random() * 26))
    );
    
    const validation = validateKeyMatrix(newMatrix);
    if (validation.valid) {
      setKeyMatrix(newMatrix);
      setIsValidKey(true);
      setKeyError('');
    } else {
      generateRandomKey(); // Try again
    }
  };

  const handleMatrixChange = (row, col, value) => {
    const newMatrix = [...keyMatrix];
    newMatrix[row][col] = parseInt(value) || 0;
    setKeyMatrix(newMatrix);
  };

  const handleEncrypt = () => {
    if (!isValidKey || !plaintext.trim()) return;
    try {
      const result = encryptText(plaintext, keyMatrix);
      setEncryptedResult(result);
    } catch (error) {
      setEncryptedResult('Error: ' + error.message);
    }
  };

  const handleDecrypt = () => {
    if (!isValidKey || !ciphertext.trim()) return;
    try {
      const result = decryptText(ciphertext, keyMatrix);
      setDecryptedResult(result);
    } catch (error) {
      setDecryptedResult('Error: ' + error.message);
    }
  };

  const handleMatrixSizeChange = (size) => {
    setMatrixSize(size);
    if (size === 2) {
      setKeyMatrix([[3, 2], [5, 7]]);
    } else {
      setKeyMatrix([[6, 24, 1], [13, 16, 10], [20, 17, 15]]);
    }
  };

  useEffect(() => {
    const validation = validateKeyMatrix(keyMatrix);
    setIsValidKey(validation.valid);
    setKeyError(validation.error);
  }, [keyMatrix]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">Hill Cipher</h1>
            <p className="text-lg text-gray-600">Cryptography with Numerical Linear Algebra</p>
          </div>

          {/* Matrix Size Selection */}
          <div className="mb-8 p-4 bg-gray-50 rounded-lg">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Key className="mr-2" size={20} />
              Key Matrix Configuration
            </h2>
            <div className="flex gap-4 mb-4">
              <button
                onClick={() => handleMatrixSizeChange(2)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  matrixSize === 2 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                2×2 Matrix
              </button>
              <button
                onClick={() => handleMatrixSizeChange(3)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  matrixSize === 3 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                3×3 Matrix
              </button>
              <button
                onClick={generateRandomKey}
                className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors flex items-center"
              >
                <RefreshCw className="mr-2" size={16} />
                Random Key
              </button>
            </div>

            {/* Matrix Input */}
            <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${matrixSize}, 1fr)` }}>
              {keyMatrix.map((row, i) =>
                row.map((val, j) => (
                  <input
                    key={`${i}-${j}`}
                    type="number"
                    min="0"
                    max="25"
                    value={val}
                    onChange={(e) => handleMatrixChange(i, j, e.target.value)}
                    className="w-16 h-16 text-center border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none text-lg font-medium"
                  />
                ))
              )}
            </div>

            {/* Matrix Validation */}
            <div className="mt-4 flex items-center">
              {isValidKey ? (
                <div className="flex items-center text-green-600">
                  <CheckCircle className="mr-2" size={20} />
                  Valid key matrix
                </div>
              ) : (
                <div className="flex items-center text-red-600">
                  <AlertCircle className="mr-2" size={20} />
                  Invalid key: {keyError}
                </div>
              )}
            </div>
          </div>

          {/* Tabs */}
          <div className="mb-6">
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setActiveTab('encrypt')}
                className={`px-6 py-3 font-medium transition-colors ${
                  activeTab === 'encrypt'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Lock className="inline mr-2" size={18} />
                Encrypt
              </button>
              <button
                onClick={() => setActiveTab('decrypt')}
                className={`px-6 py-3 font-medium transition-colors ${
                  activeTab === 'decrypt'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Unlock className="inline mr-2" size={18} />
                Decrypt
              </button>
            </div>
          </div>

          {/* Encryption Tab */}
          {activeTab === 'encrypt' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Plaintext
                </label>
                <textarea
                  value={plaintext}
                  onChange={(e) => setPlaintext(e.target.value)}
                  placeholder="Enter text to encrypt..."
                  className="w-full p-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  rows="3"
                />
              </div>
              
              <button
                onClick={handleEncrypt}
                disabled={!isValidKey || !plaintext.trim()}
                className="w-full py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
              >
                <Lock className="inline mr-2" size={18} />
                Encrypt Text
              </button>

              {encryptedResult && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h3 className="font-medium text-blue-800 mb-2">Encrypted Result:</h3>
                  <p className="text-blue-700 font-mono text-lg break-all">{encryptedResult}</p>
                </div>
              )}
            </div>
          )}

          {/* Decryption Tab */}
          {activeTab === 'decrypt' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ciphertext
                </label>
                <textarea
                  value={ciphertext}
                  onChange={(e) => setCiphertext(e.target.value)}
                  placeholder="Enter text to decrypt..."
                  className="w-full p-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  rows="3"
                />
              </div>
              
              <button
                onClick={handleDecrypt}
                disabled={!isValidKey || !ciphertext.trim()}
                className="w-full py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
              >
                <Unlock className="inline mr-2" size={18} />
                Decrypt Text
              </button>

              {decryptedResult && (
                <div className="p-4 bg-green-50 rounded-lg">
                  <h3 className="font-medium text-green-800 mb-2">Decrypted Result:</h3>
                  <p className="text-green-700 font-mono text-lg break-all">{decryptedResult}</p>
                </div>
              )}
            </div>
          )}

          {/* Information Section */}
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">About Hill Cipher</h3>
            <p className="text-gray-600 text-sm">
              The Hill cipher is a polygraphic substitution cipher based on linear algebra. 
              It uses matrix multiplication to encrypt blocks of plaintext. The key matrix 
              must be invertible modulo 26 (for English alphabet) to ensure decryption is possible.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HillCipherApp;