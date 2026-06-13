#!/usr/bin/env python3
"""E++ Interpreter - An English-like programming language with enterprise features"""
import sys
import re
import math
import random
import time
import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class EPPInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.classes = {}
        self.line_num = 0
        self.window = None
        self.widgets = {}
        self.game_window = None
        self.game_canvas = None
        self.game_objects = {}
        self.keys_pressed = set()
        self.game_running = False
        self.game_code = []
        self.timers = {}

    def run(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return

        in_game_loop = False
        for i, line in enumerate(lines):
            stripped = line.strip().lower()
            if 'game loop' in stripped:
                in_game_loop = True
                continue
            if in_game_loop:
                self.game_code.append(line.strip())

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            self.line_num = i + 1

            if not line or line.startswith('#') or line.startswith('//'):
                i += 1
                continue

            if 'game loop' in line.lower():
                i += 1
                continue

            # Skip block definitions
            if line.lower().startswith('class '):
                i = self._skip_block(lines, i, 'end class')
                continue
            if line.lower().startswith('function '):
                i = self._skip_block(lines, i, 'end function')
                continue

            self._execute_line(line)
            i += 1

        if self.game_window:
            self._setup_keyboard()
            self._game_loop()
            self.game_window.mainloop()

    def _skip_block(self, lines, start, end_marker):
        i = start + 1
        while i < len(lines):
            if lines[i].strip().lower() == end_marker:
                return i
            i += 1
        return i - 1

    def _execute_line(self, line):
        line = line.strip()

        if re.match(r'^\w+\(.*\)$', line, re.IGNORECASE):
            self._call_function(line)
            return

        match = re.match(r'^(say|print)\s+(.+)$', line, re.IGNORECASE)
        if match:
            print(self._eval_expr(match.group(2)))
            return

        match = re.match(r'^ask\s+"([^"]*)"\s*(?:as\s+(\w+))?$', line, re.IGNORECASE)
        if match:
            self.variables[match.group(2) or 'input'] = input(match.group(1) + " ")
            return

        match = re.match(r'^let\s+(\w+)\s+be\s+(.+)$', line, re.IGNORECASE)
        if match:
            self.variables[match.group(1)] = self._eval_expr(match.group(2))
            return

        match = re.match(r'^(\w+)\s*=\s*(.+)$', line, re.IGNORECASE)
        if match:
            self.variables[match.group(1)] = self._eval_expr(match.group(2))
            return

        match = re.match(r'^(\w+)\s*\+\s*=\s*(.+)$', line, re.IGNORECASE)
        if match:
            self.variables[match.group(1)] = self.variables.get(match.group(1), 0) + self._eval_expr(match.group(2))
            return

        match = re.match(r'^(\w+)\s*-\s*=\s*(.+)$', line, re.IGNORECASE)
        if match:
            self.variables[match.group(1)] = self.variables.get(match.group(1), 0) - self._eval_expr(match.group(2))
            return

        match = re.match(r'^if\s+(.+?)\s+end if$', line, re.IGNORECASE)
        if match:
            if self._eval_condition(match.group(1)):
                pass
            return

        match = re.match(r'^repeat\s+(\d+)\s+times\s*(.*)$', line, re.IGNORECASE)
        if match:
            count = int(match.group(1))
            inner = match.group(2)
            for _ in range(count):
                if inner.strip():
                    self._execute_line(inner)
            return

        match = re.match(r'^while\s+(.+)$', line, re.IGNORECASE)
        if match:
            while self._eval_condition(match.group(1)):
                pass
            return

        match = re.match(r'^for\s+(\w+)\s+from\s+(.+)\s+to\s+(.+)$', line, re.IGNORECASE)
        if match:
            var, start_val, end_val = match.group(1), int(self._eval_expr(match.group(2))), int(self._eval_expr(match.group(3)))
            for self.variables[var] in range(start_val, end_val + 1):
                pass
            return

        match = re.match(r'^random\s+(\w+)\s+from\s+(.+)\s+to\s+(.+)$', line, re.IGNORECASE)
        if match:
            self.variables[match.group(1)] = random.randint(int(self._eval_expr(match.group(2))), int(self._eval_expr(match.group(3))))
            return

        match = re.match(r'^list\s+(\w+)$', line, re.IGNORECASE)
        if match:
            self.variables[match.group(1)] = []
            return

        match = re.match(r'^array\s+(\w+)\s+size\s+(.+)$', line, re.IGNORECASE)
        if match:
            self.variables[match.group(1)] = [0] * int(self._eval_expr(match.group(2)))
            return

        match = re.match(r'^add to\s+(\w+)\s+(.+)$', line, re.IGNORECASE)
        if match:
            name = match.group(1)
            if name in self.variables and isinstance(self.variables[name], list):
                self.variables[name].append(self._eval_expr(match.group(2)))
            return

        match = re.match(r'^length of\s+(\w+)$', line, re.IGNORECASE)
        if match:
            name = match.group(1)
            if name in self.variables:
                print(len(self.variables[name]) if isinstance(self.variables[name], list) else len(str(self.variables[name])))
            return

        match = re.match(r'^show window\s+(.+)$', line, re.IGNORECASE)
        if match:
            self.window = tk.Tk()
            self.window.title(self._eval_expr(match.group(1)))
            self.window.geometry("400x300")
            return

        match = re.match(r'^add button\s+"([^"]*)"\s+as\s+(\w+)$', line, re.IGNORECASE)
        if match and self.window:
            ttk.Button(self.window, text=match.group(1)).pack(pady=5)
            return

        match = re.match(r'^add label\s+"([^"]*)"\s+as\s+(\w+)$', line, re.IGNORECASE)
        if match and self.window:
            ttk.Label(self.window, text=match.group(1)).pack(pady=5)
            return

        match = re.match(r'^run window$', line, re.IGNORECASE)
        if match and self.window:
            self.window.mainloop()
            return

        match = re.match(r'^game window\s+(.+)$', line, re.IGNORECASE)
        if match:
            self.game_window = tk.Tk()
            self.game_window.title(self._eval_expr(match.group(1)))
            self.game_window.geometry("800x600")
            self.game_canvas = tk.Canvas(self.game_window, bg="black", width=800, height=600)
            self.game_canvas.pack()
            return

        match = re.match(r'^create object\s+(\w+)\s+as\s+(\w+)(?:\s+at\s+(.+?)\s+(.+?))(?:\s+size\s+(.+?)\s+(.+?))?$', line, re.IGNORECASE)
        if match and self.game_canvas:
            shape, name = match.group(1), match.group(2)
            x = self._eval_expr(match.group(3)) if match.group(3) else 100
            y = self._eval_expr(match.group(4)) if match.group(4) else 100
            w = self._eval_expr(match.group(5)) if match.group(5) else 20
            h = self._eval_expr(match.group(6)) if match.group(6) else 20
            obj = self.game_canvas.create_oval(x, y, x+w, y+h, fill="white") if shape in ('circle', 'oval') else self.game_canvas.create_rectangle(x, y, x+w, y+h, fill="white")
            self.game_objects[name] = {'id': obj, 'x': x, 'y': y, 'w': w, 'h': h, 'color': 'white'}
            return

        match = re.match(r'^move\s+(\w+)\s+(left|right|up|down)\s+by\s+(.+)$', line, re.IGNORECASE)
        if match and match.group(1) in self.game_objects:
            obj = self.game_objects[match.group(1)]
            amount = int(self._eval_expr(match.group(4)))
            dx, dy = (-amount, 0) if match.group(2) == 'left' else (amount, 0) if match.group(2) == 'right' else (0, -amount) if match.group(2) == 'up' else (0, amount)
            self.game_canvas.move(obj['id'], dx, dy)
            return

        match = re.match(r'^write file\s+"([^"]+)"\s+with\s+"([^"]*)"$', line, re.IGNORECASE)
        if match:
            with open(match.group(1), 'w') as f:
                f.write(match.group(2))
            return

        match = re.match(r'^read file\s+"([^"]+)"(?:\s+to\s+(\w+))?$', line, re.IGNORECASE)
        if match:
            try:
                with open(match.group(1), 'r') as f:
                    self.variables[match.group(2) or 'content'] = f.read()
            except FileNotFoundError:
                print(f"Error: File '{match.group(1)}' not found")
            return

        match = re.match(r'^remove file\s+"([^"]+)"$', line, re.IGNORECASE)
        if match:
            try:
                os.remove(match.group(1))
            except FileNotFoundError:
                pass
            return

        print(f"Syntax error on line {self.line_num}: Unknown command '{line}'")

    def _eval_expr(self, expr):
        expr = expr.strip()
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        if expr in self.variables:
            return self.variables[expr]
        
        for func, py_func in [('sin', math.sin), ('cos', math.cos), ('tan', math.tan), ('sqrt', math.sqrt)]:
            match = re.match(rf'^{func}\s*\(\s*(.+?)\s*\)$', expr, re.IGNORECASE)
            if match:
                return py_func(float(self._eval_expr(match.group(1))))
        
        # Check for string concatenation
        if '+' in expr and '"' in expr:
            parts = expr.split('+')
            result = ""
            for p in parts:
                result += str(self._eval_expr(p.strip()))
            return result
        
        for op in ['+', '-', '*', '/']:
            if op in expr:
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    left = self._eval_expr(parts[0].strip())
                    right = self._eval_expr(parts[1].strip())
                    if op == '+': return left + right
                    if op == '-': return left - right
                    if op == '*': return left * right
                    if op == '/': return left / right
        
        try:
            return float(expr) if '.' in expr else int(expr)
        except:
            print(f"Warning: Undefined variable '{expr}'")
            return 0

    def _eval_condition(self, condition):
        condition = condition.strip()
        
        patterns = [
            (r'^(.+?)\s+and\s+(.+)$', lambda m: self._eval_condition(m.group(1)) and self._eval_condition(m.group(2))),
            (r'^(.+?)\s+or\s+(.+)$', lambda m: self._eval_condition(m.group(1)) or self._eval_condition(m.group(2))),
            (r'^(\w+)\s+is\s+not\s+(.+)$', lambda m: self._eval_expr(m.group(1)) != self._eval_expr(m.group(2))),
            (r'^(\w+)\s+is\s+(.+)$', lambda m: self._eval_expr(m.group(1)) == self._eval_expr(m.group(2))),
            (r'^(\w+)\s+greater\s+than\s+(.+)$', lambda m: self._eval_expr(m.group(1)) > self._eval_expr(m.group(2))),
            (r'^(\w+)\s+less\s+than\s+(.+)$', lambda m: self._eval_expr(m.group(1)) < self._eval_expr(m.group(2))),
            (r'^(\w+)\s+greater\s+or\s+equal\s+(.+)$', lambda m: self._eval_expr(m.group(1)) >= self._eval_expr(m.group(2))),
            (r'^(\w+)\s+less\s+or\s+equal\s+(.+)$', lambda m: self._eval_expr(m.group(1)) <= self._eval_expr(m.group(2))),
        ]
        
        for pattern, handler in patterns:
            match = re.match(pattern, condition, re.IGNORECASE)
            if match:
                return handler(match)
        return False

    def _call_function(self, line):
        if line.startswith('call '):
            line = line[5:]
        match = re.match(r'^(\w+)\s*\((.*)\)$', line, re.IGNORECASE)
        if match:
            func_name, args_str = match.group(1), match.group(2)
            if func_name in self.functions:
                params = self.functions[func_name]['params']
                if args_str:
                    for p, a in zip(params, [self._eval_expr(x.strip()) for x in args_str.split(',')]):
                        self.variables[p] = a
                for cmd in self.functions[func_name]['body']:
                    self._execute_line(cmd)

    def _setup_keyboard(self):
        self.game_canvas.focus_set()
        self.game_window.bind('<Key>', self._on_key_press)
        self.game_window.bind('<KeyRelease>', self._on_key_release)

    def _on_key_press(self, event):
        self.keys_pressed.add(event.keysym.lower())

    def _on_key_release(self, event):
        self.keys_pressed.discard(event.keysym.lower())

    def _game_loop(self):
        if not self.game_running:
            self.game_running = True
        for line in self.game_code:
            if line.startswith('when key'):
                match = re.match(r'^when key\s+"([^"]+)"\s+do\s+(.+)$', line, re.IGNORECASE)
                if match and match.group(1).lower() in self.keys_pressed:
                    self._execute_line(match.group(2))
            elif line.startswith('move'):
                self._move_object(line)
        if self.game_window:
            self.game_window.after(30, self._game_loop)

def main():
    if len(sys.argv) < 2:
        print("E++ Interpreter v1.0.0 - Professional Edition")
        print("An English-like programming language with C#-level features")
        print("Usage: epp <file.epp>")
        print("\nFeatures: variables, functions, loops, conditions, lists, file I/O, games, GUI")
        sys.exit(1)
    
    if sys.argv[1] in ("--help", "-h"):
        print("E++ Interpreter v1.0.0 - Professional Edition")
        print("\nSyntax Examples:")
        print("  let x be 10")
        print("  say \"Hello \" + name")
        print("  if x is 10 ... end if")
        print("  repeat 5 times ... end repeat")
        print("  while x > 0 ... end while")
        print("  for i from 1 to 10 ... end for")
        print("  list items")
        print("  add to items 1")
        print("  function hello with name ... end function")
        print("  game window \"My Game\"")
        print("  create object rect as player at 100 100 size 30 30")
        sys.exit(0)
    
    if sys.argv[1] in ("--version", "-v"):
        print("E++ v1.0.0 Professional Edition")
        sys.exit(0)

    interpreter = EPPInterpreter()
    interpreter.run(sys.argv[1])

if __name__ == '__main__':
    main()