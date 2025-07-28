# OreUI Theme CSS Tests

This directory contains comprehensive tests for the OreUI theme CSS file.

## Testing Framework

**Primary: Playwright** - Used for comprehensive UI testing including:
- CSS property validation
- Interactive state testing  
- Responsive design verification
- Animation and transition testing
- Cross-browser compatibility

**Fallback: Node.js CSS Validator** - Used when Playwright is not available:
- CSS syntax validation
- Selector pattern verification  
- Color value validation
- Media query validation

## Running Tests

```bash
# Run all tests (tries Playwright first, falls back to Node.js validator)
npm test

# Run only CSS validation (Node.js)
npm run test:css

# Run only Playwright tests
npm run test:playwright
```

## Test Coverage

### CSS Variables
- ✅ All CSS custom properties are defined
- ✅ RGB color values are valid
- ✅ Dimension values are correct

### Component Styling  
- ✅ Button components (all color variants)
- ✅ Input components (normal and disabled states)
- ✅ General components
- ✅ Search components

### Interactive States
- ✅ Hover effects on buttons
- ✅ Active states and transforms
- ✅ Focus states on inputs
- ✅ Disabled state styling

### Responsive Design
- ✅ Mobile viewport styles (max-width: 767px)
- ✅ Desktop viewport styles (min-width: 768px)
- ✅ Navigation transforms

### Animations
- ✅ Keyframe definitions (@keyframes radar81)
- ✅ Animation properties and timing
- ✅ Pinger animation component

### Edge Cases
- ✅ Invalid attribute handling  
- ✅ CSS specificity conflicts
- ✅ Multiple attribute combinations
- ✅ Performance implications

## Files

- `theme.css.test.js` - Main Playwright test suite
- `theme.validation.js` - Node.js CSS validator fallback
- `README.md` - This documentation