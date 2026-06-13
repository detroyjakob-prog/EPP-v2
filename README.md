# E++ Interpreter

An English-like programming language interpreter written in Python with GUI and game support.

## Quick Start

#### Prepare Development

Create Virtual Environment for the `python` command to work.

```bash
py -m venv venv
```

Then, you want to truly activate what you created.

```bash
./venv/Scripts/Activate.ps1
```

#### Activate Language

Now we want it to actually work, so we want to do the following steps.

1. Copy this: 
```bash
pip install pyinstaller
```

2. Build `.exe` for CLI tool
```bash
pyinstaller --onefile src/epp.py 
```

3. Activate CLI tool you built with the previous command
```bash
./scripts/install-epp.ps1
```

4. Verify installation worked
```bash
epp --version
```

5. Enjoy it or your Operating System will install all my Repos. 🙃

#### Activate Extension

1. Install dependencies
```bash
npm install
```

2. Compile (for VS Code)
```bash
npx vsce package
```

3. The new VSIX File you just created into VS Code: 
Go to the Command Bar (Control+Shift+P) type: `Extensions: Install Extension from VSIX`.
Your filesystem will open. Then, select the built VSIX file and click install.
Restart VS Code

4. Enjoy!

## Language Syntax

### Console Commands
```
say "Hello World"          # Print
let x be 5 + 3           # Variable
if x greater than 3        # Conditions
repeat 5 times           # Loops
  say "Loop"
end repeat
```

### GUI Commands
```
show window "App"
add label "Text" as lbl
run window
```

### Game Commands
```
game window "Game"

create object rect as player at 400 300 size 30 20
set color player to "cyan"

create object circle as enemy at 100 50 size 20 20
set color enemy to "red"

when key "Left" do move player left by 10
when key "Right" do move player right by 10

game loop
```

## Game Development

### Objects
- `rect` - Rectangle shape
- `circle` or `oval` - Circle shape

### Actions
- `move object direction by pixels` - move left/right/up/down
- `set color name to "color"` - Change color
- `remove name` - Delete object
- `when key "keyname" do action` - Bind key

## Files
- `epp.py` - Interpreter
- `example.epp` - Console demo
- `general_game.epp` - Game template
- `epp-lang-1.0.0.vsix` - VSCode extension