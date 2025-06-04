#!/bin/bash

# Install NPM dependencies
npm install

# Build the Tailwind CSS file
npm run build:css

echo "Tailwind CSS has been installed and built successfully!"
echo "To watch for changes during development, run: npm run watch:css"
