// Fallback CSS validation tests using Node.js (no browser required)
const fs = require('fs');
const path = require('path');

class CSSValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
  }

  validateCSS(cssContent) {
    this.validateCSSVariables(cssContent);
    this.validateSelectors(cssContent);
    this.validateColorValues(cssContent);
    this.validateAnimations(cssContent);
    this.validateMediaQueries(cssContent);
    
    return {
      errors: this.errors,
      warnings: this.warnings,
      isValid: this.errors.length === 0
    };
  }

  validateCSSVariables(css) {
    const variablePattern = /--[\w-]+:\s*([^;]+);/g;
    const variables = [];
    let match;

    while ((match = variablePattern.exec(css)) !== null) {
      variables.push({
        name: match[0].split(':')[0].trim(),
        value: match[1].trim()
      });
    }

    // Check for required variables
    const requiredVars = [
      '--light-bg', '--dark-bg', '--red-bg', '--pink-bg', '--purple-bg', '--green-bg',
      '--padding', '--bezel-size', '--font', '--transition-duration'
    ];

    requiredVars.forEach(varName => {
      if (!variables.some(v => v.name === varName)) {
        this.errors.push(`Missing required CSS variable: ${varName}`);
      }
    });

    // Validate RGB color format
    const colorVars = variables.filter(v => v.name.includes('-bg') || v.name.includes('-bezel'));
    colorVars.forEach(colorVar => {
      if (colorVar.value.startsWith('rgb(') && !colorVar.value.match(/^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$/)) {
        this.errors.push(`Invalid RGB format for ${colorVar.name}: ${colorVar.value}`);
      }
    });

    console.log(`✓ Found ${variables.length} CSS variables`);
  }

  validateSelectors(css) {
    const selectorPatterns = [
      /\[oreui-type="button"\]/g,
      /\[oreui-type="input"\]/g,
      /\[oreui-type="general"\]/g,
      /\[oreui-color="red"\]/g,
      /\[oreui-color="pink"\]/g,
      /\[oreui-color="purple"\]/g,
      /\[oreui-color="green"\]/g,
      /\[oreui-color="light"\]/g,
      /\[oreui-color="dark"\]/g
    ];

    selectorPatterns.forEach((pattern, index) => {
      const matches = css.match(pattern);
      if (!matches) {
        this.errors.push(`Missing selector pattern: ${pattern.source}`);
      } else {
        console.log(`✓ Found ${matches.length} instances of selector ${pattern.source}`);
      }
    });
  }

  validateColorValues(css) {
    const rgbPattern = /rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)/g;
    let match;
    let colorCount = 0;

    while ((match = rgbPattern.exec(css)) !== null) {
      const [r, g, b] = [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
      
      if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
        this.errors.push(`Invalid RGB values: rgb(${r}, ${g}, ${b})`);
      }
      colorCount++;
    }

    console.log(`✓ Validated ${colorCount} RGB color values`);
  }

  validateAnimations(css) {
    if (!css.includes('@keyframes radar81')) {
      this.errors.push('Missing @keyframes radar81 animation');
    } else {
      console.log('✓ Found @keyframes radar81 animation');
    }

    if (!css.includes('animation: radar81')) {
      this.warnings.push('radar81 animation may not be used');
    }
  }

  validateMediaQueries(css) {
    const mediaQueries = [
      '@media (max-width: 767px)',
      '@media (min-width: 768px)'
    ];

    mediaQueries.forEach(query => {
      if (!css.includes(query)) {
        this.errors.push(`Missing media query: ${query}`);
      } else {
        console.log(`✓ Found media query: ${query}`);
      }
    });
  }
}

// Read and validate the CSS file
function runValidation() {
  console.log('🎨 Running CSS Theme Validation Tests...\n');

  try {
    // Try to read the actual theme file
    let cssContent = '';
    const possiblePaths = [
      path.join(__dirname, '..', 'theme.css'),
      path.join(__dirname, '..', 'css', 'theme.css'),
      path.join(__dirname, '..', 'src', 'theme.css')
    ];

    for (const filePath of possiblePaths) {
      if (fs.existsSync(filePath)) {
        cssContent = fs.readFileSync(filePath, 'utf8');
        console.log(`📁 Reading CSS from: ${filePath}\n`);
        break;
      }
    }

    if (!cssContent) {
      console.log('⚠️  Could not find theme.css file, using test content\n');
      // Use the content from the test file as reference
      cssContent = fs.readFileSync(__filename, 'utf8').match(/const cssContent = `([\s\S]*?)`;/)[1];
    }

    const validator = new CSSValidator();
    const result = validator.validateCSS(cssContent);

    console.log('\n📊 Validation Results:');
    console.log(`  Errors: ${result.errors.length}`);
    console.log(`  Warnings: ${result.warnings.length}`);

    if (result.errors.length > 0) {
      console.log('\n❌ Errors:');
      result.errors.forEach(error => console.log(`  - ${error}`));
    }

    if (result.warnings.length > 0) {
      console.log('\n⚠️  Warnings:');
      result.warnings.forEach(warning => console.log(`  - ${warning}`));
    }

    if (result.isValid) {
      console.log('\n✅ CSS validation passed!');
      process.exit(0);
    } else {
      console.log('\n❌ CSS validation failed!');
      process.exit(1);
    }

  } catch (error) {
    console.error('❌ Validation error:', error.message);
    process.exit(1);
  }
}

// Run validation if this file is executed directly
if (require.main === module) {
  runValidation();
}

module.exports = { CSSValidator };