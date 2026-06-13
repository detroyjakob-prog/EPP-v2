# E++ VSCode Extension

## Features

- **Syntax Highlighting** - Full support for E++ language syntax
- **Snippets** - Quick templates for common patterns:
  - `say` - Print statement
  - `let` - Variable declaration  
  - `if` - If condition block
  - `repeat` - Loop block
  - `ask` - User input
- **Intellisense** - Auto-completion for keywords and operators
- **Icon** - Custom E++ language icon

## Installation

1. Copy the `vscode-extension` folder to your VSCode extensions directory
2. Run `npm install` in the extension folder
3. Press F5 to launch the extension in a new window

Or package it:
```bash
npm install -g vsce
vsce package
```