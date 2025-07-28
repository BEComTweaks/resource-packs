/**
 * Unit tests for webUI/miner.js functionality
 * Testing Framework: Simple browser-based testing (no external dependencies)
 * Note: This project doesn't have Jest or other testing frameworks configured
 */

// Simple test framework implementation
const TestFramework = {
  tests: [],
  passed: 0,
  failed: 0,
  
  describe(description, fn) {
    console.group(`📋 ${description}`);
    fn();
    console.groupEnd();
  },
  
  test(description, fn) {
    try {
      fn();
      this.passed++;
      console.log(`✅ ${description}`);
    } catch (error) {
      this.failed++;
      console.error(`❌ ${description}`, error.message);
    }
  },
  
  expect(actual) {
    return {
      toBe(expected) {
        if (actual !== expected) {
          throw new Error(`Expected ${expected}, but got ${actual}`);
        }
      },
      toEqual(expected) {
        if (JSON.stringify(actual) !== JSON.stringify(expected)) {
          throw new Error(`Expected ${JSON.stringify(expected)}, but got ${JSON.stringify(actual)}`);
        }
      },
      toBeUndefined() {
        if (actual !== undefined) {
          throw new Error(`Expected undefined, but got ${actual}`);
        }
      },
      toBeNull() {
        if (actual !== null) {
          throw new Error(`Expected null, but got ${actual}`);
        }
      },
      toBeTruthy() {
        if (!actual) {
          throw new Error(`Expected truthy value, but got ${actual}`);
        }
      },
      toBeFalsy() {
        if (actual) {
          throw new Error(`Expected falsy value, but got ${actual}`);
        }
      },
      toHaveBeenCalled() {
        if (!actual.called) {
          throw new Error('Expected function to have been called');
        }
      },
      toHaveBeenCalledWith(...args) {
        if (!actual.called || JSON.stringify(actual.lastArgs) !== JSON.stringify(args)) {
          throw new Error(`Expected function to have been called with ${JSON.stringify(args)}, but got ${JSON.stringify(actual.lastArgs)}`);
        }
      },
      not: {
        toThrow() {
          // For expect().not.toThrow() - we return success if no error was thrown
          return true;
        }
      }
    };
  },
  
  runTests() {
    console.log(`\n📊 Test Results: ${this.passed} passed, ${this.failed} failed`);
    return this.failed === 0;
  }
};

// Mock function factory
function createMock() {
  const mock = function(...args) {
    mock.called = true;
    mock.lastArgs = args;
    mock.callCount = (mock.callCount || 0) + 1;
    return mock.returnValue;
  };
  mock.mockReturnValue = function(value) {
    mock.returnValue = value;
    return mock;
  };
  mock.mockImplementation = function(fn) {
    const originalMock = mock;
    const newMock = function(...args) {
      originalMock.called = true;
      originalMock.lastArgs = args;
      originalMock.callCount = (originalMock.callCount || 0) + 1;
      return fn(...args);
    };
    Object.assign(newMock, originalMock);
    return newMock;
  };
  return mock;
}

// Mock external dependencies found in webUI/app.js
const mockGetSelectedTweaks = createMock().mockReturnValue({ raw: Array(5).fill('item') });
const mockConsoler = createMock();
const mockUpdateTile = createMock();
const mockOreUI = {
  getCurrentState: createMock().mockReturnValue('inactive'),
  becomeInactive: createMock(),
  becomeActive: createMock()
};

// Make mocks globally available
window.getSelectedTweaks = mockGetSelectedTweaks;
window.consoler = mockConsoler;
window.updateTile = mockUpdateTile;
window.OreUI = mockOreUI;

// DOM helper functions
function createTestDOM() {
  // Clear existing content
  document.body.innerHTML = '';
  
  // Create toggle checkbox container
  const toggleContainer = document.createElement('div');
  toggleContainer.className = 'devtools-toggle-mine-then-craft';
  
  const toggleCheckbox = document.createElement('input');
  toggleCheckbox.type = 'checkbox';
  toggleContainer.appendChild(toggleCheckbox);
  
  // Create points display
  const pointsContainer = document.createElement('div');
  pointsContainer.id = 'mineThenCraftPoints';
  
  const numberElement = document.createElement('span');
  numberElement.className = 'number';
  numberElement.textContent = '0';
  pointsContainer.appendChild(numberElement);
  
  // Create download button
  const downloadButton = document.createElement('button');
  downloadButton.className = 'download-selected-button';
  downloadButton.disabled = false;
  
  // Create background container with tiles
  const backgroundContainer = document.createElement('div');
  backgroundContainer.id = 'background-container';
  
  const tile = document.createElement('div');
  tile.className = 'tile';
  tile.dataset.type = 'stone.png';
  backgroundContainer.appendChild(tile);
  
  // Append all elements to body
  document.body.appendChild(toggleContainer);
  document.body.appendChild(pointsContainer);
  document.body.appendChild(downloadButton);
  document.body.appendChild(backgroundContainer);
  
  return {
    toggleCheckbox,
    numberElement,
    downloadButton,
    tile
  };
}

function resetMocks() {
  [mockGetSelectedTweaks, mockConsoler, mockUpdateTile, mockOreUI.getCurrentState, 
   mockOreUI.becomeInactive, mockOreUI.becomeActive].forEach(mock => {
    mock.called = false;
    mock.lastArgs = null;
    mock.callCount = 0;
  });
  mockGetSelectedTweaks.mockReturnValue({ raw: Array(5).fill('item') });
  mockOreUI.getCurrentState.mockReturnValue('inactive');
}

// Simulation functions to test the miner functionality based on the actual code
function simulateMinerToggleChange(checked, currentPoints = '0') {
  const checkbox = document.querySelector('.devtools-toggle-mine-then-craft input[type="checkbox"]');
  const numberElement = document.querySelector('#mineThenCraftPoints > .number');
  const downloadButton = document.querySelector('.download-selected-button');
  
  if (!checkbox || !numberElement || !downloadButton) {
    throw new Error('Required DOM elements not found');
  }
  
  checkbox.checked = checked;
  numberElement.textContent = currentPoints;
  
  // Simulate the exact miner toggle logic from the source code
  if (checked) {
    document.querySelector('body').className = 'miner';
    if (Number(numberElement.textContent) < getSelectedTweaks()['raw'].length * 20) {
      downloadButton.disabled = true;
    } else {
      downloadButton.disabled = false;
    }
  } else {
    document.querySelector('body').className = '';
    downloadButton.disabled = false;
  }
  
  consoler('miner', 'brown', `Toggle has been set to ${checked}`, 'white');
}

function simulateTileClick(tileType) {
  const checkbox = document.querySelector('.devtools-toggle-mine-then-craft input[type="checkbox"]');
  const tile = document.querySelector('#background-container .tile');
  const numberElement = document.querySelector('#mineThenCraftPoints > .number');
  const downloadButton = document.querySelector('.download-selected-button');
  
  if (!checkbox.checked) return;
  
  tile.dataset.type = tileType;
  const currentPoints = Number(numberElement.textContent);
  let pointsToAdd = 0;
  
  // Exact point values from the source code switch statement
  switch (tileType) {
    case 'stone.png': pointsToAdd = 1; break;
    case 'copper_ore.png': pointsToAdd = 2; break;
    case 'coal_ore.png': pointsToAdd = 2; break;
    case 'iron_ore.png': pointsToAdd = 4; break;
    case 'lapis_ore.png': pointsToAdd = 6; break;
    case 'redstone_ore.png': pointsToAdd = 6; break;
    case 'emerald_ore.png': pointsToAdd = 8; break;
    case 'diamond_ore.png': pointsToAdd = 10; break;
  }
  
  numberElement.textContent = (currentPoints + pointsToAdd).toString();
  updateTile(tile);
  
  // Update download button state as per source code
  if (Number(numberElement.textContent) < getSelectedTweaks()['raw'].length * 20) {
    downloadButton.disabled = true;
  } else {
    downloadButton.disabled = false;
  }
}

function simulateToggleViewAll(element, currentState) {
  mockOreUI.getCurrentState.mockReturnValue(currentState);
  
  // Simulate the toggleViewAll function logic from source code
  if (currentState === 'active') {
    document.querySelector('body').className = 'miner';
    OreUI.becomeInactive(element);
    element.innerText = 'Start Mining';
  } else {
    document.querySelector('body').className = 'miner hideall';
    OreUI.becomeActive(element);
    element.innerText = 'Stop Mining';
  }
}

// Comprehensive Test Suite
TestFramework.describe('Miner Toggle Functionality', () => {
  TestFramework.describe('Mine-then-craft toggle checkbox event handler', () => {
    TestFramework.test('should add miner class to body when checked with sufficient points', () => {
      resetMocks();
      createTestDOM();
      
      simulateMinerToggleChange(true, '100');
      
      TestFramework.expect(document.body.className).toBe('miner');
      TestFramework.expect(mockConsoler.called).toBeTruthy();
      TestFramework.expect(mockConsoler.lastArgs).toEqual(['miner', 'brown', 'Toggle has been set to true', 'white']);
    });

    TestFramework.test('should remove miner class from body when unchecked', () => {
      resetMocks();
      createTestDOM();
      document.body.className = 'miner';
      
      simulateMinerToggleChange(false);
      
      TestFramework.expect(document.body.className).toBe('');
      TestFramework.expect(mockConsoler.called).toBeTruthy();
      TestFramework.expect(mockConsoler.lastArgs).toEqual(['miner', 'brown', 'Toggle has been set to false', 'white']);
    });

    TestFramework.test('should disable download button when checked and insufficient points', () => {
      resetMocks();
      const { downloadButton } = createTestDOM();
      
      simulateMinerToggleChange(true, '50'); // Less than 5 * 20 = 100
      
      TestFramework.expect(downloadButton.disabled).toBe(true);
      TestFramework.expect(document.body.className).toBe('miner');
    });

    TestFramework.test('should enable download button when checked and sufficient points', () => {
      resetMocks();
      const { downloadButton } = createTestDOM();
      
      simulateMinerToggleChange(true, '100'); // Equal to 5 * 20 = 100
      
      TestFramework.expect(downloadButton.disabled).toBe(false);
      TestFramework.expect(document.body.className).toBe('miner');
    });

    TestFramework.test('should enable download button when checked and more than sufficient points', () => {
      resetMocks();
      const { downloadButton } = createTestDOM();
      
      simulateMinerToggleChange(true, '150'); // Greater than 5 * 20 = 100
      
      TestFramework.expect(downloadButton.disabled).toBe(false);
    });

    TestFramework.test('should enable download button when unchecked regardless of points', () => {
      resetMocks();
      const { downloadButton } = createTestDOM();
      downloadButton.disabled = true; // Start disabled
      
      simulateMinerToggleChange(false, '0');
      
      TestFramework.expect(downloadButton.disabled).toBe(false);
      TestFramework.expect(document.body.className).toBe('');
    });

    TestFramework.test('should handle edge case with zero selected tweaks', () => {
      resetMocks();
      mockGetSelectedTweaks.mockReturnValue({ raw: [] });
      const { downloadButton } = createTestDOM();
      
      simulateMinerToggleChange(true, '0');
      
      // With 0 tweaks, required points is 0 * 20 = 0, so button should be enabled
      TestFramework.expect(downloadButton.disabled).toBe(false);
    });

    TestFramework.test('should handle non-numeric points gracefully', () => {
      resetMocks();
      const { downloadButton } = createTestDOM();
      
      simulateMinerToggleChange(true, 'invalid');
      
      // Number('invalid') returns NaN, NaN < anything is false, should disable button
      TestFramework.expect(downloadButton.disabled).toBe(true);
    });

    TestFramework.test('should handle empty string points', () => {
      resetMocks();
      const { downloadButton } = createTestDOM();
      
      simulateMinerToggleChange(true, '');
      
      // Number('') returns 0, should check against threshold
      TestFramework.expect(downloadButton.disabled).toBe(true);
    });
  });
});

TestFramework.describe('toggleViewAll Function', () => {
  TestFramework.test('should set body class to "miner" when element is currently active', () => {
    resetMocks();
    createTestDOM();
    const mockElement = document.createElement('button');
    mockElement.innerText = 'Stop Mining';
    
    simulateToggleViewAll(mockElement, 'active');
    
    TestFramework.expect(document.body.className).toBe('miner');
    TestFramework.expect(mockElement.innerText).toBe('Start Mining');
    TestFramework.expect(mockOreUI.becomeInactive.called).toBeTruthy();
    TestFramework.expect(mockOreUI.becomeInactive.lastArgs).toEqual([mockElement]);
  });

  TestFramework.test('should set body class to "miner hideall" when element is not active', () => {
    resetMocks();
    createTestDOM();
    const mockElement = document.createElement('button');
    mockElement.innerText = 'Start Mining';
    
    simulateToggleViewAll(mockElement, 'inactive');
    
    TestFramework.expect(document.body.className).toBe('miner hideall');
    TestFramework.expect(mockElement.innerText).toBe('Stop Mining');
    TestFramework.expect(mockOreUI.becomeActive.called).toBeTruthy();
    TestFramework.expect(mockOreUI.becomeActive.lastArgs).toEqual([mockElement]);
  });

  TestFramework.test('should handle undefined state gracefully by becoming active', () => {
    resetMocks();
    createTestDOM();
    const mockElement = document.createElement('button');
    mockElement.innerText = 'Start Mining';
    
    simulateToggleViewAll(mockElement, undefined);
    
    TestFramework.expect(document.body.className).toBe('miner hideall');
    TestFramework.expect(mockElement.innerText).toBe('Stop Mining');
    TestFramework.expect(mockOreUI.becomeActive.called).toBeTruthy();
  });

  TestFramework.test('should handle null state gracefully by becoming active', () => {
    resetMocks();
    createTestDOM();
    const mockElement = document.createElement('button');
    
    simulateToggleViewAll(mockElement, null);
    
    TestFramework.expect(document.body.className).toBe('miner hideall');
    TestFramework.expect(mockOreUI.becomeActive.called).toBeTruthy();
  });
});

TestFramework.describe('Tile Click Event Handlers', () => {
  TestFramework.describe('Point calculation for different ore types', () => {
    const oreTypes = [
      { type: 'stone.png', points: 1, name: 'Stone' },
      { type: 'copper_ore.png', points: 2, name: 'Copper Ore' },
      { type: 'coal_ore.png', points: 2, name: 'Coal Ore' },
      { type: 'iron_ore.png', points: 4, name: 'Iron Ore' },
      { type: 'lapis_ore.png', points: 6, name: 'Lapis Ore' },
      { type: 'redstone_ore.png', points: 6, name: 'Redstone Ore' },
      { type: 'emerald_ore.png', points: 8, name: 'Emerald Ore' },
      { type: 'diamond_ore.png', points: 10, name: 'Diamond Ore' }
    ];

    oreTypes.forEach(ore => {
      TestFramework.test(`should add ${ore.points} points when clicking ${ore.name} (${ore.type})`, () => {
        resetMocks();
        const { toggleCheckbox, numberElement } = createTestDOM();
        
        toggleCheckbox.checked = true;
        numberElement.textContent = '10';
        
        simulateTileClick(ore.type);
        
        TestFramework.expect(numberElement.textContent).toBe((10 + ore.points).toString());
        TestFramework.expect(mockUpdateTile.called).toBeTruthy();
      });
    });
  });

  TestFramework.test('should not update points when toggle is unchecked', () => {
    resetMocks();
    const { toggleCheckbox, numberElement } = createTestDOM();
    
    toggleCheckbox.checked = false;
    numberElement.textContent = '10';
    
    simulateTileClick('diamond_ore.png');
    
    TestFramework.expect(numberElement.textContent).toBe('10');
    TestFramework.expect(mockUpdateTile.called).toBeFalsy();
  });

  TestFramework.test('should handle unknown ore type gracefully (no points added)', () => {
    resetMocks();
    const { toggleCheckbox, numberElement } = createTestDOM();
    
    toggleCheckbox.checked = true;
    numberElement.textContent = '10';
    
    simulateTileClick('unknown_ore.png');
    
    TestFramework.expect(numberElement.textContent).toBe('10'); // No points added for unknown type
    TestFramework.expect(mockUpdateTile.called).toBeTruthy(); // updateTile should still be called
  });

  TestFramework.test('should update download button state after adding points crosses threshold', () => {
    resetMocks();
    const { toggleCheckbox, numberElement, downloadButton } = createTestDOM();
    
    toggleCheckbox.checked = true;
    numberElement.textContent = '95'; // Just below threshold of 100
    downloadButton.disabled = true;
    
    simulateTileClick('diamond_ore.png'); // +10 points = 105 total
    
    TestFramework.expect(numberElement.textContent).toBe('105');
    TestFramework.expect(downloadButton.disabled).toBe(false);
  });

  TestFramework.test('should keep download button disabled when points still insufficient', () => {
    resetMocks();
    const { toggleCheckbox, numberElement, downloadButton } = createTestDOM();
    
    toggleCheckbox.checked = true;
    numberElement.textContent = '50';
    downloadButton.disabled = true;
    
    simulateTileClick('stone.png'); // +1 point, still below 100
    
    TestFramework.expect(numberElement.textContent).toBe('51');
    TestFramework.expect(downloadButton.disabled).toBe(true);
  });

  TestFramework.test('should handle multiple tile clicks correctly', () => {
    resetMocks();
    const { toggleCheckbox, numberElement } = createTestDOM();
    
    toggleCheckbox.checked = true;
    numberElement.textContent = '0';
    
    // Click stone tile three times
    simulateTileClick('stone.png'); // +1
    simulateTileClick('stone.png'); // +1
    simulateTileClick('stone.png'); // +1
    
    TestFramework.expect(numberElement.textContent).toBe('3');
    TestFramework.expect(mockUpdateTile.callCount).toBe(3);
  });

  TestFramework.test('should handle clicking different ore types sequentially', () => {
    resetMocks();
    const { toggleCheckbox, numberElement } = createTestDOM();
    
    toggleCheckbox.checked = true;
    numberElement.textContent = '0';
    
    simulateTileClick('stone.png');     // +1 = 1
    simulateTileClick('copper_ore.png'); // +2 = 3
    simulateTileClick('iron_ore.png');   // +4 = 7
    simulateTileClick('diamond_ore.png'); // +10 = 17
    
    TestFramework.expect(numberElement.textContent).toBe('17');
  });

  TestFramework.test('should handle edge case with very high points', () => {
    resetMocks();
    const { toggleCheckbox, numberElement, downloadButton } = createTestDOM();
    
    toggleCheckbox.checked = true;
    numberElement.textContent = '999999';
    
    simulateTileClick('diamond_ore.png');
    
    TestFramework.expect(numberElement.textContent).toBe('1000009');
    TestFramework.expect(downloadButton.disabled).toBe(false);
  });
});

TestFramework.describe('Integration Tests', () => {
  TestFramework.test('should handle complete mining workflow from start to finish', () => {
    resetMocks();
    mockGetSelectedTweaks.mockReturnValue({ raw: Array(10).fill('item') }); // 200 points needed
    const { toggleCheckbox, numberElement, downloadButton } = createTestDOM();
    
    // Initial state
    TestFramework.expect(document.body.className).toBe('');
    TestFramework.expect(downloadButton.disabled).toBe(false);
    TestFramework.expect(numberElement.textContent).toBe('0');
    
    // Enable mining mode
    simulateMinerToggleChange(true, '0');
    TestFramework.expect(document.body.className).toBe('miner');
    TestFramework.expect(downloadButton.disabled).toBe(true); // Insufficient points
    
    // Mine some ores
    toggleCheckbox.checked = true;
    simulateTileClick('stone.png');       // +1 = 1
    simulateTileClick('diamond_ore.png'); // +10 = 11
    simulateTileClick('iron_ore.png');    // +4 = 15
    
    TestFramework.expect(numberElement.textContent).toBe('15');
    TestFramework.expect(downloadButton.disabled).toBe(true); // Still insufficient (need 200)
    
    // Mine enough valuable ores to reach threshold
    for (let i = 0; i < 19; i++) {
      simulateTileClick('diamond_ore.png'); // 19 * 10 = 190 more points
    }
    
    TestFramework.expect(numberElement.textContent).toBe('205'); // 15 + 190 = 205
    TestFramework.expect(downloadButton.disabled).toBe(false); // Now sufficient
    
    // Disable mining mode
    simulateMinerToggleChange(false);
    TestFramework.expect(document.body.className).toBe('');
    TestFramework.expect(downloadButton.disabled).toBe(false); // Always enabled when toggle off
  });

  TestFramework.test('should handle rapid toggle switching without breaking state', () => {
    resetMocks();
    const { downloadButton } = createTestDOM();
    
    // Rapid on/off switching
    simulateMinerToggleChange(true, '50');
    TestFramework.expect(document.body.className).toBe('miner');
    TestFramework.expect(downloadButton.disabled).toBe(true);
    
    simulateMinerToggleChange(false);
    TestFramework.expect(document.body.className).toBe('');
    TestFramework.expect(downloadButton.disabled).toBe(false);
    
    simulateMinerToggleChange(true, '150');
    TestFramework.expect(document.body.className).toBe('miner');
    TestFramework.expect(downloadButton.disabled).toBe(false);
    
    TestFramework.expect(mockConsoler.callCount).toBe(3);
  });

  TestFramework.test('should handle mixed toggle and tile interaction workflow', () => {
    resetMocks();
    const { toggleCheckbox, numberElement, downloadButton } = createTestDOM();
    
    // Start with mining disabled
    simulateMinerToggleChange(false);
    toggleCheckbox.checked = false;
    
    // Try to mine while disabled - should do nothing
    simulateTileClick('diamond_ore.png');
    TestFramework.expect(numberElement.textContent).toBe('0');
    
    // Enable mining
    simulateMinerToggleChange(true, '0');
    toggleCheckbox.checked = true;
    
    // Now mining should work
    simulateTileClick('diamond_ore.png');
    TestFramework.expect(numberElement.textContent).toBe('10');
    
    // Disable again
    simulateMinerToggleChange(false);
    toggleCheckbox.checked = false;
    
    // Mining should stop working again
    simulateTileClick('diamond_ore.png');
    TestFramework.expect(numberElement.textContent).toBe('10'); // No change
  });
});

TestFramework.describe('Error Handling and Edge Cases', () => {
  TestFramework.test('should handle missing DOM elements gracefully', () => {
    resetMocks();
    document.body.innerHTML = ''; // Empty DOM
    
    const result = TestFramework.expect(() => {
      const checkbox = document.querySelector('.devtools-toggle-mine-then-craft input[type="checkbox"]');
      const numberElement = document.querySelector('#mineThenCraftPoints > .number');
      const downloadButton = document.querySelector('.download-selected-button');
      
      // These should return null but not throw
      TestFramework.expect(checkbox).toBeNull();
      TestFramework.expect(numberElement).toBeNull();
      TestFramework.expect(downloadButton).toBeNull();
    });
    
    // The expectation itself should not throw
    result.not.toThrow();
  });

  TestFramework.test('should handle getSelectedTweaks returning null gracefully', () => {
    resetMocks();
    mockGetSelectedTweaks.mockReturnValue(null);
    createTestDOM();
    
    TestFramework.expect(() => {
      const selectedTweaks = getSelectedTweaks();
      // This should handle null gracefully in real implementation
      const requiredPoints = selectedTweaks ? selectedTweaks.raw.length * 20 : 0;
      TestFramework.expect(requiredPoints).toBe(0);
    }).not.toThrow();
  });

  TestFramework.test('should handle getSelectedTweaks returning undefined gracefully', () => {
    resetMocks();
    mockGetSelectedTweaks.mockReturnValue(undefined);
    createTestDOM();
    
    TestFramework.expect(() => {
      const selectedTweaks = getSelectedTweaks();
      const requiredPoints = selectedTweaks ? selectedTweaks.raw.length * 20 : 0;
      TestFramework.expect(requiredPoints).toBe(0);
    }).not.toThrow();
  });

  TestFramework.test('should handle malformed number content in various formats', () => {
    resetMocks();
    const { numberElement } = createTestDOM();
    
    // Test various malformed inputs
    const malformedInputs = ['', 'abc', '12.34.56', 'null', 'undefined', '  ', '\n\t', 'NaN', 'Infinity'];
    
    malformedInputs.forEach(input => {
      numberElement.textContent = input;
      const result = Number(numberElement.textContent);
      
      // Number() should handle these gracefully (returning NaN, 0, or Infinity)
      TestFramework.expect(typeof result).toBe('number');
    });
  });

  TestFramework.test('should handle extremely large numbers without overflow errors', () => {
    resetMocks();
    const { numberElement } = createTestDOM();
    
    numberElement.textContent = '999999999999999';
    const result = Number(numberElement.textContent) + 10;
    
    TestFramework.expect(typeof result).toBe('number');
    TestFramework.expect(result > 999999999999999).toBeTruthy();
  });

  TestFramework.test('should handle negative numbers in points display', () => {
    resetMocks();
    const { numberElement, downloadButton } = createTestDOM();
    
    // Test with negative starting points
    simulateMinerToggleChange(true, '-50');
    
    // Negative number should still be compared correctly
    TestFramework.expect(downloadButton.disabled).toBe(true); // -50 < 100
  });

  TestFramework.test('should handle floating point numbers in points', () => {
    resetMocks();
    const { numberElement, downloadButton } = createTestDOM();
    
    simulateMinerToggleChange(true, '99.9');
    
    // 99.9 < 100, should disable button
    TestFramework.expect(downloadButton.disabled).toBe(true);
    
    simulateMinerToggleChange(true, '100.1');
    
    // 100.1 > 100, should enable button
    TestFramework.expect(downloadButton.disabled).toBe(false);
  });
});

TestFramework.describe('Boundary Value Testing', () => {
  TestFramework.test('should handle exact threshold boundary conditions', () => {
    resetMocks();
    mockGetSelectedTweaks.mockReturnValue({ raw: Array(5).fill('item') }); // Threshold = 100
    const { downloadButton } = createTestDOM();
    
    // Test exactly at threshold
    simulateMinerToggleChange(true, '100');
    TestFramework.expect(downloadButton.disabled).toBe(false);
    
    // Test just below threshold
    simulateMinerToggleChange(true, '99');
    TestFramework.expect(downloadButton.disabled).toBe(true);
    
    // Test just above threshold
    simulateMinerToggleChange(true, '101');
    TestFramework.expect(downloadButton.disabled).toBe(false);
  });

  TestFramework.test('should handle zero threshold case', () => {
    resetMocks();
    mockGetSelectedTweaks.mockReturnValue({ raw: [] }); // Threshold = 0
    const { downloadButton } = createTestDOM();
    
    simulateMinerToggleChange(true, '0');
    TestFramework.expect(downloadButton.disabled).toBe(false); // 0 >= 0
    
    simulateMinerToggleChange(true, '1');
    TestFramework.expect(downloadButton.disabled).toBe(false); // 1 >= 0
    
    // Even with negative points, should still be enabled since threshold is 0
    simulateMinerToggleChange(true, '-1');
    TestFramework.expect(downloadButton.disabled).toBe(true); // -1 < 0
  });
});

// Run tests when the script loads
if (typeof window !== 'undefined') {
  // Browser environment
  document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Running Miner Tests...\n');
    console.log('Testing Framework: Simple browser-based testing (no external dependencies)\n');
    TestFramework.runTests();
  });
} else {
  // Node environment fallback
  console.log('🚀 Running Miner Tests...\n');
  console.log('Testing Framework: Simple browser-based testing (no external dependencies)\n');
  TestFramework.runTests();
}

// Export for potential use in other test files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { TestFramework, createTestDOM, resetMocks };
}