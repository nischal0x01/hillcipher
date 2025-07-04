let size = 2;
let matrix = [[3,2],[5,7]];

function setSize(n) {
  size = n;
  document.querySelectorAll('.buttons button').forEach(btn => btn.classList.remove('active'));
  document.querySelector(`.buttons button:nth-child(${n-1})`).classList.add('active');
  matrix = Array.from({length: n}, () => Array(n).fill(0));
  renderMatrix();
  validateMatrix();
}

function renderMatrix() {
  const grid = document.getElementById('matrixGrid');
  grid.style.gridTemplateColumns = `repeat(${size}, 50px)`;
  grid.innerHTML = '';
  for(let i=0; i<size; i++) {
    for(let j=0; j<size; j++) {
      const input = document.createElement('input');
      input.type = 'number';
      input.value = matrix[i][j];
      input.oninput = e => {
        matrix[i][j] = parseInt(e.target.value) || 0;
        validateMatrix();
      }
      grid.appendChild(input);
    }
  }
}

function validateMatrix() {
  fetch('/api/validate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key_matrix: matrix })
  }).then(res => res.json()).then(data => {
    const status = document.getElementById('matrixStatus');
    status.innerText = data.valid ? '✅ Valid key matrix' : `❌ Invalid key: ${data.error}`;
    status.style.color = data.valid ? '#28a745' : '#dc3545';
  });
}

function randomKey() {
  fetch('/api/generate-key', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ size })
  }).then(res => res.json()).then(data => {
    matrix = data.key_matrix;
    renderMatrix();
    validateMatrix();
  });
}

function setTab(tab) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(`${tab}Tab`).classList.add('active');
  document.getElementById('encryptForm').classList.toggle('hidden', tab !== 'encrypt');
  document.getElementById('decryptForm').classList.toggle('hidden', tab !== 'decrypt');
  document.getElementById('result').innerText = '';
}

function submit(type) {
  const text = document.getElementById(type === 'encrypt' ? 'plaintext' : 'ciphertext').value;
  fetch(`/api/${type}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ [type === 'encrypt' ? 'plaintext' : 'ciphertext']: text, key_matrix: matrix })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('result').innerText = data.result || data.error;
  });
  if (!/^[a-zA-Z\s]*$/.test(text)) {
  document.getElementById('result').innerText = "❌ Only alphabetic characters (A-Z) are allowed!";
  return;
}
}

// Initial setup
renderMatrix();
validateMatrix();
