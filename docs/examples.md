---
layout: docs
title: Examples
description: Real-world examples of using pycefrl
toc: true
---

## Introduction

This page provides practical examples of using pycefrl to analyze different types of Python code and projects.

## Example 1: Analyzing a Simple Script

Let's analyze a simple Python script:

```python
# calculator.py
def add(a, b):
    """Add two numbers"""
    return a + b

def multiply(a, b):
    """Multiply two numbers"""
    result = a * b
    return result

def main():
    x = 10
    y = 5
    sum_result = add(x, y)
    mult_result = multiply(x, y)
    print(f"Sum: {sum_result}, Product: {mult_result}")

if __name__ == "__main__":
    main()
```

**Run the analysis:**
```bash
python3 pycerfl.py directory .
```

**Expected Results:**

| Element | Level | Explanation |
|---------|-------|-------------|
| Function `add` | B1 | Function with simple arguments |
| Function `multiply` | B1 | Function with simple arguments |
| Function `main` | B1 | Function definition |
| Assignment `result = a * b` | A1 | Simple assignment |
| Return statements | B1 | Return in functions |
| Print with f-string | A1 | Basic print statement |
| `if __name__ == "__main__"` | A2 | Main guard pattern |

## Example 2: Analyzing a Class-Based Application

```python
# student_manager.py
class Student:
    """Represents a student with grades"""
    
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.grades = []
    
    def add_grade(self, grade):
        """Add a grade to the student's record"""
        if 0 <= grade <= 100:
            self.grades.append(grade)
        else:
            raise ValueError("Grade must be between 0 and 100")
    
    def get_average(self):
        """Calculate average grade"""
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)
    
    def __repr__(self):
        return f"Student({self.name}, {self.student_id})"

class GradeBook:
    """Manages multiple students"""
    
    def __init__(self):
        self.students = {}
    
    def add_student(self, student):
        """Add a student to the gradebook"""
        self.students[student.student_id] = student
    
    def get_top_students(self, n=5):
        """Get top N students by average grade"""
        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.get_average(),
            reverse=True
        )
        return sorted_students[:n]
```

**Analysis Results Highlight:**

| Element | Level | Explanation |
|---------|-------|-------------|
| Class definitions | B1 | Basic class structure |
| `__init__` method | B1 | Constructor method |
| Exception raising | B2 | Error handling with raise |
| `__repr__` method | B2 | Special method implementation |
| Lambda function | B1 | Simple lambda |
| List comprehension concepts | C1 | Advanced iteration |

## Example 3: Analyzing a GitHub Repository

Analyze Django (a popular Python framework):

```bash
python3 pycerfl.py repo https://github.com/django/django
```

This will analyze all Python files in the Django repository and provide insights into:
- Overall complexity distribution
- Most common code patterns
- Advanced features used (metaclasses, decorators, etc.)
- File-by-file breakdown

**Typical Results for Django:**
- High percentage of B1-B2 (well-structured, professional code)
- Moderate C1-C2 (advanced Python features where appropriate)
- Good balance indicating maintainable complexity

## Example 4: Analyzing a GitHub User's Projects

Analyze all public repositories of a user:

```bash
python3 pycerfl.py user guido
```

**Use Cases:**
- Assess a developer's coding style and complexity preferences
- Identify skill level progression over time
- Compare multiple developers' coding patterns

## Example 5: Using List Comprehensions

```python
# list_operations.py

# A1: Simple list
numbers = [1, 2, 3, 4, 5]

# A2: For loop
squares = []
for n in numbers:
    squares.append(n ** 2)

# C1: List comprehension (more advanced)
squares_comp = [n ** 2 for n in numbers]

# C1: List comprehension with condition
even_squares = [n ** 2 for n in numbers if n % 2 == 0]

# C2: Nested list comprehension
matrix = [[i * j for j in range(3)] for i in range(3)]
```

**Analysis Comparison:**
- The for loop approach gets A2 (elementary)
- Simple list comprehension gets C1 (advanced)
- Comprehensions with conditions get C1
- Nested comprehensions get C2 (proficient)

This shows how pycefrl can identify when you're using more Pythonic patterns.

## Example 6: Decorator Usage

```python
# decorators.py
import functools
import time

# B2: Simple decorator
def timer(func):
    """Time the execution of a function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

# B2: Using decorator
@timer
def slow_function():
    time.sleep(1)
    return "Done"

# C1: Decorator with arguments
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")
```

**Key Findings:**
- Function decorators: B2
- Nested functions: B2
- `*args, **kwargs`: B2
- Decorators with arguments: C1

## Example 7: Real-Time Analysis with Streamlit

Launch the Streamlit interface for interactive analysis:

```bash
python3 -m streamlit run app.py
```

**Workflow:**
1. Select "GitHub Repository" mode
2. Enter: `https://github.com/requests/requests`
3. Click "Analyze Repository"
4. Watch real-time logs as analysis progresses
5. View interactive visualizations:
   - Bubble chart of categories vs levels
   - Heatmap of files vs complexity
   - Treemap for drilling into specific elements
6. Download results as JSON or CSV

## Example 8: Comparing Code Versions

Track complexity changes over time:

```bash
# Analyze version 1
git checkout v1.0
python3 pycerfl.py directory ./src
cp data.json data_v1.json

# Analyze version 2
git checkout v2.0
python3 pycerfl.py directory ./src
cp data.json data_v2.json

# Compare the two JSON files to see complexity evolution
```

**Insights You Can Gain:**
- Did complexity increase or decrease?
- Are you using more advanced patterns?
- Which files changed most significantly?

## Example 9: Custom Configuration

Customize level assignments in `configuration.cfg`:

```ini
[A1]
List = ast.List
Tuple = ast.Tuple
Assignment = ast.Assign

[A2]
For = ast.For
If = ast.If
Import = ast.Import

[B1]
Function = ast.FunctionDef
Class = ast.ClassDef

# ... etc
```

After editing, regenerate the dictionary:
```bash
python3 dict.py
python3 pycerfl.py directory ./myproject
```

## Example 10: Batch Analysis Script

Create a script to analyze multiple projects:

```bash
#!/bin/bash
# analyze_projects.sh

PROJECTS=(
    "https://github.com/user/project1"
    "https://github.com/user/project2"
    "https://github.com/user/project3"
)

for project in "${PROJECTS[@]}"; do
    echo "Analyzing $project..."
    python3 pycerfl.py repo "$project"
    
    # Rename output files to avoid overwriting
    project_name=$(basename "$project")
    mv data.json "results/${project_name}_data.json"
    mv data.csv "results/${project_name}_data.csv"
done

echo "All analyses complete!"
```

## Practical Tips

### 1. Focus on High-Complexity Areas

```bash
# After analysis, filter for C1/C2 elements
cat data.csv | grep -E "C1|C2" > complex_elements.csv
```

### 2. Identify Refactoring Opportunities

Look for files with high concentrations of complex elements - these might benefit from simplification.

### 3. Use as a Learning Tool

Compare your code to established projects to see what patterns are used at different skill levels.

### 4. Team Code Reviews

Use pycefrl in code reviews to objectively discuss code complexity and suggest improvements.

### 5. Track Learning Progress

Regularly analyze your own projects to see how your coding patterns evolve over time.

## Next Steps

- [User Guide](./guide) - Comprehensive documentation
- [API Reference](./api) - Detailed API documentation
- [Dashboard](./dashboard) - Visualize your results
- [Contributing](./contributing) - Help improve pycefrl

## Share Your Examples

Have an interesting use case? Share it with the community:
- Open a discussion on [GitHub](https://github.com/raux/pycefrl/discussions)
- Submit a pull request with your example
- Blog about your experience and let us know!
