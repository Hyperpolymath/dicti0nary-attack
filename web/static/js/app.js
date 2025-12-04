/*
 * Main Application JavaScript for dicti0nary-attack
 * Handles UI interactions and WASM function calls
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 * SPDX-FileCopyrightText: 2025 Security Research Team
 */

'use strict';

/**
 * Application State
 */
const AppState = {
  currentTab: 'generate',
  wasmReady: false,
  processing: false,
};

/**
 * Initialize application
 */
function initializeApp() {
  console.log('🚀 Initializing dicti0nary-attack application');

  // Set up tab navigation
  setupTabNavigation();

  // Set up form handlers
  setupGenerateForm();
  setupCrackForm();
  setupHashForm();

  // Listen for WASM ready event
  window.addEventListener('wasm-ready', () => {
    console.log('✓ WASM ready, enabling forms');
    AppState.wasmReady = true;
    enableForms();
  });

  console.log('✓ Application initialized');
}

/**
 * Tab Navigation
 */
function setupTabNavigation() {
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const tabName = button.getAttribute('data-tab');

      // Update button states
      tabButtons.forEach(btn => {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
      });
      button.classList.add('active');
      button.setAttribute('aria-selected', 'true');

      // Update panel visibility
      tabPanels.forEach(panel => {
        panel.hidden = true;
      });
      const activePanel = document.getElementById(tabName);
      if (activePanel) {
        activePanel.hidden = false;
        AppState.currentTab = tabName;
      }
    });
  });
}

/**
 * Generate Form Handler
 */
function setupGenerateForm() {
  const form = document.getElementById('generate-form');
  const outputPanel = document.getElementById('generate-output');
  const outputStats = outputPanel.querySelector('.output-stats');
  const outputContent = outputPanel.querySelector('.output-content');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!AppState.wasmReady) {
      showNotification('WASM modules not ready yet. Please wait...', 'warning');
      return;
    }

    if (AppState.processing) {
      showNotification('Already processing. Please wait...', 'warning');
      return;
    }

    // Get form values
    const generatorType = form.querySelector('#gen-type').value;
    const count = parseInt(form.querySelector('#gen-count').value);
    const minLength = parseInt(form.querySelector('#gen-min').value);
    const maxLength = parseInt(form.querySelector('#gen-max').value);

    // Validate
    if (count < 1 || count > 10000) {
      showNotification('Count must be between 1 and 10,000', 'error');
      return;
    }

    if (minLength > maxLength) {
      showNotification('Min length cannot be greater than max length', 'error');
      return;
    }

    AppState.processing = true;
    setFormLoading(form, true);

    try {
      const startTime = performance.now();

      // Generate passwords using WASM
      const passwords = await generatePasswords(generatorType, count, minLength, maxLength);

      const endTime = performance.now();
      const elapsed = ((endTime - startTime) / 1000).toFixed(2);

      // Display results
      outputStats.innerHTML = `
        <div>
          <strong>${passwords.length}</strong>
          <span>Generated</span>
        </div>
        <div>
          <strong>${generatorType}</strong>
          <span>Generator</span>
        </div>
        <div>
          <strong>${minLength}-${maxLength}</strong>
          <span>Length Range</span>
        </div>
        <div>
          <strong>${elapsed}s</strong>
          <span>Time Taken</span>
        </div>
      `;

      outputContent.textContent = passwords.join('\n');
      outputPanel.hidden = false;

      showNotification(`Generated ${passwords.length} passwords in ${elapsed}s`, 'success');

    } catch (error) {
      console.error('Generation error:', error);
      showNotification(`Generation failed: ${error.message}`, 'error');
    } finally {
      AppState.processing = false;
      setFormLoading(form, false);
    }
  });
}

/**
 * Crack Form Handler
 */
function setupCrackForm() {
  const form = document.getElementById('crack-form');
  const outputPanel = document.getElementById('crack-output');
  const outputContent = outputPanel.querySelector('.output-content');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!AppState.wasmReady) {
      showNotification('WASM modules not ready yet. Please wait...', 'warning');
      return;
    }

    if (AppState.processing) {
      showNotification('Already processing. Please wait...', 'warning');
      return;
    }

    // Get form values
    const hash = form.querySelector('#crack-hash').value.trim();
    const algorithm = form.querySelector('#crack-algo').value;
    const generator = form.querySelector('#crack-gen').value;
    const maxAttempts = parseInt(form.querySelector('#crack-max').value);

    // Validate hash format
    if (!hash || !isValidHash(hash, algorithm)) {
      showNotification(`Invalid ${algorithm.toUpperCase()} hash format`, 'error');
      return;
    }

    AppState.processing = true;
    setFormLoading(form, true);

    try {
      const startTime = performance.now();

      // Crack hash using WASM
      const result = await crackHash(hash, algorithm, generator, maxAttempts);

      const endTime = performance.now();
      const elapsed = ((endTime - startTime) / 1000).toFixed(2);

      // Display results
      if (result.found) {
        outputContent.innerHTML = `
          <div class="text-success" style="margin-bottom: 1rem;">
            <strong>✓ Password Found!</strong>
          </div>
          <div style="margin-bottom: 0.5rem;">
            <strong>Password:</strong> <code style="color: var(--color-success);">${escapeHtml(result.password)}</code>
          </div>
          <div style="margin-bottom: 0.5rem;">
            <strong>Attempts:</strong> ${result.attempts.toLocaleString()} / ${maxAttempts.toLocaleString()}
          </div>
          <div style="margin-bottom: 0.5rem;">
            <strong>Time:</strong> ${elapsed}s
          </div>
          <div>
            <strong>Rate:</strong> ${Math.floor(result.attempts / elapsed).toLocaleString()} hashes/sec
          </div>
        `;
        showNotification(`Password cracked in ${elapsed}s!`, 'success');
      } else {
        outputContent.innerHTML = `
          <div class="text-warning" style="margin-bottom: 1rem;">
            <strong>✗ Password Not Found</strong>
          </div>
          <div style="margin-bottom: 0.5rem;">
            <strong>Attempts:</strong> ${maxAttempts.toLocaleString()}
          </div>
          <div style="margin-bottom: 0.5rem;">
            <strong>Time:</strong> ${elapsed}s
          </div>
          <div>
            <strong>Rate:</strong> ${Math.floor(maxAttempts / elapsed).toLocaleString()} hashes/sec
          </div>
          <div style="margin-top: 1rem; color: var(--color-text-muted);">
            Try increasing max attempts or using a different generator.
          </div>
        `;
        showNotification('Password not found. Try different settings.', 'warning');
      }

      outputPanel.hidden = false;

    } catch (error) {
      console.error('Cracking error:', error);
      showNotification(`Cracking failed: ${error.message}`, 'error');
    } finally {
      AppState.processing = false;
      setFormLoading(form, false);
    }
  });
}

/**
 * Hash Form Handler
 */
function setupHashForm() {
  const form = document.getElementById('hash-form');
  const outputPanel = document.getElementById('hash-output');
  const outputContent = outputPanel.querySelector('.output-content');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!AppState.wasmReady) {
      showNotification('WASM modules not ready yet. Please wait...', 'warning');
      return;
    }

    // Get form values
    const password = form.querySelector('#hash-input').value;
    const algorithm = form.querySelector('#hash-algo').value;

    if (!password) {
      showNotification('Please enter a password to hash', 'error');
      return;
    }

    setFormLoading(form, true);

    try {
      const startTime = performance.now();

      // Hash password using WASM
      const hash = await hashPassword(password, algorithm);

      const endTime = performance.now();
      const elapsed = ((endTime - startTime) * 1000).toFixed(2); // ms

      // Display result
      outputContent.textContent = `Algorithm: ${algorithm.toUpperCase()}\nHash: ${hash}\n\nTime: ${elapsed}ms`;
      outputPanel.hidden = false;

      showNotification(`Password hashed using ${algorithm.toUpperCase()}`, 'success');

    } catch (error) {
      console.error('Hashing error:', error);
      showNotification(`Hashing failed: ${error.message}`, 'error');
    } finally {
      setFormLoading(form, false);
    }
  });
}

/**
 * Generate passwords using WASM
 */
async function generatePasswords(generatorType, count, minLength, maxLength) {
  // Map generator type to WASM module
  const moduleMap = {
    'leetspeak': 'leetspeak',
    'phonetic': 'phonetic',
    'pattern': 'pattern',
    'random': 'random',
    'markov': 'markov'
  };

  const moduleName = moduleMap[generatorType];
  if (!moduleName) {
    throw new Error(`Unknown generator type: ${generatorType}`);
  }

  const module = window.getWasmModule(moduleName);
  if (!module) {
    // Fallback to JavaScript implementation
    console.warn(`WASM module ${moduleName} not available, using fallback`);
    return generatePasswordsFallback(generatorType, count, minLength, maxLength);
  }

  // TODO: Call actual WASM function
  // This is a placeholder until WASM functions are fully implemented
  // const func = module.getFunction('generate');
  // return callWasmGenerate(func, count, minLength, maxLength);

  // For now, use fallback
  return generatePasswordsFallback(generatorType, count, minLength, maxLength);
}

/**
 * Fallback JavaScript password generation
 */
function generatePasswordsFallback(generatorType, count, minLength, maxLength) {
  const passwords = [];

  for (let i = 0; i < count; i++) {
    let password = '';

    switch (generatorType) {
      case 'leetspeak':
        password = generateLeetspeak(minLength, maxLength);
        break;
      case 'phonetic':
        password = generatePhonetic(minLength, maxLength);
        break;
      case 'pattern':
        password = generatePattern(minLength, maxLength);
        break;
      case 'random':
        password = generateRandom(minLength, maxLength);
        break;
      case 'markov':
        password = generateMarkov(minLength, maxLength);
        break;
      default:
        password = generateRandom(minLength, maxLength);
    }

    passwords.push(password);
  }

  return passwords;
}

function generateLeetspeak(minLen, maxLen) {
  const words = ['password', 'admin', 'login', 'secure', 'access', 'system'];
  const word = words[Math.floor(Math.random() * words.length)];
  const leetMap = { 'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7' };

  let result = word.split('').map(c =>
    Math.random() > 0.5 && leetMap[c] ? leetMap[c] : c
  ).join('');

  // Add numbers/symbols to reach length
  while (result.length < minLen) {
    result += Math.floor(Math.random() * 10);
  }

  return result.substring(0, maxLen);
}

function generatePhonetic(minLen, maxLen) {
  const phonetic = ['for', 'to', 'you', 'see', 'why', 'are', 'bee', 'sea'];
  const numbers = ['4', '2', 'u', 'c', 'y', 'r', 'b', 'c'];

  let result = '';
  const iterations = Math.ceil(maxLen / 3);

  for (let i = 0; i < iterations && result.length < maxLen; i++) {
    const idx = Math.floor(Math.random() * phonetic.length);
    result += Math.random() > 0.5 ? phonetic[idx] : numbers[idx];
  }

  return result.substring(0, Math.max(minLen, Math.min(result.length, maxLen)));
}

function generatePattern(minLen, maxLen) {
  const patterns = [
    'qwerty', 'asdfgh', 'zxcvbn', '123456', 'qazwsx', 'qwertyuiop',
    'asdfghjkl', '1qaz2wsx', 'zaq12wsx'
  ];

  let result = patterns[Math.floor(Math.random() * patterns.length)];

  // Add variation
  if (Math.random() > 0.5) {
    result = result.split('').reverse().join('');
  }

  // Add numbers
  result += Math.floor(Math.random() * 1000);

  return result.substring(0, Math.max(minLen, Math.min(result.length, maxLen)));
}

function generateRandom(minLen, maxLen) {
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  const length = Math.floor(Math.random() * (maxLen - minLen + 1)) + minLen;
  let result = '';

  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }

  return result;
}

function generateMarkov(minLen, maxLen) {
  // Simple Markov-like generation
  const bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'ed'];
  const length = Math.floor(Math.random() * (maxLen - minLen + 1)) + minLen;
  let result = '';

  while (result.length < length) {
    result += bigrams[Math.floor(Math.random() * bigrams.length)];
  }

  return result.substring(0, length);
}

/**
 * Crack hash using WASM
 */
async function crackHash(hash, algorithm, generator, maxAttempts) {
  const module = window.getWasmModule('hash_cracker');

  if (!module) {
    // Fallback to JavaScript
    return crackHashFallback(hash, algorithm, generator, maxAttempts);
  }

  // TODO: Call actual WASM function
  return crackHashFallback(hash, algorithm, generator, maxAttempts);
}

/**
 * Fallback JavaScript hash cracking
 */
async function crackHashFallback(targetHash, algorithm, generator, maxAttempts) {
  let attempts = 0;

  // Generate candidates and test
  for (let i = 0; i < maxAttempts; i++) {
    const password = (await generatePasswordsFallback(generator, 1, 6, 16))[0];
    attempts++;

    const hash = await hashPassword(password, algorithm);

    if (hash.toLowerCase() === targetHash.toLowerCase()) {
      return { found: true, password, attempts };
    }

    // Yield to UI every 1000 attempts
    if (attempts % 1000 === 0) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }

  return { found: false, password: null, attempts };
}

/**
 * Hash password using WASM or Web Crypto API
 */
async function hashPassword(password, algorithm) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);

  const algoMap = {
    'md5': 'MD5',      // Not in Web Crypto, would need polyfill
    'sha1': 'SHA-1',
    'sha256': 'SHA-256',
    'sha512': 'SHA-512'
  };

  const algoName = algoMap[algorithm];

  if (algorithm === 'md5') {
    // Use simple MD5 polyfill for demo
    return md5Polyfill(password);
  }

  const hashBuffer = await crypto.subtle.digest(algoName, data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Simple MD5 polyfill (NOT cryptographically secure, for demo only)
 */
function md5Polyfill(str) {
  // This is a VERY simplified MD5 for demonstration
  // In production, use a proper MD5 library
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash).toString(16).padStart(32, '0');
}

/**
 * Validate hash format
 */
function isValidHash(hash, algorithm) {
  const lengths = {
    'md5': 32,
    'sha1': 40,
    'sha256': 64,
    'sha512': 128
  };

  const expectedLength = lengths[algorithm];
  return hash.length === expectedLength && /^[a-fA-F0-9]+$/.test(hash);
}

/**
 * Copy output to clipboard
 */
window.copyOutput = function(panelId) {
  const panel = document.getElementById(panelId);
  const content = panel.querySelector('.output-content');

  if (!content) return;

  const text = content.textContent;

  navigator.clipboard.writeText(text).then(() => {
    showNotification('Copied to clipboard!', 'success');
  }).catch(err => {
    console.error('Copy failed:', err);
    showNotification('Failed to copy to clipboard', 'error');
  });
};

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
  const colors = {
    success: 'var(--color-success)',
    error: 'var(--color-error)',
    warning: 'var(--color-warning)',
    info: 'var(--color-info)'
  };

  const notification = document.createElement('div');
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: ${colors[type] || colors.info};
    color: var(--color-bg-primary);
    padding: 1rem 1.5rem;
    border-radius: 8px;
    box-shadow: var(--shadow-lg);
    font-weight: 600;
    z-index: 10000;
    animation: slideIn 0.3s ease;
  `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

/**
 * Set form loading state
 */
function setFormLoading(form, loading) {
  const submitButton = form.querySelector('button[type="submit"]');

  if (loading) {
    form.classList.add('loading');
    submitButton.disabled = true;
    submitButton.textContent = 'Processing...';
  } else {
    form.classList.remove('loading');
    submitButton.disabled = false;
    submitButton.textContent = submitButton.getAttribute('data-original-text') ||
      submitButton.textContent.replace('Processing...', 'Generate');
  }
}

/**
 * Enable forms after WASM loads
 */
function enableForms() {
  const forms = document.querySelectorAll('.tool-form');
  forms.forEach(form => {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
      submitButton.disabled = false;
    }
  });
}

/**
 * HTML escape for security
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
`;
document.head.appendChild(style);

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}

console.log('🎨 Application JavaScript loaded');
