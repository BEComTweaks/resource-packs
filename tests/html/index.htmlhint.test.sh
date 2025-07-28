#!/bin/bash
# HTMLHint validation for index.html
if ! command -v htmlhint &> /dev/null; then
  echo "HTMLHint is not installed. Install with: npm install -g htmlhint"
  exit 1
fi
htmlhint --config .htmlhintrc tests/index.test.js