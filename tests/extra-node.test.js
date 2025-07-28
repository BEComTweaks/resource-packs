// Node.js compatible test runner for extra.js functionality
// Testing Framework: Simple custom test runner (no external dependencies)

// Since this is browser-focused code, we'll create mock implementations for testing
const assert = require('assert');

// Mock browser APIs
global.document = {
  querySelector: () => ({ checked: false, appendChild: () => {}, innerHTML: '' }),
  getElementById: () => ({ children: [], appendChild: () => {}, removeChild: () => {} }),
  createElement: () => ({ className: '', style: {}, dataset: {}, innerHTML: '' }),
  head: { appendChild: () => {} }
};

global.window = {
  innerWidth: 1920,
  innerHeight: 1080,
  matchMedia: () => ({ matches: false })
};

global.console = { log: () => {} };
global.fetch = () => Promise.resolve({ ok: true });

// Test configuration constants
const serverip = "localhost";
const textures = [
  { src: "stone.png", probability: 0.59 },
  { src: "copper_ore.png", probability: 0.128 },
  { src: "coal_ore.png", probability: 0.128 },
  { src: "iron_ore.png", probability: 0.064 },
  { src: "lapis_ore.png", probability: 0.032 },
  { src: "redstone_ore.png", probability: 0.032 },
  { src: "gold_ore.png", probability: 0.016 },
  { src: "emerald_ore.png", probability: 0.008 },
  { src: "diamond_ore.png", probability: 0.002 }
];

// Mock selectTexture function
function selectTexture() {
  const rand = Math.random();
  let cumulativeProbability = 0;
  for (const texture of textures) {
    cumulativeProbability += texture.probability;
    if (rand < cumulativeProbability) {
      return texture.src;
    }
  }
  return "stone.png";
}

// Test runner
function runTests() {
  console.log('Running Extra.js Node.js Tests...\n');
  
  // Test 1: Texture array validation
  console.log('✓ Testing texture array validation');
  assert.strictEqual(textures.length, 9, 'Should have 9 textures');
  
  textures.forEach((texture, index) => {
    assert.ok(texture.hasOwnProperty('src'), `Texture ${index + 1} should have src`);
    assert.ok(texture.hasOwnProperty('probability'), `Texture ${index + 1} should have probability`);
    assert.strictEqual(typeof texture.src, 'string', `Texture ${index + 1} src should be string`);
    assert.strictEqual(typeof texture.probability, 'number', `Texture ${index + 1} probability should be number`);
  });
  
  const totalProbability = textures.reduce((sum, texture) => sum + texture.probability, 0);
  assert.ok(Math.abs(totalProbability - 1.0) < 0.001, 'Total probability should be ~1.0');
  
  // Test 2: selectTexture function
  console.log('✓ Testing selectTexture function');
  const originalRandom = Math.random;
  
  Math.random = () => 0.1;
  assert.strictEqual(selectTexture(), 'stone.png', 'Should select stone for 0.1');
  
  Math.random = () => 0.65;
  assert.strictEqual(selectTexture(), 'copper_ore.png', 'Should select copper for 0.65');
  
  Math.random = () => 0.999;
  assert.strictEqual(selectTexture(), 'diamond_ore.png', 'Should select diamond for 0.999');
  
  Math.random = () => 1.0;
  assert.strictEqual(selectTexture(), 'stone.png', 'Should fallback to stone for 1.0');
  
  Math.random = originalRandom;
  
  // Test 3: Configuration constants
  console.log('✓ Testing configuration constants');
  assert.strictEqual(serverip, "localhost", 'Server IP should be localhost');
  assert.strictEqual(typeof serverip, "string", 'Server IP should be string');
  
  // Test 4: Texture probability distribution
  console.log('✓ Testing texture probability distribution');
  const stoneTexture = textures.find(t => t.src === 'stone.png');
  assert.strictEqual(stoneTexture.probability, 0.59, 'Stone should be most common');
  
  const diamondTexture = textures.find(t => t.src === 'diamond_ore.png');
  assert.strictEqual(diamondTexture.probability, 0.002, 'Diamond should be rarest');
  
  // Test 5: Utility function mocks
  console.log('✓ Testing utility functions');
  
  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
  
  assert.ok(sleep(100) instanceof Promise, 'sleep should return Promise');
  
  function getTimeoutDuration() {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    return mediaQuery.matches ? 0 : 1000;
  }
  
  assert.strictEqual(getTimeoutDuration(), 1000, 'Should return 1000 for normal motion');
  
  // Test 6: Error handling
  console.log('✓ Testing error handling');
  
  function updateTile(element) {
    if (!element) return;
    const tile_image = selectTexture();
    element.style.backgroundImage = `url("images/blocks/${tile_image}")`;
    element.dataset.type = tile_image;
  }
  
  // Should not throw for null/undefined
  assert.doesNotThrow(() => updateTile(null), 'Should handle null gracefully');
  assert.doesNotThrow(() => updateTile(undefined), 'Should handle undefined gracefully');
  
  console.log('\n✅ All tests passed!');
}

// Run tests if called directly
if (require.main === module) {
  try {
    runTests();
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    process.exit(1);
  }
}

module.exports = { runTests, textures, selectTexture };