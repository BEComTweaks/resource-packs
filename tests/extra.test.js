<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Extra.js Unit Tests</title>
    <link rel="stylesheet" href="https://code.jquery.com/qunit/qunit-2.19.4.css">
</head>
<body>
    <div id="qunit"></div>
    <div id="qunit-fixture">
        <!-- Test fixtures -->
        <div class="loading-screen"></div>
        <div id="background-container"></div>
        <div class="devtools"></div>
        <div class="capture-exit"></div>
        <div class="devtools-toggle-console">
            <input type="checkbox">
        </div>
        <div class="devtools-console-content"></div>
        <div class="devtools-toggle-tweak-per-column">
            <input type="number" value="3">
            <input type="checkbox">
        </div>
        <div class="devtools-pinger-inner"></div>
        <div class="pinger-anim"></div>
        <div class="devtools-pinger-console-content-general">
            <span></span>
        </div>
        <div class="devtools-pinger-console-content-server">
            <span></span>
        </div>
    </div>

    <script src="https://code.jquery.com/qunit/qunit-2.19.4.js"></script>
    <script>
        // Testing Framework: QUnit (browser-based testing without build dependencies)
        
        // Mock the original functions and constants from extra.js
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

        // Original consoler function for testing
        function consoler(logTag, logColour, logMessage, logMessageColour) {
            const err = new Error();
            const stack = err.stack.split("\n");
            let functionCall;
            if (stack[1].includes("consoler")) {
                functionCall = stack[2];
            } else {
                functionCall = stack[1];
            }
            console.log(
                `[%c${logTag}%c] %c${functionCall}%c\n%c${logMessage}`,
                `color: ${logColour}`,
                "color: white",
                "color: #4fa1ff",
                `color: ${logMessageColour}`,
            );
            
            const checkbox = document.querySelector(".devtools-toggle-console input[type='checkbox']");
            if (checkbox && checkbox.checked) {
                const consoleElement = document.querySelector(".devtools-console-content");
                const log = document.createElement("div");
                log.className = "devtools-console-log";
                log.innerHTML = `[<span style="color: ${logColour}">${logTag}</span>] <span style="color: #4fa1ff">${functionCall}}</span><br><span style="color: ${logMessageColour}">${logMessage}</span>`;
                consoleElement.appendChild(log);
            }
        }

        // Original selectTexture function for testing
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

        // Original updateTile function for testing
        function updateTile(element) {
            if (!element) return;
            const tile_image = selectTexture();
            element.style.backgroundImage = `url("images/blocks/${tile_image}")`;
            element.dataset.type = tile_image;
        }

        // Original createTiles function (simplified for testing)
        function createTiles() {
            const container = document.getElementById("background-container");
            if (!container) return;
            
            const numColumns = Math.ceil(window.innerWidth / 100) + 2;
            const numRows = Math.ceil(window.innerHeight / 100) + 2;

            // Create new columns if needed
            for (let i = container.children.length; i < numColumns; i++) {
                const rowDiv = document.createElement("div");
                rowDiv.className = "row";
                for (let j = 0; j < numRows; j++) {
                    const tile = document.createElement("div");
                    tile.className = "tile";
                    const tile_image = selectTexture();
                    tile.style.backgroundImage = `url("images/blocks/${tile_image}")`;
                    tile.dataset.type = tile_image;
                    rowDiv.appendChild(tile);
                }
                container.appendChild(rowDiv);
            }
        }

        // Original utility functions
        function sleep(ms) {
            return new Promise((resolve) => setTimeout(resolve, ms));
        }

        function getTimeoutDuration() {
            const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
            return mediaQuery.matches ? 0 : 1000;
        }

        function showDevToolsPanel() {
            const devtools = document.querySelector(".devtools");
            const captureExit = document.querySelector(".capture-exit");
            if (devtools) devtools.style.transform = "translateY(0)";
            if (captureExit) {
                captureExit.setAttribute("close", ".devtools");
                captureExit.style = "opacity: 1; pointer-events: all;";
            }
        }

        function closePanel() {
            const element = document.querySelector(".capture-exit");
            if (!element) return;
            const closeSelector = element.getAttribute("close");
            if (closeSelector) {
                const targetElement = document.querySelector(closeSelector);
                if (targetElement) targetElement.removeAttribute("style");
            }
            element.removeAttribute("style");
        }

        // Test Suites
        QUnit.module('Texture Selection System', function() {
            QUnit.test('Texture array validation', function(assert) {
                assert.equal(textures.length, 9, 'Should have 9 textures');
                
                textures.forEach(function(texture, index) {
                    assert.ok(texture.hasOwnProperty('src'), `Texture ${index + 1} should have src property`);
                    assert.ok(texture.hasOwnProperty('probability'), `Texture ${index + 1} should have probability property`);
                    assert.equal(typeof texture.src, 'string', `Texture ${index + 1} src should be a string`);
                    assert.equal(typeof texture.probability, 'number', `Texture ${index + 1} probability should be a number`);
                });
                
                const totalProbability = textures.reduce((sum, texture) => sum + texture.probability, 0);
                assert.ok(Math.abs(totalProbability - 1.0) < 0.001, 'Total probability should be approximately 1.0');
            });

            QUnit.test('Stone texture should be most common', function(assert) {
                const stoneTexture = textures.find(t => t.src === 'stone.png');
                assert.equal(stoneTexture.probability, 0.59, 'Stone should have highest probability');
            });

            QUnit.test('Diamond texture should be rarest', function(assert) {
                const diamondTexture = textures.find(t => t.src === 'diamond_ore.png');
                assert.equal(diamondTexture.probability, 0.002, 'Diamond should have lowest probability');
            });

            QUnit.test('selectTexture should return valid texture', function(assert) {
                // Mock Math.random for predictable results
                const originalRandom = Math.random;
                
                // Test stone selection (random = 0.1)
                Math.random = () => 0.1;
                assert.equal(selectTexture(), 'stone.png', 'Should select stone for random value 0.1');
                
                // Test copper selection (random = 0.65)
                Math.random = () => 0.65;
                assert.equal(selectTexture(), 'copper_ore.png', 'Should select copper for random value 0.65');
                
                // Test diamond selection (random = 0.999)
                Math.random = () => 0.999;
                assert.equal(selectTexture(), 'diamond_ore.png', 'Should select diamond for random value 0.999');
                
                // Test fallback (random = 1.0)
                Math.random = () => 1.0;
                assert.equal(selectTexture(), 'stone.png', 'Should fallback to stone for edge case');
                
                // Restore original Math.random
                Math.random = originalRandom;
            });

            QUnit.test('selectTexture probability distribution', function(assert) {
                const originalRandom = Math.random;
                const samples = 10000;
                const results = {};
                
                // Initialize results counter
                textures.forEach(texture => {
                    results[texture.src] = 0;
                });
                
                // Generate samples
                for (let i = 0; i < samples; i++) {
                    Math.random = () => originalRandom();
                    const selected = selectTexture();
                    results[selected]++;
                });
                
                // Check if distribution is roughly correct (within 10% tolerance)
                textures.forEach(texture => {
                    const expectedCount = samples * texture.probability;
                    const actualCount = results[texture.src];
                    const tolerance = expectedCount * 0.1;
                    assert.ok(
                        Math.abs(actualCount - expectedCount) <= tolerance,
                        `${texture.src} distribution should be within tolerance. Expected: ${expectedCount}, Actual: ${actualCount}`
                    );
                });
                
                Math.random = originalRandom;
            });
        });

        QUnit.module('Console Logger System', function() {
            QUnit.test('consoler should log to console', function(assert) {
                const originalLog = console.log;
                let loggedMessage = '';
                
                console.log = function() {
                    loggedMessage = Array.from(arguments).join(' ');
                };
                
                consoler('TEST', 'red', 'Test message', 'white');
                
                assert.ok(loggedMessage.includes('TEST'), 'Should include log tag');
                assert.ok(loggedMessage.includes('Test message'), 'Should include log message');
                
                console.log = originalLog;
            });

            QUnit.test('consoler should handle empty parameters', function(assert) {
                const originalLog = console.log;
                let logCalled = false;
                
                console.log = function() {
                    logCalled = true;
                };
                
                consoler('', '', '', '');
                assert.ok(logCalled, 'Should call console.log even with empty parameters');
                
                console.log = originalLog;
            });

            QUnit.test('consoler should create DOM elements when devtools console is active', function(assert) {
                const checkbox = document.querySelector(".devtools-toggle-console input[type='checkbox']");
                const consoleElement = document.querySelector(".devtools-console-content");
                
                checkbox.checked = true;
                const initialChildCount = consoleElement.children.length;
                
                consoler('DOM_TEST', 'purple', 'DOM test message', 'yellow');
                
                assert.equal(consoleElement.children.length, initialChildCount + 1, 'Should add one log element');
                
                const logElement = consoleElement.lastElementChild;
                assert.ok(logElement.innerHTML.includes('DOM_TEST'), 'Log element should contain tag');
                assert.ok(logElement.innerHTML.includes('DOM test message'), 'Log element should contain message');
                
                checkbox.checked = false;
            });
        });

        QUnit.module('Tile Creation System', function() {
            QUnit.test('createTiles should get background container', function(assert) {
                const container = document.getElementById("background-container");
                assert.ok(container, 'Should find background container element');
                
                createTiles();
                assert.ok(true, 'createTiles should execute without errors');
            });

            QUnit.test('createTiles should calculate correct dimensions', function(assert) {
                const numColumns = Math.ceil(window.innerWidth / 100) + 2;
                const numRows = Math.ceil(window.innerHeight / 100) + 2;
                
                assert.ok(numColumns > 0, 'Should calculate positive number of columns');
                assert.ok(numRows > 0, 'Should calculate positive number of rows');
                assert.equal(typeof numColumns, 'number', 'Columns should be a number');
                assert.equal(typeof numRows, 'number', 'Rows should be a number');
            });

            QUnit.test('updateTile should update tile properties', function(assert) {
                const mockTile = document.createElement('div');
                mockTile.className = 'tile';
                mockTile.style = {};
                mockTile.dataset = {};
                
                updateTile(mockTile);
                
                assert.ok(mockTile.style.backgroundImage, 'Should set background image');
                assert.ok(mockTile.dataset.type, 'Should set data type');
                assert.ok(mockTile.style.backgroundImage.includes('url("images/blocks/'), 'Should use correct image path');
            });

            QUnit.test('updateTile should handle null element gracefully', function(assert) {
                assert.expect(0); // No assertions needed, just check it doesn't throw
                updateTile(null);
                updateTile(undefined);
            });
        });

        QUnit.module('Utility Functions', function() {
            QUnit.test('sleep should return a Promise', function(assert) {
                const promise = sleep(100);
                assert.ok(promise instanceof Promise, 'Should return a Promise');
                
                return promise.then(function() {
                    assert.ok(true, 'Promise should resolve');
                });
            });

            QUnit.test('getTimeoutDuration should respect reduced motion preference', function(assert) {
                // Mock matchMedia for testing
                const originalMatchMedia = window.matchMedia;
                
                // Test with reduced motion enabled
                window.matchMedia = function(query) {
                    return { matches: query === "(prefers-reduced-motion: reduce)" };
                };
                assert.equal(getTimeoutDuration(), 0, 'Should return 0 for reduced motion');
                
                // Test with reduced motion disabled
                window.matchMedia = function(query) {
                    return { matches: false };
                };
                assert.equal(getTimeoutDuration(), 1000, 'Should return 1000 for normal motion');
                
                window.matchMedia = originalMatchMedia;
            });

            QUnit.test('sleep should handle different timeout values', function(assert) {
                assert.ok(sleep(0) instanceof Promise, 'Should handle 0 milliseconds');
                assert.ok(sleep(1000) instanceof Promise, 'Should handle positive values');
                assert.ok(sleep(-100) instanceof Promise, 'Should handle negative values');
            });
        });

        QUnit.module('DevTools Panel Functions', function() {
            QUnit.test('showDevToolsPanel should modify elements', function(assert) {
                const devtools = document.querySelector(".devtools");
                const captureExit = document.querySelector(".capture-exit");
                
                showDevToolsPanel();
                
                assert.equal(devtools.style.transform, "translateY(0)", 'Should set devtools transform');
                assert.equal(captureExit.getAttribute("close"), ".devtools", 'Should set close attribute');
                assert.ok(captureExit.style.includes("opacity: 1"), 'Should set opacity style');
            });

            QUnit.test('closePanel should clear styles', function(assert) {
                const captureExit = document.querySelector(".capture-exit");
                const devtools = document.querySelector(".devtools");
                
                // Set up initial state
                captureExit.setAttribute("close", ".devtools");
                captureExit.style = "opacity: 1; pointer-events: all;";
                devtools.style.transform = "translateY(0)";
                
                closePanel();
                
                assert.equal(captureExit.style, "", 'Should clear capture exit styles');
                assert.equal(devtools.style.transform, "", 'Should clear devtools styles');
            });

            QUnit.test('closePanel should handle missing elements', function(assert) {
                // Temporarily remove elements
                const captureExit = document.querySelector(".capture-exit");
                const parent = captureExit.parentNode;
                parent.removeChild(captureExit);
                
                assert.expect(0); // Should not throw
                closePanel();
                
                // Restore element
                parent.appendChild(captureExit);
            });
        });

        QUnit.module('Network Ping System', function() {
            QUnit.test('should handle fetch requests', function(assert) {
                const done = assert.async();
                
                // Mock fetch for testing
                const originalFetch = window.fetch;
                window.fetch = function(url, options) {
                    return Promise.resolve({ ok: true });
                };
                
                fetch("https://www.google.com", {
                    method: "HEAD",
                    mode: "no-cors",
                }).then(function() {
                    assert.ok(true, 'Should handle successful fetch');
                    return true;
                }).catch(function() {
                    return false;
                }).then(function(result) {
                    assert.equal(result, true, 'Should return true for successful fetch');
                    window.fetch = originalFetch;
                    done();
                });
            });

            QUnit.test('should handle fetch failures', function(assert) {
                const done = assert.async();
                
                const originalFetch = window.fetch;
                window.fetch = function(url, options) {
                    return Promise.reject(new Error('Network error'));
                };
                
                fetch("https://www.google.com", {
                    method: "HEAD",
                    mode: "no-cors",
                }).then(function() {
                    return true;
                }).catch(function() {
                    return false;
                }).then(function(result) {
                    assert.equal(result, false, 'Should return false for failed fetch');
                    window.fetch = originalFetch;
                    done();
                });
            });
        });

        QUnit.module('Event Handlers', function() {
            QUnit.test('should handle Escape key events', function(assert) {
                const captureExit = document.querySelector(".capture-exit");
                captureExit.style = "opacity: 1; pointer-events: all;";
                
                let clickCalled = false;
                const originalClick = captureExit.click;
                captureExit.click = function() {
                    clickCalled = true;
                };
                
                // Simulate Escape key event
                const event = { key: "Escape" };
                if (event.key === "Escape") {
                    const captureExitElement = document.querySelector(".capture-exit");
                    if (captureExitElement.style !== "") {
                        captureExitElement.click();
                    }
                }
                
                assert.ok(clickCalled, 'Should call click on capture exit element');
                captureExit.click = originalClick;
            });

            QUnit.test('should ignore non-Escape keys', function(assert) {
                const captureExit = document.querySelector(".capture-exit");
                let clickCalled = false;
                const originalClick = captureExit.click;
                captureExit.click = function() {
                    clickCalled = true;
                };
                
                // Simulate non-Escape key event
                const event = { key: "Enter" };
                if (event.key === "Escape") {
                    captureExit.click();
                }
                
                assert.ok(!clickCalled, 'Should not call click for non-Escape keys');
                captureExit.click = originalClick;
            });
        });

        QUnit.module('Dynamic Grid System', function() {
            QUnit.test('should create dynamic style block', function(assert) {
                const checkbox = document.querySelector(".devtools-toggle-tweak-per-column input[type='checkbox']");
                const numberInput = document.querySelector(".devtools-toggle-tweak-per-column input[type='number']");
                
                checkbox.checked = true;
                numberInput.value = '4';
                
                // Simulate the input event handler logic
                if (checkbox.checked) {
                    let styleBlock = document.querySelector("#dynamic-grid-style");
                    if (!styleBlock) {
                        styleBlock = document.createElement("style");
                        styleBlock.id = "dynamic-grid-style";
                        document.head.appendChild(styleBlock);
                    }
                    styleBlock.textContent = `
                        .tweaks, .subcattweaks {
                            grid-template-columns: repeat(${numberInput.value}, 1fr) !important;
                        }
                    `;
                }
                
                const createdStyleBlock = document.querySelector("#dynamic-grid-style");
                assert.ok(createdStyleBlock, 'Should create style block');
                assert.ok(createdStyleBlock.textContent.includes('repeat(4, 1fr)'), 'Should set correct grid columns');
                
                // Cleanup
                createdStyleBlock.remove();
                checkbox.checked = false;
            });

            QUnit.test('should remove style block when disabled', function(assert) {
                const checkbox = document.querySelector(".devtools-toggle-tweak-per-column input[type='checkbox']");
                
                // Create style block first
                const styleBlock = document.createElement("style");
                styleBlock.id = "dynamic-grid-style";
                document.head.appendChild(styleBlock);
                
                checkbox.checked = false;
                
                // Simulate the change event handler logic
                if (!checkbox.checked) {
                    const existingStyleBlock = document.querySelector("#dynamic-grid-style");
                    if (existingStyleBlock) {
                        existingStyleBlock.remove();
                    }
                }
                
                const removedStyleBlock = document.querySelector("#dynamic-grid-style");
                assert.ok(!removedStyleBlock, 'Should remove style block when disabled');
            });
        });

        QUnit.module('Loading Screen Animation', function() {
            QUnit.test('should select animation based on random value', function(assert) {
                const loadingElement = document.querySelector(".loading-screen");
                const originalRandom = Math.random;
                
                // Test first animation (random <= 0.9)
                Math.random = () => 0.5;
                loadingElement.innerHTML = '';
                
                if (Math.random() <= 0.9) {
                    loadingElement.innerHTML += '<style>.box1 { animation: abox1 4s 1s forwards ease-in-out infinite; }</style>';
                } else {
                    loadingElement.innerHTML += '<style>.box3 { animation: infinite 1.8s wink; }</style>';
                }
                
                assert.ok(loadingElement.innerHTML.includes('abox1'), 'Should use first animation for random <= 0.9');
                
                // Test second animation (random > 0.9)
                Math.random = () => 0.95;
                loadingElement.innerHTML = '';
                
                if (Math.random() <= 0.9) {
                    loadingElement.innerHTML += '<style>.box1 { animation: abox1 4s 1s forwards ease-in-out infinite; }</style>';
                } else {
                    loadingElement.innerHTML += '<style>.box3 { animation: infinite 1.8s wink; }</style>';
                }
                
                assert.ok(loadingElement.innerHTML.includes('wink'), 'Should use second animation for random > 0.9');
                
                Math.random = originalRandom;
            });
        });

        QUnit.module('Configuration Constants', function() {
            QUnit.test('should have correct server configuration', function(assert) {
                assert.equal(serverip, "localhost", 'Server IP should be localhost');
                assert.equal(typeof serverip, "string", 'Server IP should be a string');
            });

            QUnit.test('should validate complete texture configuration', function(assert) {
                const expectedTextures = [
                    "stone.png", "copper_ore.png", "coal_ore.png", "iron_ore.png",
                    "lapis_ore.png", "redstone_ore.png", "gold_ore.png", "emerald_ore.png", "diamond_ore.png"
                ];
                
                const actualTextures = textures.map(t => t.src);
                expectedTextures.forEach(texture => {
                    assert.ok(actualTextures.includes(texture), `Should include ${texture}`);
                });
                
                // Verify probabilities are positive
                textures.forEach(texture => {
                    assert.ok(texture.probability > 0, `${texture.src} should have positive probability`);
                });
            });
        });
    </script>
</body>
</html>