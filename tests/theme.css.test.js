const { test, expect } = require('@playwright/test');

test.describe('OreUI Theme CSS Comprehensive Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Load the complete CSS theme from the source file
    const cssContent = `
      /* Custom Font */
      @font-face {
        font-family: "Futura Heavy";
        src: url("font/Futura_Heavy.ttf") format("truetype");
        font-weight: normal;
        font-style: normal;
      }
      @font-face {
        font-family: "Futura Medium";
        src: url("font/Futura_Medium.ttf") format("truetype");
        font-weight: normal;
        font-style: normal;
      }
      @font-face {
        font-family: "CaskaydiaMono";
        src: url("font/CaskaydiaMono_Regular.ttf") format("truetype");
        font-weight: normal;
        font-style: normal;
      }

      /* CSS Root Variables */
      :root {
        --light-bg: rgb(208, 209, 212);
        --light-border: rgb(222, 223, 225) rgb(227, 227, 229) rgb(227, 227, 229) rgb(222, 223, 225);
        --light-bezel: rgb(98, 98, 100);
        --dark-bg: rgb(72, 73, 74);
        --dark-border: rgb(106, 108, 112) rgb(84, 86, 88) rgb(84, 86, 88) rgb(106, 108, 112);
        --dark-bezel: rgb(49, 50, 51);
        --outer-bezel-black: black;
        --green-bg: rgb(60, 133, 39);
        --green-border: rgb(99, 157, 82) rgb(79, 145, 60) rgb(79, 145, 60) rgb(99, 157, 82);
        --green-bezel: rgb(52, 84, 43);
        --light-disabled-bg: rgb(208, 209, 212);
        --light-disabled-border: rgb(208, 209, 212);
        --light-disabled-bezel: rgb(177, 178, 181);
        --outer-bezel-light-disabled: rgb(140, 141, 144);
        --dark-disabled-bg: rgb(53, 54, 55);
        --dark-disabled-border: rgb(78, 80, 83) rgb(62, 64, 65) rgb(62, 64, 65) rgb(78, 80, 83);
        --dark-disabled-bezel: rgb(36, 37, 38);
        --pink-bg: rgb(255, 186, 231);
        --pink-border: rgb(255, 235, 248) rgb(245, 215, 235) rgb(245, 215, 235) rgb(255, 235, 248);
        --pink-bezel: rgb(117, 38, 89);
        --outer-bezel-pink: rgb(55, 18, 42);
        --red-bg: rgb(214, 71, 71);
        --red-border: rgb(224, 114, 114) rgb(173, 29, 29) rgb(173, 29, 29) rgb(224, 114, 114);
        --red-bezel: rgb(96, 24, 25);
        --purple-bg: rgb(115, 69, 229);
        --purple-border: rgb(162, 100, 242) rgb(142, 73, 235) rgb(142, 73, 235) rgb(162, 100, 242);
        --purple-bezel: rgb(74, 28, 172);
        --padding: 5px 15px;
        --bezel-size: 5px;
        --hover-overlay: rgba(0, 0, 0, 0.05);
        --dark-zero: rgb(61, 62, 63);
        --leftmargin: 15px;
        --rightmargin: 250px;
        --font: "Futura Medium", white;
        --transition-duration: 1s;
      }

      /* OreUI Button Components */
      [oreui-type="button"] {
        border-width: 5px;
        border-style: solid;
        border-radius: 0;
        cursor: pointer;
        padding: var(--padding);
        transform: translateY(-1px);
        text-align: center;
        transition: border-color 0s, background-color 0s;
        position: relative;
      }

      [oreui-type="button"]::before {
        position: absolute;
        content: "";
        bottom: calc(-3px - var(--bezel-size));
        left: -3px;
        right: -3px;
        height: var(--bezel-size);
        transform: translateY(0);
        pointer-events: none;
      }

      [oreui-type="button"]:hover::before {
        height: 0;
      }

      [oreui-type="button"]:active::before,
      [oreui-type="button"][oreui-state="active"]::before {
        height: 0;
      }

      [oreui-type="button"]:not(:active):not(:hover):not([oreui-state="active"]) {
        transform: translateY(calc(-1px - var(--bezel-size)));
      }

      [oreui-type="button"]::after {
        position: absolute;
        content: "";
        border-style: solid;
        border-width: 2.5px;
        bottom: calc(-5px - var(--bezel-size));
        left: -5px;
        right: -5px;
        top: -5px;
        pointer-events: none;
      }

      [oreui-type="button"]:hover::after,
      [oreui-type="button"]:active::after,
      [oreui-type="button"][oreui-state="active"]::after {
        bottom: -5px;
      }

      [oreui-type="button"]:hover::after {
        background: var(--hover-overlay);
      }

      /* Color Variants */
      [oreui-color="red"] {
        background-color: var(--red-bg);
        border-color: var(--red-border);
        color: white;
      }

      [oreui-color="pink"] {
        background-color: var(--pink-bg);
        border-color: var(--pink-border);
        color: black;
      }

      [oreui-color="purple"] {
        background-color: var(--purple-bg);
        border-color: var(--purple-border);
        color: white;
      }

      [oreui-color="green"] {
        background-color: var(--green-bg);
        border-color: var(--green-border);
        color: white;
      }

      [oreui-color="light"] {
        background-color: var(--light-bg);
        border-color: var(--light-border);
        color: black;
      }

      [oreui-color="dark"] {
        background-color: var(--dark-bg);
        border-color: var(--dark-border);
        color: white;
      }

      /* Active Color States */
      [oreui-active-color="red"]:active,
      [oreui-active-color="red"][oreui-state="active"] {
        background-color: var(--red-bg);
        border-color: var(--red-border);
        color: white;
      }

      [oreui-active-color="pink"]:active,
      [oreui-active-color="pink"][oreui-state="active"] {
        background-color: var(--pink-bg);
        border-color: var(--pink-border);
        color: black;
      }

      [oreui-active-color="purple"]:active,
      [oreui-active-color="purple"][oreui-state="active"] {
        background-color: var(--purple-bg);
        border-color: var(--purple-border);
        color: white;
      }

      [oreui-active-color="green"]:active,
      [oreui-active-color="green"][oreui-state="active"] {
        background-color: var(--green-bg);
        border-color: var(--green-border);
        color: white;
      }

      [oreui-active-color="light"]:active,
      [oreui-active-color="light"][oreui-state="active"] {
        background-color: var(--light-bg);
        border-color: var(--light-border);
        color: black;
      }

      [oreui-active-color="dark"]:active,
      [oreui-active-color="dark"][oreui-state="active"] {
        background-color: var(--dark-bg);
        border-color: var(--dark-border);
        color: white;
      }

      /* Disabled States */
      [oreui-type="button"][disabled],
      [oreui-type="button"][disabled="true"],
      [oreui-type="button"]:disabled {
        color: white;
        background-color: var(--dark-disabled-bg) !important;
        border-color: var(--dark-disabled-border) !important;
        cursor: not-allowed;
      }

      [oreui-type="button"][disabled][oreui-disabled-color="light"],
      [oreui-type="button"][disabled="true"][oreui-disabled-color="light"],
      [oreui-type="button"]:disabled[oreui-disabled-color="light"] {
        color: black;
        background-color: var(--light-disabled-bg) !important;
        border-color: var(--light-disabled-border) !important;
      }

      /* General Components */
      [oreui-type="general"] {
        border-width: 5px;
        border-style: solid;
        border-radius: 0;
        padding: var(--padding);
        text-align: center;
        outline: 2.5px solid var(--outer-bezel-black);
        outline-offset: -2px;
      }

      /* Input Components */
      [oreui-type="input"] {
        background: rgb(51, 51, 51);
        outline: 2.5px solid var(--outer-bezel-black);
        box-shadow: inset 0 5px 0 0 rgb(35, 35, 35);
        outline-offset: -2px;
        color: white;
        padding: 10px;
        border: none;
      }

      [oreui-type="input"]:focus {
        outline-color: white;
        outline-offset: -0.5px;
      }

      [oreui-type="input"]::placeholder {
        color: white;
      }

      [oreui-type="input"][disabled="true"],
      [oreui-type="input"]:disabled {
        background: color-mix(in srgb, rgb(51, 51, 51), black);
        color: gray;
        box-shadow: inset 0 5px 0 0 color-mix(in srgb, rgb(35, 35, 35), black);
      }

      [oreui-type="input"][disabled="true"]::placeholder,
      [oreui-type="input"]:disabled::placeholder {
        color: gray;
      }

      /* Base Styles */
      body {
        color: white;
        font-family: var(--font);
        margin: 0;
        padding: 0;
      }

      button {
        color: white;
        font-family: var(--font);
      }

      input {
        color: white;
        font-family: var(--font);
      }

      select {
        color: white;
        font-family: var(--font);
        text-align: center;
        text-align-last: center;
      }

      /* Search Components */
      .search-container {
        margin: 0;
        text-align: center;
        position: relative;
        height: 37.5px;
        display: flex;
        flex-direction: row;
      }

      .search-results {
        margin: 5px auto;
        padding: 13.75px 10px 0 10px;
        border-radius: 5px;
        position: absolute;
        left: 0;
        right: 0;
        top: 42.5px;
        z-index: 100;
      }

      .search-results[hasmatches="true"] {
        display: block;
      }

      .search-results:not(:hover) {
        display: none;
      }

      /* Animations */
      @keyframes radar81 {
        0% {
          transform: rotate(-90deg);
        }
        100% {
          transform: rotate(270deg);
        }
      }

      .pinger-anim {
        position: relative;
        width: 100px;
        height: 100px;
        background: transparent;
        border-radius: 50%;
        box-shadow: 0 0 75px rgba(0, 0, 0, 0.55);
        border: 1px solid #333;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
      }

      .pinger-anim span {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 50%;
        height: 100%;
        background: transparent;
        transform-origin: top left;
        animation: radar81 2s linear infinite;
        animation-play-state: paused;
        border-top: 2px dotted #fff;
      }

      .pinger-anim[spin] span {
        animation-play-state: running;
      }

      /* Media Queries */
      @media (max-width: 767px) {
        .large-nav {
          display: block;
          transform: translateY(-100%);
        }
        .small-nav {
          display: block;
          transform: translateY(0%);
        }
      }

      @media (min-width: 768px) {
        body {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        .large-nav {
          display: block;
          transform: translateY(0%);
        }
        .small-nav {
          display: block;
          transform: translateY(-100%);
        }
      }
    `;

    await page.setContent(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OreUI Theme Test</title>
        <style>${cssContent}</style>
      </head>
      <body>
        <div id="test-container">
          <!-- Button Tests -->
          <button oreui-type="button" oreui-color="red" id="red-button">Red Button</button>
          <button oreui-type="button" oreui-color="pink" id="pink-button">Pink Button</button>
          <button oreui-type="button" oreui-color="purple" id="purple-button">Purple Button</button>
          <button oreui-type="button" oreui-color="green" id="green-button">Green Button</button>
          <button oreui-type="button" oreui-color="light" id="light-button">Light Button</button>
          <button oreui-type="button" oreui-color="dark" id="dark-button">Dark Button</button>
          
          <!-- Disabled Button Tests -->
          <button oreui-type="button" disabled id="disabled-button">Disabled Button</button>
          <button oreui-type="button" disabled oreui-disabled-color="light" id="disabled-light-button">Disabled Light</button>
          
          <!-- Active State Tests -->
          <button oreui-type="button" oreui-active-color="green" id="active-green-button">Active Green</button>
          <button oreui-type="button" oreui-state="active" oreui-color="red" id="static-active-button">Static Active</button>
          
          <!-- Input Tests -->
          <input oreui-type="input" id="test-input" placeholder="Test input">
          <input oreui-type="input" disabled id="disabled-input" placeholder="Disabled input">
          
          <!-- General Component Tests -->
          <div oreui-type="general" id="general-component">General Component</div>
          
          <!-- Search Component Tests -->
          <div class="search-container" id="search-container">
            <input id="searchBar" type="text" placeholder="Search...">
            <div class="search-results" id="search-results" hasmatches="false">
              <div class="search-result-item">Result 1</div>
            </div>
          </div>
          
          <!-- Animation Tests -->
          <div class="pinger-anim" id="pinger">
            <span></span>
          </div>
          
          <!-- Navigation Tests -->
          <nav class="large-nav" id="large-nav">Large Nav</nav>
          <nav class="small-nav" id="small-nav">Small Nav</nav>
        </div>
      </body>
      </html>
    `);
  });

  test.describe('CSS Custom Properties', () => {
    test('all CSS variables are properly defined', async ({ page }) => {
      const rootStyles = await page.evaluate(() => {
        const root = document.documentElement;
        const computedStyle = getComputedStyle(root);
        const vars = {};
        
        // Test all major CSS variables
        const varNames = [
          '--light-bg', '--dark-bg', '--red-bg', '--pink-bg', '--purple-bg', '--green-bg',
          '--light-bezel', '--dark-bezel', '--red-bezel', '--pink-bezel', '--purple-bezel', '--green-bezel',
          '--padding', '--bezel-size', '--hover-overlay', '--leftmargin', '--rightmargin', '--font', '--transition-duration'
        ];
        
        varNames.forEach(varName => {
          vars[varName] = computedStyle.getPropertyValue(varName).trim();
        });
        
        return vars;
      });

      // Validate color variables
      expect(rootStyles['--light-bg']).toBe('rgb(208, 209, 212)');
      expect(rootStyles['--dark-bg']).toBe('rgb(72, 73, 74)');
      expect(rootStyles['--red-bg']).toBe('rgb(214, 71, 71)');
      expect(rootStyles['--pink-bg']).toBe('rgb(255, 186, 231)');
      expect(rootStyles['--purple-bg']).toBe('rgb(115, 69, 229)');
      expect(rootStyles['--green-bg']).toBe('rgb(60, 133, 39)');
      
      // Validate dimension variables
      expect(rootStyles['--padding']).toBe('5px 15px');
      expect(rootStyles['--bezel-size']).toBe('5px');
      expect(rootStyles['--leftmargin']).toBe('15px');
      expect(rootStyles['--rightmargin']).toBe('250px');
      expect(rootStyles['--transition-duration']).toBe('1s');
      
      // Validate font variable
      expect(rootStyles['--font']).toBe('"Futura Medium", white');
    });

    test('color variables have valid RGB values', async ({ page }) => {
      const colorVars = await page.evaluate(() => {
        const root = document.documentElement;
        const computedStyle = getComputedStyle(root);
        const colors = {};
        
        // Get all color-related variables
        for (let i = 0; i < computedStyle.length; i++) {
          const property = computedStyle[i];
          if (property.startsWith('--') && (property.includes('-bg') || property.includes('-bezel'))) {
            const value = computedStyle.getPropertyValue(property).trim();
            if (value.startsWith('rgb(')) {
              colors[property] = value;
            }
          }
        }
        
        return colors;
      });

      // Validate RGB format for all color variables
      Object.entries(colorVars).forEach(([prop, value]) => {
        expect(value).toMatch(/^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$/);
      });
    });
  });

  test.describe('Button Component Styling', () => {
    test('red button has correct styling properties', async ({ page }) => {
      const redButton = page.locator('#red-button');
      
      const styles = await redButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          backgroundColor: computed.backgroundColor,
          color: computed.color,
          borderWidth: computed.borderWidth,
          borderStyle: computed.borderStyle,
          borderRadius: computed.borderRadius,
          cursor: computed.cursor,
          textAlign: computed.textAlign,
          padding: computed.padding,
          position: computed.position
        };
      });

      expect(styles.backgroundColor).toBe('rgb(214, 71, 71)');
      expect(styles.color).toBe('rgb(255, 255, 255)');
      expect(styles.borderWidth).toBe('5px');
      expect(styles.borderStyle).toBe('solid');
      expect(styles.borderRadius).toBe('0px');
      expect(styles.cursor).toBe('pointer');
      expect(styles.textAlign).toBe('center');
      expect(styles.padding).toBe('5px 15px');
      expect(styles.position).toBe('relative');
    });

    test('all color variants have correct styling', async ({ page }) => {
      const colorTests = [
        { id: '#pink-button', expectedBg: 'rgb(255, 186, 231)', expectedColor: 'rgb(0, 0, 0)' },
        { id: '#purple-button', expectedBg: 'rgb(115, 69, 229)', expectedColor: 'rgb(255, 255, 255)' },
        { id: '#green-button', expectedBg: 'rgb(60, 133, 39)', expectedColor: 'rgb(255, 255, 255)' },
        { id: '#light-button', expectedBg: 'rgb(208, 209, 212)', expectedColor: 'rgb(0, 0, 0)' },
        { id: '#dark-button', expectedBg: 'rgb(72, 73, 74)', expectedColor: 'rgb(255, 255, 255)' }
      ];

      for (const colorTest of colorTests) {
        const button = page.locator(colorTest.id);
        const styles = await button.evaluate((el) => {
          const computed = getComputedStyle(el);
          return {
            backgroundColor: computed.backgroundColor,
            color: computed.color
          };
        });

        expect(styles.backgroundColor).toBe(colorTest.expectedBg);
        expect(styles.color).toBe(colorTest.expectedColor);
      }
    });

    test('disabled buttons have correct styling', async ({ page }) => {
      const disabledButton = page.locator('#disabled-button');
      const disabledLightButton = page.locator('#disabled-light-button');
      
      const disabledStyles = await disabledButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          backgroundColor: computed.backgroundColor,
          color: computed.color,
          cursor: computed.cursor
        };
      });

      const disabledLightStyles = await disabledLightButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          backgroundColor: computed.backgroundColor,
          color: computed.color,
          cursor: computed.cursor
        };
      });

      // Default disabled (dark)
      expect(disabledStyles.backgroundColor).toBe('rgb(53, 54, 55)');
      expect(disabledStyles.color).toBe('rgb(255, 255, 255)');
      expect(disabledStyles.cursor).toBe('not-allowed');

      // Light disabled
      expect(disabledLightStyles.backgroundColor).toBe('rgb(208, 209, 212)');
      expect(disabledLightStyles.color).toBe('rgb(0, 0, 0)');
      expect(disabledLightStyles.cursor).toBe('not-allowed');
    });

    test('button pseudo-elements are properly configured', async ({ page }) => {
      const redButton = page.locator('#red-button');
      
      const pseudoStyles = await redButton.evaluate((el) => {
        const beforeStyles = getComputedStyle(el, '::before');
        const afterStyles = getComputedStyle(el, '::after');
        return {
          beforePosition: beforeStyles.position,
          beforeContent: beforeStyles.content,
          beforePointerEvents: beforeStyles.pointerEvents,
          beforeHeight: beforeStyles.height,
          afterPosition: afterStyles.position,
          afterContent: afterStyles.content,
          afterPointerEvents: afterStyles.pointerEvents,
          afterBorderWidth: afterStyles.borderWidth
        };
      });

      expect(pseudoStyles.beforePosition).toBe('absolute');
      expect(pseudoStyles.beforeContent).toBe('""');
      expect(pseudoStyles.beforePointerEvents).toBe('none');
      expect(pseudoStyles.beforeHeight).toBe('5px');
      
      expect(pseudoStyles.afterPosition).toBe('absolute');
      expect(pseudoStyles.afterContent).toBe('""');
      expect(pseudoStyles.afterPointerEvents).toBe('none');
      expect(pseudoStyles.afterBorderWidth).toBe('2.5px');
    });
  });

  test.describe('Interactive States', () => {
    test('button hover state modifies pseudo-elements', async ({ page }) => {
      const redButton = page.locator('#red-button');
      
      // Get initial state
      const initialHeight = await redButton.evaluate((el) => {
        const beforeStyles = getComputedStyle(el, '::before');
        return beforeStyles.height;
      });

      // Hover over button
      await redButton.hover();
      await page.waitForTimeout(100);

      const hoveredHeight = await redButton.evaluate((el) => {
        const beforeStyles = getComputedStyle(el, '::before');
        return beforeStyles.height;
      });

      expect(initialHeight).toBe('5px');
      expect(hoveredHeight).toBe('0px');
    });

    test('button active state works correctly', async ({ page }) => {
      const staticActiveButton = page.locator('#static-active-button');
      
      const activeHeight = await staticActiveButton.evaluate((el) => {
        const beforeStyles = getComputedStyle(el, '::before');
        return beforeStyles.height;
      });

      // Active state should have height 0 for before pseudo-element
      expect(activeHeight).toBe('0px');
    });

    test('active color attributes override base colors', async ({ page }) => {
      // Test with dynamic active state
      await page.evaluate(() => {
        const button = document.getElementById('active-green-button');
        button.setAttribute('oreui-state', 'active');
      });

      const activeButton = page.locator('#active-green-button');
      
      const styles = await activeButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          backgroundColor: computed.backgroundColor,
          color: computed.color
        };
      });

      expect(styles.backgroundColor).toBe('rgb(60, 133, 39)'); // green
      expect(styles.color).toBe('rgb(255, 255, 255)'); // white
    });

    test('button transforms change on hover/active states', async ({ page }) => {
      const redButton = page.locator('#red-button');
      
      // Get normal state transform
      const normalTransform = await redButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return computed.transform;
      });

      // Hover over button
      await redButton.hover();
      
      const hoveredTransform = await redButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return computed.transform;
      });

      // Transform should be different on hover
      expect(normalTransform).not.toBe(hoveredTransform);
    });
  });

  test.describe('Input Component Styling', () => {
    test('input has correct default styling', async ({ page }) => {
      const testInput = page.locator('#test-input');
      
      const styles = await testInput.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          backgroundColor: computed.backgroundColor,
          color: computed.color,
          outline: computed.outline,
          boxShadow: computed.boxShadow,
          outlineOffset: computed.outlineOffset,
          padding: computed.padding
        };
      });

      expect(styles.backgroundColor).toBe('rgb(51, 51, 51)');
      expect(styles.color).toBe('rgb(255, 255, 255)');
      expect(styles.outline).toContain('rgb(0, 0, 0)'); // black outline
      expect(styles.boxShadow).toContain('rgb(35, 35, 35)'); // inset shadow
      expect(styles.outlineOffset).toBe('-2px');
      expect(styles.padding).toBe('10px');
    });

    test('input focus state changes outline', async ({ page }) => {
      const testInput = page.locator('#test-input');
      
      await testInput.focus();
      
      const focusedStyles = await testInput.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          outline: computed.outline,
          outlineOffset: computed.outlineOffset
        };
      });

      expect(focusedStyles.outline).toContain('rgb(255, 255, 255)'); // white outline when focused
      expect(focusedStyles.outlineOffset).toBe('-0.5px');
    });

    test('disabled input has correct styling', async ({ page }) => {
      const disabledInput = page.locator('#disabled-input');
      
      const styles = await disabledInput.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          color: computed.color
        };
      });

      expect(styles.color).toBe('rgb(128, 128, 128)'); // gray
    });
  });

  test.describe('General Components', () => {
    test('general component has correct styling', async ({ page }) => {
      const generalComponent = page.locator('#general-component');
      
      const styles = await generalComponent.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          borderWidth: computed.borderWidth,
          borderStyle: computed.borderStyle,
          borderRadius: computed.borderRadius,
          padding: computed.padding,
          textAlign: computed.textAlign,
          outline: computed.outline,
          outlineOffset: computed.outlineOffset
        };
      });

      expect(styles.borderWidth).toBe('5px');
      expect(styles.borderStyle).toBe('solid');
      expect(styles.borderRadius).toBe('0px');
      expect(styles.padding).toBe('5px 15px');
      expect(styles.textAlign).toBe('center');
      expect(styles.outline).toContain('rgb(0, 0, 0)'); // black outline
      expect(styles.outlineOffset).toBe('-2px');
    });

    test('search container has correct layout', async ({ page }) => {
      const searchContainer = page.locator('#search-container');
      
      const styles = await searchContainer.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          margin: computed.margin,
          textAlign: computed.textAlign,
          position: computed.position,
          height: computed.height,
          display: computed.display,
          flexDirection: computed.flexDirection
        };
      });

      expect(styles.margin).toBe('0px');
      expect(styles.textAlign).toBe('center');
      expect(styles.position).toBe('relative');
      expect(styles.height).toBe('37.5px');
      expect(styles.display).toBe('flex');
      expect(styles.flexDirection).toBe('row');
    });

    test('search results have correct positioning', async ({ page }) => {
      const searchResults = page.locator('#search-results');
      
      const styles = await searchResults.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          position: computed.position,
          top: computed.top,
          zIndex: computed.zIndex,
          display: computed.display
        };
      });

      expect(styles.position).toBe('absolute');
      expect(styles.top).toBe('42.5px');
      expect(styles.zIndex).toBe('100');
      expect(styles.display).toBe('none'); // hidden by default
    });
  });

  test.describe('Font Declarations', () => {
    test('font-face rules are properly declared', async ({ page }) => {
      const fontFaceRules = await page.evaluate(() => {
        const styleSheets = Array.from(document.styleSheets);
        const fontFaces = [];
        
        for (const sheet of styleSheets) {
          try {
            const rules = Array.from(sheet.cssRules || sheet.rules || []);
            for (const rule of rules) {
              if (rule.type === CSSRule.FONT_FACE_RULE) {
                fontFaces.push({
                  fontFamily: rule.style.fontFamily,
                  src: rule.style.src,
                  fontWeight: rule.style.fontWeight,
                  fontStyle: rule.style.fontStyle
                });
              }
            }
          } catch (e) {
            // Ignore cross-origin errors
          }
        }
        return fontFaces;
      });

      expect(fontFaceRules.length).toBeGreaterThanOrEqual(3);
      
      const fontFamilies = fontFaceRules.map(rule => rule.fontFamily.replace(/"/g, ''));
      expect(fontFamilies).toContain('Futura Heavy');
      expect(fontFamilies).toContain('Futura Medium');
      expect(fontFamilies).toContain('CaskaydiaMono');

      // Validate font properties
      fontFaceRules.forEach(rule => {
        expect(rule.fontWeight).toBe('normal');
        expect(rule.fontStyle).toBe('normal');
        expect(rule.src).toContain('format("truetype")');
      });
    });

    test('body uses correct font family', async ({ page }) => {
      const bodyFont = await page.evaluate(() => {
        const computed = getComputedStyle(document.body);
        return computed.fontFamily;
      });

      expect(bodyFont).toContain('Futura Medium');
    });
  });

  test.describe('Animations and Keyframes', () => {
    test('radar81 keyframe animation is defined', async ({ page }) => {
      const keyframeRules = await page.evaluate(() => {
        const styleSheets = Array.from(document.styleSheets);
        const keyframes = [];
        
        for (const sheet of styleSheets) {
          try {
            const rules = Array.from(sheet.cssRules || sheet.rules || []);
            for (const rule of rules) {
              if (rule.type === CSSRule.KEYFRAMES_RULE) {
                keyframes.push({
                  name: rule.name,
                  cssRules: Array.from(rule.cssRules).map(r => r.keyText)
                });
              }
            }
          } catch (e) {
            // Ignore cross-origin errors
          }
        }
        return keyframes;
      });

      const radar81 = keyframes.find(k => k.name === 'radar81');
      expect(radar81).toBeDefined();
      expect(radar81.cssRules).toContain('0%');
      expect(radar81.cssRules).toContain('100%');
    });

    test('pinger animation component has correct structure', async ({ page }) => {
      const pingerAnim = page.locator('#pinger');
      
      const styles = await pingerAnim.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          position: computed.position,
          width: computed.width,
          height: computed.height,
          borderRadius: computed.borderRadius,
          display: computed.display,
          alignItems: computed.alignItems,
          justifyContent: computed.justifyContent,
          overflow: computed.overflow
        };
      });

      expect(styles.position).toBe('relative');
      expect(styles.width).toBe('100px');
      expect(styles.height).toBe('100px');
      expect(styles.borderRadius).toBe('50%');
      expect(styles.display).toBe('flex');
      expect(styles.alignItems).toBe('center');
      expect(styles.justifyContent).toBe('center');
      expect(styles.overflow).toBe('hidden');
    });

    test('pinger animation span has correct animation properties', async ({ page }) => {
      const pingerSpan = page.locator('#pinger span');
      
      const styles = await pingerSpan.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          position: computed.position,
          animationName: computed.animationName,
          animationDuration: computed.animationDuration,
          animationIterationCount: computed.animationIterationCount,
          animationPlayState: computed.animationPlayState,
          borderTop: computed.borderTop
        };
      });

      expect(styles.position).toBe('absolute');
      expect(styles.animationName).toBe('radar81');
      expect(styles.animationDuration).toBe('2s');
      expect(styles.animationIterationCount).toBe('infinite');
      expect(styles.animationPlayState).toBe('paused');
      expect(styles.borderTop).toContain('2px dotted');
    });
  });

  test.describe('Responsive Design', () => {
    test('mobile media query styles apply correctly', async ({ page }) => {
      await page.setViewportSize({ width: 500, height: 600 });
      
      const mediaQueryMatch = await page.evaluate(() => {
        return window.matchMedia('(max-width: 767px)').matches;
      });
      
      expect(mediaQueryMatch).toBe(true);

      // Test navigation transforms for mobile
      const largeNav = page.locator('#large-nav');
      const smallNav = page.locator('#small-nav');
      
      const navStyles = await page.evaluate(() => {
        const largeNavEl = document.getElementById('large-nav');
        const smallNavEl = document.getElementById('small-nav');
        const largeNavStyles = getComputedStyle(largeNavEl);
        const smallNavStyles = getComputedStyle(smallNavEl);
        
        return {
          largeNavTransform: largeNavStyles.transform,
          largeNavDisplay: largeNavStyles.display,
          smallNavTransform: smallNavStyles.transform,
          smallNavDisplay: smallNavStyles.display
        };
      });

      expect(navStyles.largeNavDisplay).toBe('block');
      expect(navStyles.smallNavDisplay).toBe('block');
      expect(navStyles.largeNavTransform).toContain('translateY(-100%)');
      expect(navStyles.smallNavTransform).toContain('translateY(0%)');
    });

    test('desktop media query styles apply correctly', async ({ page }) => {
      await page.setViewportSize({ width: 1200, height: 800 });
      
      const mediaQueryMatch = await page.evaluate(() => {
        return window.matchMedia('(min-width: 768px)').matches;
      });
      
      expect(mediaQueryMatch).toBe(true);

      // Test body layout for desktop
      const bodyStyles = await page.evaluate(() => {
        const computed = getComputedStyle(document.body);
        return {
          display: computed.display,
          flexDirection: computed.flexDirection,
          justifyContent: computed.justifyContent
        };
      });

      expect(bodyStyles.display).toBe('flex');
      expect(bodyStyles.flexDirection).toBe('column');
      expect(bodyStyles.justifyContent).toBe('space-between');

      // Test navigation transforms for desktop
      const navStyles = await page.evaluate(() => {
        const largeNavEl = document.getElementById('large-nav');
        const smallNavEl = document.getElementById('small-nav');
        const largeNavStyles = getComputedStyle(largeNavEl);
        const smallNavStyles = getComputedStyle(smallNavEl);
        
        return {
          largeNavTransform: largeNavStyles.transform,
          smallNavTransform: smallNavStyles.transform
        };
      });

      expect(navStyles.largeNavTransform).toContain('translateY(0%)');
      expect(navStyles.smallNavTransform).toContain('translateY(-100%)');
    });
  });

  test.describe('Edge Cases and Error Handling', () => {
    test('invalid color attributes are handled gracefully', async ({ page }) => {
      await page.evaluate(() => {
        const button = document.createElement('button');
        button.setAttribute('oreui-type', 'button');
        button.setAttribute('oreui-color', 'invalid-color');
        button.id = 'invalid-color-button';
        button.textContent = 'Invalid Color';
        document.getElementById('test-container').appendChild(button);
      });

      const invalidButton = page.locator('#invalid-color-button');
      
      const styles = await invalidButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          borderWidth: computed.borderWidth,
          borderStyle: computed.borderStyle,
          cursor: computed.cursor,
          position: computed.position
        };
      });

      // Should still have basic button styling
      expect(styles.borderWidth).toBe('5px');
      expect(styles.borderStyle).toBe('solid');
      expect(styles.cursor).toBe('pointer');
      expect(styles.position).toBe('relative');
    });

    test('multiple conflicting attributes prioritize correctly', async ({ page }) => {
      await page.evaluate(() => {
        const button = document.createElement('button');
        button.setAttribute('oreui-type', 'button');
        button.setAttribute('oreui-color', 'red');
        button.setAttribute('oreui-active-color', 'green');
        button.setAttribute('oreui-state', 'active');
        button.disabled = true;
        button.id = 'conflict-button';
        button.textContent = 'Conflict Test';
        document.getElementById('test-container').appendChild(button);
      });

      const conflictButton = page.locator('#conflict-button');
      
      const styles = await conflictButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          backgroundColor: computed.backgroundColor,
          cursor: computed.cursor
        };
      });

      // Disabled should override other color states due to !important
      expect(styles.backgroundColor).toBe('rgb(53, 54, 55)'); // disabled dark bg
      expect(styles.cursor).toBe('not-allowed');
    });

    test('malformed CSS properties do not break layout', async ({ page }) => {
      // Test that the CSS is robust against potential parsing issues
      const cssValidation = await page.evaluate(() => {
        const errors = [];
        
        try {
          // Test creating elements with all possible oreui attributes
          const testTypes = ['button', 'input', 'general'];
          const testColors = ['red', 'pink', 'purple', 'green', 'light', 'dark'];
          
          testTypes.forEach(type => {
            testColors.forEach(color => {
              const element = document.createElement(type === 'input' ? 'input' : 'div');
              element.setAttribute('oreui-type', type);
              element.setAttribute('oreui-color', color);
              
              const computed = getComputedStyle(element);
              if (!computed.display) {
                errors.push(`Failed to compute styles for ${type} with ${color} color`);
              }
            });
          });
        } catch (e) {
          errors.push(e.message);
        }
        
        return errors;
      });

      expect(cssValidation).toHaveLength(0);
    });

    test('CSS specificity works as expected', async ({ page }) => {
      // Test CSS selector specificity by checking that more specific selectors override less specific ones
      await page.evaluate(() => {
        const button = document.createElement('button');
        button.setAttribute('oreui-type', 'button');
        button.setAttribute('oreui-color', 'red');
        button.setAttribute('oreui-active-color', 'green');
        button.disabled = true;
        button.setAttribute('oreui-disabled-color', 'light');
        button.id = 'specificity-button';
        button.textContent = 'Specificity Test';
        document.getElementById('test-container').appendChild(button);
      });

      const specificityButton = page.locator('#specificity-button');
      
      const styles = await specificityButton.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          backgroundColor: computed.backgroundColor,
          color: computed.color,
          cursor: computed.cursor
        };
      });

      // The most specific disabled color should win
      expect(styles.backgroundColor).toBe('rgb(208, 209, 212)'); // light disabled bg
      expect(styles.color).toBe('rgb(0, 0, 0)'); // black text for light disabled
      expect(styles.cursor).toBe('not-allowed');
    });
  });

  test.describe('Performance and Compatibility', () => {
    test('CSS does not cause layout thrashing', async ({ page }) => {
      // Test that hover and active states don't cause excessive reflows
      const redButton = page.locator('#red-button');
      
      const performanceStart = await page.evaluate(() => performance.now());
      
      // Perform multiple hover operations
      for (let i = 0; i < 10; i++) {
        await redButton.hover();
        await page.waitForTimeout(50);
        await page.mouse.move(0, 0);
        await page.waitForTimeout(50);
      }
      
      const performanceEnd = await page.evaluate(() => performance.now());
      const totalTime = performanceEnd - performanceStart;
      
      // Should complete quickly (less than 5 seconds for 10 hover cycles)
      expect(totalTime).toBeLessThan(5000);
    });

    test('all CSS selectors are syntactically valid', async ({ page }) => {
      const cssValidation = await page.evaluate(() => {
        const issues = [];
        
        try {
          // Check that the stylesheet loaded without errors
          const styleSheets = Array.from(document.styleSheets);
          
          for (const sheet of styleSheets) {
            try {
              const rules = Array.from(sheet.cssRules || sheet.rules || []);
              
              if (rules.length === 0) {
                issues.push('No CSS rules found - possible parsing error');
              }
              
              // Check for common CSS rule types
              const hasStyleRules = rules.some(rule => rule.type === CSSRule.STYLE_RULE);
              const hasFontFaceRules = rules.some(rule => rule.type === CSSRule.FONT_FACE_RULE);
              const hasKeyframesRules = rules.some(rule => rule.type === CSSRule.KEYFRAMES_RULE);
              const hasMediaRules = rules.some(rule => rule.type === CSSRule.MEDIA_RULE);
              
              if (!hasStyleRules) issues.push('No style rules found');
              if (!hasFontFaceRules) issues.push('No font-face rules found');
              if (!hasKeyframesRules) issues.push('No keyframes rules found');
              if (!hasMediaRules) issues.push('No media rules found');
              
            } catch (e) {
              issues.push(`Error reading stylesheet: ${e.message}`);
            }
          }
        } catch (e) {
          issues.push(`CSS validation error: ${e.message}`);
        }
        
        return issues;
      });

      expect(cssValidation).toHaveLength(0);
    });
  });
});