/*
 * WASM Loader for dicti0nary-attack
 * Loads and initializes Chapel-compiled WASM modules
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 * SPDX-FileCopyrightText: 2025 Security Research Team
 *
 * Architecture: Chapel → emchapel → WASM → JavaScript FFI
 */

'use strict';

/**
 * Global WASM module registry
 * Stores loaded WASM modules and their exported functions
 */
window.DICTI0NARY_WASM = {
  modules: {},
  ready: false,
  errors: [],

  // Configuration
  config: {
    wasmPath: '/static/wasm/',
    modules: [
      'leetspeak',
      'phonetic',
      'pattern',
      'random',
      'markov',
      'hash_cracker'
    ],
    timeout: 10000, // 10 seconds
  }
};

/**
 * WASM Module Loader Class
 */
class WasmModuleLoader {
  constructor(moduleName, wasmPath) {
    this.moduleName = moduleName;
    this.wasmPath = wasmPath;
    this.instance = null;
    this.memory = null;
    this.exports = null;
  }

  /**
   * Load and instantiate WASM module
   */
  async load() {
    try {
      const response = await fetch(`${this.wasmPath}${this.moduleName}.wasm`);

      if (!response.ok) {
        throw new Error(`Failed to fetch ${this.moduleName}.wasm: ${response.statusText}`);
      }

      const wasmBytes = await response.arrayBuffer();

      // Import object for WASM (environment functions)
      const importObject = {
        env: {
          memory: new WebAssembly.Memory({ initial: 256, maximum: 512 }),

          // Chapel runtime functions (minimal stubs)
          __chapel_print: (ptr, len) => {
            const str = this.readString(ptr, len);
            console.log(`[Chapel] ${str}`);
          },

          __chapel_error: (ptr, len) => {
            const str = this.readString(ptr, len);
            console.error(`[Chapel Error] ${str}`);
          },

          // Math functions that Chapel might need
          sin: Math.sin,
          cos: Math.cos,
          tan: Math.tan,
          exp: Math.exp,
          log: Math.log,
          pow: Math.pow,
          sqrt: Math.sqrt,
        }
      };

      const wasmModule = await WebAssembly.instantiate(wasmBytes, importObject);

      this.instance = wasmModule.instance;
      this.exports = wasmModule.instance.exports;
      this.memory = importObject.env.memory;

      console.log(`✓ Loaded WASM module: ${this.moduleName}`);
      return true;

    } catch (error) {
      console.error(`✗ Failed to load WASM module ${this.moduleName}:`, error);
      window.DICTI0NARY_WASM.errors.push({
        module: this.moduleName,
        error: error.message
      });
      return false;
    }
  }

  /**
   * Read string from WASM memory
   */
  readString(ptr, len) {
    if (!this.memory) return '';

    const bytes = new Uint8Array(this.memory.buffer, ptr, len);
    return new TextDecoder('utf-8').decode(bytes);
  }

  /**
   * Write string to WASM memory
   */
  writeString(str) {
    if (!this.memory) return { ptr: 0, len: 0 };

    const encoder = new TextEncoder();
    const bytes = encoder.encode(str);

    // Allocate memory in WASM (if Chapel exports malloc)
    let ptr;
    if (this.exports.malloc) {
      ptr = this.exports.malloc(bytes.length);
    } else {
      // Fallback: use static buffer at a known offset
      ptr = 1024; // Start after first 1KB
    }

    const memoryBytes = new Uint8Array(this.memory.buffer, ptr, bytes.length);
    memoryBytes.set(bytes);

    return { ptr, len: bytes.length };
  }

  /**
   * Read array of strings from WASM memory
   */
  readStringArray(ptrArray, count) {
    if (!this.memory) return [];

    const result = [];
    const ptrView = new Uint32Array(this.memory.buffer, ptrArray, count);

    for (let i = 0; i < count; i++) {
      const strPtr = ptrView[i];
      // Assume null-terminated strings
      let len = 0;
      const bytes = new Uint8Array(this.memory.buffer, strPtr);
      while (bytes[len] !== 0 && len < 1000) len++;

      result.push(this.readString(strPtr, len));
    }

    return result;
  }

  /**
   * Get exported function
   */
  getFunction(name) {
    if (!this.exports || !this.exports[name]) {
      console.warn(`Function ${name} not found in ${this.moduleName}`);
      return null;
    }
    return this.exports[name];
  }
}

/**
 * Initialize all WASM modules
 */
async function initializeWasm() {
  console.log('🔧 Initializing WASM modules...');

  const config = window.DICTI0NARY_WASM.config;
  const loadPromises = [];

  // Check for WebAssembly support
  if (typeof WebAssembly === 'undefined') {
    console.error('❌ WebAssembly is not supported in this browser');
    showError('WebAssembly not supported. Please use a modern browser.');
    return false;
  }

  // Load all modules in parallel
  for (const moduleName of config.modules) {
    const loader = new WasmModuleLoader(moduleName, config.wasmPath);
    loadPromises.push(loader.load().then(success => {
      if (success) {
        window.DICTI0NARY_WASM.modules[moduleName] = loader;
      }
      return success;
    }));
  }

  // Wait for all modules with timeout
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('WASM loading timeout')), config.timeout)
  );

  try {
    const results = await Promise.race([
      Promise.all(loadPromises),
      timeoutPromise
    ]);

    const successCount = results.filter(r => r).length;
    console.log(`✓ Loaded ${successCount}/${config.modules.length} WASM modules`);

    if (successCount === 0) {
      console.error('❌ No WASM modules loaded successfully');
      showError('Failed to load WASM modules. Running in degraded mode.');
      return false;
    }

    window.DICTI0NARY_WASM.ready = true;
    console.log('✓ WASM initialization complete');

    // Dispatch ready event
    window.dispatchEvent(new CustomEvent('wasm-ready'));

    return true;

  } catch (error) {
    console.error('❌ WASM initialization failed:', error);
    showError('WASM initialization failed. Some features may not work.');
    return false;
  }
}

/**
 * Show error message to user
 */
function showError(message) {
  // Create error banner if it doesn't exist
  let errorBanner = document.getElementById('wasm-error-banner');
  if (!errorBanner) {
    errorBanner = document.createElement('div');
    errorBanner.id = 'wasm-error-banner';
    errorBanner.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background: linear-gradient(135deg, rgba(255, 68, 102, 0.9), rgba(255, 187, 0, 0.9));
      color: white;
      padding: 1rem;
      text-align: center;
      font-weight: bold;
      z-index: 9999;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    `;
    document.body.prepend(errorBanner);
  }
  errorBanner.textContent = `⚠️ ${message}`;
}

/**
 * Get WASM module by name
 */
function getWasmModule(name) {
  if (!window.DICTI0NARY_WASM.ready) {
    console.warn('WASM not ready yet');
    return null;
  }
  return window.DICTI0NARY_WASM.modules[name];
}

/**
 * Call WASM function with error handling
 */
function callWasmFunction(moduleName, functionName, ...args) {
  const module = getWasmModule(moduleName);
  if (!module) {
    throw new Error(`WASM module ${moduleName} not loaded`);
  }

  const func = module.getFunction(functionName);
  if (!func) {
    throw new Error(`Function ${functionName} not found in ${moduleName}`);
  }

  try {
    return func(...args);
  } catch (error) {
    console.error(`Error calling ${moduleName}.${functionName}:`, error);
    throw error;
  }
}

// Export functions to global scope
window.getWasmModule = getWasmModule;
window.callWasmFunction = callWasmFunction;

// Auto-initialize on DOM content loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeWasm);
} else {
  // DOM already loaded
  initializeWasm();
}

console.log('📦 WASM Loader initialized');
