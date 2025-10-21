#!/usr/bin/env node

/**
 * Mermaid to Excalidraw Converter
 *
 * Converts Mermaid diagram syntax to Excalidraw format using the official
 * @excalidraw/mermaid-to-excalidraw package.
 *
 * Usage:
 *   node mermaid-to-excalidraw.js <input.mmd> <output.excalidraw>
 *
 * Example:
 *   node mermaid-to-excalidraw.js flowchart.mmd flowchart.excalidraw
 */

const fs = require('fs');
const path = require('path');
const { parseMermaidToExcalidraw, convertToExcalidrawElements } =
  require('@excalidraw/mermaid-to-excalidraw');

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

/**
 * Print colored message to console
 */
function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * Print usage information
 */
function printUsage() {
  log('\nMermaid to Excalidraw Converter', 'cyan');
  log('================================\n', 'cyan');
  log('Usage:', 'yellow');
  log('  node mermaid-to-excalidraw.js <input.mmd> <output.excalidraw>\n');
  log('Arguments:', 'yellow');
  log('  input.mmd          - Input Mermaid diagram file');
  log('  output.excalidraw  - Output Excalidraw file\n');
  log('Example:', 'yellow');
  log('  node mermaid-to-excalidraw.js flowchart.mmd flowchart.excalidraw\n');
  log('Supported Diagram Types:', 'yellow');
  log('  - Flowcharts (fully supported with hand-drawn style)');
  log('  - Other types (rendered as images)\n');
}

/**
 * Convert Mermaid to Excalidraw
 */
async function convert(inputFile, outputFile) {
  try {
    // Read Mermaid file
    log(`Reading Mermaid file: ${inputFile}`, 'blue');

    if (!fs.existsSync(inputFile)) {
      throw new Error(`Input file not found: ${inputFile}`);
    }

    const mermaidSyntax = fs.readFileSync(inputFile, 'utf8');

    if (!mermaidSyntax.trim()) {
      throw new Error('Input file is empty');
    }

    log('Parsing Mermaid syntax...', 'blue');

    // Parse Mermaid to skeleton format
    const { elements: skeletonElements } = await parseMermaidToExcalidraw(
      mermaidSyntax,
      {
        fontSize: 16,
      }
    );

    log('Converting to Excalidraw elements...', 'blue');

    // Convert to Excalidraw elements
    const excalidrawElements = convertToExcalidrawElements(skeletonElements);

    // Create Excalidraw document
    const excalidrawData = {
      type: 'excalidraw',
      version: 2,
      source: 'https://excalidraw.com',
      elements: excalidrawElements,
      appState: {
        gridSize: 20,
        viewBackgroundColor: '#ffffff'
      },
      files: {}
    };

    // Write output file
    log(`Writing Excalidraw file: ${outputFile}`, 'blue');
    fs.writeFileSync(outputFile, JSON.stringify(excalidrawData, null, 2), 'utf8');

    // Success message
    log(`\n✓ Successfully converted!`, 'green');
    log(`  Input:  ${inputFile}`, 'green');
    log(`  Output: ${outputFile}`, 'green');
    log(`  Elements: ${excalidrawElements.length}`, 'green');
    log(`\nYou can now open ${outputFile} in Excalidraw.`, 'cyan');

  } catch (error) {
    log(`\n✗ Conversion failed:`, 'red');
    log(`  ${error.message}`, 'red');

    if (error.message.includes('parseMermaidToExcalidraw')) {
      log('\nTip: Check your Mermaid syntax at https://mermaid.live/', 'yellow');
    }

    process.exit(1);
  }
}

/**
 * Main entry point
 */
async function main() {
  const args = process.argv.slice(2);

  // Check arguments
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    printUsage();
    process.exit(0);
  }

  if (args.length < 2) {
    log('Error: Missing arguments', 'red');
    printUsage();
    process.exit(1);
  }

  const [inputFile, outputFile] = args;

  // Validate file extensions
  const inputExt = path.extname(inputFile);
  const outputExt = path.extname(outputFile);

  if (!['.mmd', '.mermaid', '.txt'].includes(inputExt)) {
    log(`Warning: Input file extension is ${inputExt}, expected .mmd or .mermaid`, 'yellow');
  }

  if (outputExt !== '.excalidraw') {
    log(`Warning: Output file extension is ${outputExt}, expected .excalidraw`, 'yellow');
  }

  // Run conversion
  await convert(inputFile, outputFile);
}

// Run main function
if (require.main === module) {
  main().catch(error => {
    log(`\nUnexpected error: ${error.message}`, 'red');
    console.error(error);
    process.exit(1);
  });
}

module.exports = { convert };
