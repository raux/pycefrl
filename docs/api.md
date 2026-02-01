---
layout: docs
title: API Reference
description: Complete API reference for pycefrl
toc: true
---

## Command Line Interface

### pycerfl.py

Main entry point for the pycefrl analyzer.

#### Syntax

```bash
python3 pycerfl.py <mode> <target>
```

#### Modes

##### directory

Analyze Python files in a local directory.

```bash
python3 pycerfl.py directory <path>
```

**Arguments:**
- `path`: Path to the directory containing Python files (absolute or relative)

**Examples:**
```bash
python3 pycerfl.py directory .
python3 pycerfl.py directory /home/user/projects/myapp
python3 pycerfl.py directory ../another-project
```

##### repo

Analyze a GitHub repository.

```bash
python3 pycerfl.py repo <github_url>
```

**Arguments:**
- `github_url`: Full clone URL of the GitHub repository

**Examples:**
```bash
python3 pycerfl.py repo https://github.com/django/django
python3 pycerfl.py repo https://github.com/requests/requests
```

**Note:** The repository will be cloned to a temporary location for analysis.

##### user

Analyze all public repositories of a GitHub user.

```bash
python3 pycerfl.py user <username>
```

**Arguments:**
- `username`: GitHub username

**Examples:**
```bash
python3 pycerfl.py user guido
python3 pycerfl.py user kennethreitz
```

**Note:** This will analyze all publicly accessible repositories for the user.

#### Output Files

The analyzer generates the following files:

| File | Description |
|------|-------------|
| `data.json` | Complete analysis data in JSON format |
| `data.csv` | Complete analysis data in CSV format |
| `DATA_JSON/summary_data.json` | Aggregated level statistics |
| `DATA_JSON/total_data.json` | File-level breakdown |
| `DATA_JSON/<repo_name>.json` | Individual repository summaries |
| `DATA_CSV/<file_name>.csv` | Individual file analyses |

## Core Modules

### levels.py

Contains the level assignment logic and CEFR classification system.

#### Key Constants

```python
# CEFR Levels
LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

# Code element categories
Literals = ['ast.List', 'ast.Tuple', 'ast.Dict']
Variables = ['ast.Name']
Expressions = ['ast.Call', 'ast.IfExp', 'ast.Attribute']
Comprehensions = ['ast.ListComp', 'ast.GeneratorExp', 'ast.DictComp']
Statements = ['ast.Assign', 'ast.AugAssign', 'ast.Raise', 'ast.Assert', 'ast.Pass']
Imports = ['ast.Import', 'ast.ImportFrom']
ControlFlow = ['ast.If', 'ast.For', 'ast.While', 'ast.Break', 'ast.Continue', 'ast.Try', 'ast.With']
FunctionsClass = ['ast.FunctionDef', 'ast.Lambda', 'ast.Return', 'ast.Yield', 'ast.ClassDef']
```

#### Functions

##### `asignar_Nivel(node, dicc)`

Assigns a CEFR level to an AST node based on the level dictionary.

**Parameters:**
- `node`: AST node object
- `dicc`: Dictionary mapping code patterns to CEFR levels

**Returns:**
- `str`: CEFR level (e.g., 'A1', 'B1', 'C2')

**Example:**
```python
import ast
from levels import asignar_Nivel

code = "x = [1, 2, 3]"
tree = ast.parse(code)
level = asignar_Nivel(tree.body[0], level_dict)
# Returns: 'A1' for simple list
```

### ClassIterTree.py

Provides tree iteration utilities for traversing Abstract Syntax Trees (AST).

#### Class: IterTree

Iterator for traversing Python AST nodes.

##### Methods

###### `__init__(self, tree, dicc)`

Initialize the tree iterator.

**Parameters:**
- `tree`: AST tree object from `ast.parse()`
- `dicc`: Level dictionary for node classification

###### `__iter__(self)`

Returns iterator object.

**Returns:**
- `self`: Iterator instance

###### `__next__(self)`

Advances to the next node in the tree.

**Returns:**
- `dict`: Node information containing:
  - `class`: Element type
  - `level`: CEFR level
  - `lineno`: Start line number
  - `end_lineno`: End line number
  - `col_offset`: Column offset (displacement)

**Raises:**
- `StopIteration`: When no more nodes to iterate

**Example:**
```python
import ast
from ClassIterTree import IterTree

code = """
def greet(name):
    print(f"Hello, {name}")
"""

tree = ast.parse(code)
iterator = IterTree(tree, level_dict)

for node_info in iterator:
    print(f"Found {node_info['class']} at line {node_info['lineno']}, level {node_info['level']}")
```

### getjson.py

Handles JSON output generation and data formatting.

#### Functions

##### `read_Json(option, filename_Dir, list_Results)`

Generates JSON output files from analysis results.

**Parameters:**
- `option`: Source identifier (repository/directory name)
- `filename_Dir`: File name being analyzed
- `list_Results`: List of analysis results for the file

**Outputs:**
- Creates/updates `data.json` with all results
- Creates/updates `DATA_JSON/summary_data.json` with aggregated statistics
- Creates/updates `DATA_JSON/total_data.json` with file-level data
- Creates individual repository JSON files in `DATA_JSON/`

**Data Structure:**
```json
{
  "Repository": "project-name",
  "File Name": "main.py",
  "Class": "Simple Function",
  "Start Line": 5,
  "End Line": 10,
  "Displacement": 4,
  "Level": "B1"
}
```

### getcsv.py

Handles CSV output generation.

#### Functions

##### `read_FileCsv(option, filename_Dir, list_Results)`

Generates CSV output files from analysis results.

**Parameters:**
- `option`: Source identifier (repository/directory name)
- `filename_Dir`: File name being analyzed  
- `list_Results`: List of analysis results for the file

**Outputs:**
- Creates/updates `data.csv` with all results
- Creates individual file CSV files in `DATA_CSV/`

**CSV Format:**
```csv
Repository,File Name,Class,Start Line,End Line,Displacement,Level
project-name,main.py,Simple Function,5,10,4,B1
```

### dict.py

Dictionary generation utility.

#### Usage

```bash
python3 dict.py
```

**Purpose:**
- Reads `configuration.cfg` to get level assignments
- Generates `dicc.txt` mapping code patterns to CEFR levels
- Must be run before first analysis and after configuration changes

**Output:**
- `dicc.txt`: Text file with level mappings

## Data Structures

### Analysis Result Dictionary

Each analyzed code element produces a dictionary with these fields:

```python
{
    'class': str,           # Type of code element
    'level': str,           # CEFR level (A1-C2)
    'lineno': int,          # Starting line number
    'end_lineno': int,      # Ending line number
    'col_offset': int       # Column offset (indentation)
}
```

### Summary Data Format

`summary_data.json` contains aggregated statistics:

```json
{
  "Levels": {
    "A1": 450,
    "A2": 380,
    "B1": 120,
    "B2": 45,
    "C1": 28,
    "C2": 12
  },
  "Class": {
    "Simple List": 81,
    "Simple Function": 42,
    "Simple Class": 15
  }
}
```

### Total Data Format

`total_data.json` provides file-level breakdowns:

```json
{
  "repository-name": {
    "file1.py": {
      "Levels": {
        "A1": 25,
        "A2": 15,
        "B1": 8
      }
    },
    "file2.py": {
      "Levels": {
        "A1": 30,
        "B1": 12
      }
    }
  }
}
```

## Configuration

### configuration.cfg

INI-style configuration file for customizing level assignments.

#### Format

```ini
[LEVEL_NAME]
Element_Name = ast.NodeType
```

#### Example

```ini
[A1]
Simple List = ast.List
Simple Tuple = ast.Tuple
Simple Assignment = ast.Assign

[A2]
Simple For Loop = ast.For
Simple If statements = ast.If
Import = ast.Import

[B1]
Function = ast.FunctionDef
Simple Class = ast.ClassDef

[B2]
Function with decorators = ast.FunctionDef
Class inheritance = ast.ClassDef

[C1]
List comprehension = ast.ListComp
Generator = ast.GeneratorExp

[C2]
Nested comprehension = ast.ListComp
Metaclass = ast.ClassDef
```

#### Sections

- `[A1]`: Basic level - fundamental Python structures
- `[A2]`: Elementary level - basic control flow and I/O
- `[B1]`: Intermediate level - functions, classes, exceptions
- `[B2]`: Upper intermediate - advanced OOP, decorators
- `[C1]`: Advanced - comprehensions, generators, advanced patterns
- `[C2]`: Proficient - complex nested structures, metaclasses

## AST Node Types

pycefrl recognizes the following Python AST node types:

### Literals
- `ast.List` - List literals
- `ast.Tuple` - Tuple literals
- `ast.Dict` - Dictionary literals
- `ast.Set` - Set literals

### Variables & Attributes
- `ast.Name` - Variable names
- `ast.Attribute` - Attribute access (e.g., `obj.attr`)

### Expressions
- `ast.Call` - Function/method calls
- `ast.IfExp` - Ternary expressions
- `ast.BinOp` - Binary operations
- `ast.UnaryOp` - Unary operations
- `ast.Compare` - Comparisons

### Statements
- `ast.Assign` - Assignments
- `ast.AugAssign` - Augmented assignments (+=, -=, etc.)
- `ast.Raise` - Raise exceptions
- `ast.Assert` - Assertions
- `ast.Pass` - Pass statements

### Imports
- `ast.Import` - Import statements
- `ast.ImportFrom` - From...import statements

### Control Flow
- `ast.If` - If statements
- `ast.For` - For loops
- `ast.While` - While loops
- `ast.Break` - Break statements
- `ast.Continue` - Continue statements
- `ast.Try` - Try/except blocks
- `ast.With` - Context managers

### Functions & Classes
- `ast.FunctionDef` - Function definitions
- `ast.Lambda` - Lambda expressions
- `ast.Return` - Return statements
- `ast.Yield` - Yield expressions
- `ast.ClassDef` - Class definitions

### Comprehensions
- `ast.ListComp` - List comprehensions
- `ast.DictComp` - Dictionary comprehensions
- `ast.SetComp` - Set comprehensions
- `ast.GeneratorExp` - Generator expressions

## Integration Examples

### Using as a Python Module

```python
import ast
from ClassIterTree import IterTree
from levels import asignar_Nivel
import json

# Load level dictionary
with open('dicc.txt', 'r') as f:
    level_dict = json.load(f)

# Parse Python code
code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""

tree = ast.parse(code)

# Analyze
results = []
iterator = IterTree(tree, level_dict)
for node_info in iterator:
    results.append(node_info)

# Display results
for result in results:
    print(f"{result['class']:30} | Level {result['level']} | Lines {result['lineno']}-{result['end_lineno']}")
```

### Custom Analysis Script

```python
import os
import ast
from ClassIterTree import IterTree

def analyze_directory(path, level_dict):
    """Analyze all Python files in a directory"""
    results = {}
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    try:
                        tree = ast.parse(f.read())
                        iterator = IterTree(tree, level_dict)
                        results[file] = list(iterator)
                    except SyntaxError:
                        print(f"Syntax error in {filepath}")
    
    return results
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError: dicc.txt` | Level dictionary not generated | Run `python3 dict.py` |
| `SyntaxError` | Invalid Python syntax in target file | Fix syntax errors in target code |
| `ModuleNotFoundError` | Missing dependencies | Run `pip3 install -r requirements.txt` |
| `KeyError` in level assignment | Node type not in configuration | Add missing node type to `configuration.cfg` |

## Performance Considerations

- **Large repositories**: Analysis time is proportional to code size
- **GitHub API**: Rate limiting applies to user/repository queries
- **Memory usage**: Large projects may require significant memory for AST parsing
- **File I/O**: Multiple output files are generated; ensure sufficient disk space

## Next Steps

- [Quick Start Guide](./quickstart) - Get started quickly
- [User Guide](./guide) - Comprehensive usage guide
- [Examples](./examples) - Practical examples
- [Contributing](./contributing) - Contribute to pycefrl
