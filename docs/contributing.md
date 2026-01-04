---
layout: docs
title: Contributing to pycefrl
description: Guidelines for contributing to the pycefrl project
toc: true
---

## Welcome Contributors!

Thank you for your interest in contributing to pycefrl! This project welcomes contributions from developers of all skill levels. Whether you're fixing a bug, adding a feature, improving documentation, or suggesting enhancements, your help is appreciated.

## Ways to Contribute

### 1. Report Bugs

Found a bug? Please open an issue on GitHub with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Sample code if applicable

### 2. Suggest Features

Have an idea for a new feature? Open an issue with:
- Description of the proposed feature
- Use cases and benefits
- Potential implementation approach
- Examples of similar features in other tools

### 3. Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples and use cases
- Improve API documentation
- Translate documentation
- Create tutorials or guides

### 4. Fix Bugs

Browse the [issue tracker](https://github.com/raux/pycefrl/issues) for bugs to fix:
- Look for issues tagged `bug` or `good first issue`
- Comment on the issue to let others know you're working on it
- Submit a PR with your fix

### 5. Add Features

Implement new features:
- Check existing issues for feature requests
- Discuss major changes in an issue first
- Ensure backward compatibility
- Add tests for new functionality

### 6. Write Tests

Improve test coverage:
- Add tests for uncovered code
- Create tests for edge cases
- Write integration tests
- Improve existing test quality

## Getting Started

### 1. Fork and Clone

Fork the repository and clone your fork:

```bash
git clone https://github.com/YOUR-USERNAME/pycefrl.git
cd pycefrl
```

### 2. Set Up Development Environment

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the level dictionary:

```bash
python3 dict.py
```

### 3. Create a Branch

Create a feature branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or improvements

### 4. Make Changes

Make your changes following the code style guidelines below.

### 5. Test Your Changes

Run the existing tests:

```bash
python3 -m unittest discover tests
```

Test your changes manually:

```bash
# Test on sample code
python3 pycerfl.py directory ./tests

# Test specific scenarios
python3 pycerfl.py repo https://github.com/small/test-repo
```

### 6. Commit Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of what was added"
```

Commit message guidelines:
- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Add detailed description after blank line if needed
- Reference issues: "Fixes #123" or "Related to #456"

### 7. Push and Create PR

Push to your fork and create a Pull Request:

```bash
git push origin feature/your-feature-name
```

In your PR description:
- Explain what the changes do
- Reference related issues
- Include screenshots for UI changes
- Describe testing performed
- Note any breaking changes

## Code Style Guidelines

### Python Code Style

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def analyze_file(file_path, level_dict):
    """Analyze a Python file and return its complexity metrics.
    
    Args:
        file_path (str): Path to the Python file
        level_dict (dict): Dictionary mapping patterns to levels
        
    Returns:
        list: List of analysis results
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse and analyze
    tree = ast.parse(content)
    results = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            level = assign_level(node, level_dict)
            results.append({'type': 'function', 'level': level})
    
    return results
```

### Code Quality

- **Docstrings**: Add docstrings to all functions, classes, and modules
- **Type Hints**: Use type hints where beneficial
- **Comments**: Explain "why" not "what" (code should be self-explanatory)
- **Naming**: Use descriptive variable and function names
- **DRY**: Don't repeat yourself - extract common code
- **KISS**: Keep it simple and straightforward

### Testing

Write tests for new features:

```python
# tests/test_feature.py
import unittest
from levels import asignar_Nivel

class TestFeature(unittest.TestCase):
    def test_simple_list_detection(self):
        """Test that simple lists are detected as A1"""
        code = "x = [1, 2, 3]"
        tree = ast.parse(code)
        node = tree.body[0]
        level = asignar_Nivel(node, self.level_dict)
        self.assertEqual(level, 'A1')
    
    def test_nested_comprehension(self):
        """Test that nested comprehensions are detected as C2"""
        code = "matrix = [[i*j for j in range(3)] for i in range(3)]"
        tree = ast.parse(code)
        # Test implementation
        pass

if __name__ == '__main__':
    unittest.main()
```

### Documentation Style

For Markdown documentation:
- Use clear headings hierarchy (h2 for sections, h3 for subsections)
- Include code examples with syntax highlighting
- Add tables for structured data
- Use lists for step-by-step instructions
- Include screenshots for UI features

## Project Structure

Understanding the codebase:

```
pycefrl/
├── pycerfl.py          # Main entry point
├── levels.py           # Level assignment logic
├── ClassIterTree.py    # AST iteration
├── getjson.py          # JSON output generation
├── getcsv.py           # CSV output generation
├── dict.py             # Dictionary generation
├── configuration.cfg   # Level configuration
├── app.py              # Streamlit interface
├── tests/              # Unit tests
│   └── test_levels.py
├── docs/               # GitHub Pages documentation
│   ├── index.md
│   ├── installation.md
│   ├── quickstart.md
│   ├── guide.md
│   ├── api.md
│   ├── examples.md
│   ├── contributing.md
│   ├── dashboard.md
│   ├── _layouts/
│   ├── _includes/
│   └── assets/
├── DATA_JSON/          # JSON output directory
├── DATA_CSV/           # CSV output directory
└── WEB/                # Legacy web interface
```

## Testing Guidelines

### Running Tests

```bash
# Run all tests
python3 -m unittest discover tests

# Run specific test file
python3 -m unittest tests.test_levels

# Run specific test
python3 -m unittest tests.test_levels.TestLevels.test_simple_list
```

### Test Coverage

Tests should cover:
- **Core functionality**: Level detection for all AST node types
- **Edge cases**: Empty files, syntax errors, unusual patterns
- **Integration**: End-to-end analysis workflows
- **Output**: JSON and CSV generation
- **Configuration**: Custom configuration loading

### Writing Good Tests

```python
class TestLevelDetection(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Load level dictionary
        with open('dicc.txt') as f:
            self.level_dict = json.load(f)
    
    def test_function_with_args(self):
        """Test function with arguments is detected as B1"""
        code = """
def greet(name):
    return f"Hello, {name}"
"""
        tree = ast.parse(code)
        # Test assertions
        self.assertIsNotNone(tree)
    
    def tearDown(self):
        """Clean up after tests"""
        pass
```

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] No unnecessary files included
- [ ] Code is commented where necessary

### PR Checklist

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Test improvement

## Testing
How was this tested?

## Related Issues
Fixes #123

## Screenshots (if applicable)
Add screenshots for UI changes
```

### Code Review Process

1. Automated checks run (if configured)
2. Maintainer reviews code
3. Feedback provided if changes needed
4. Approved PRs are merged
5. Contributors are credited

## Development Tips

### Testing Changes Locally

```bash
# Test on sample code
mkdir test_project
echo "def hello(): print('world')" > test_project/sample.py
python3 pycerfl.py directory test_project

# Verify output
cat data.json
cat DATA_JSON/summary_data.json
```

### Debugging

Add debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def analyze_node(node):
    logger.debug(f"Analyzing node: {ast.dump(node)}")
    # Analysis code
```

### Performance Testing

For performance improvements:

```bash
# Time analysis
time python3 pycerfl.py directory large_project

# Profile code
python3 -m cProfile -o profile.stats pycerfl.py directory large_project
python3 -m pstats profile.stats
```

## Documentation Contributions

### Documentation Types

1. **Code Documentation**: Docstrings and inline comments
2. **User Documentation**: Guides and tutorials
3. **API Documentation**: Function and class references
4. **Examples**: Real-world usage examples

### Building Documentation Locally

```bash
cd docs

# If using Jekyll locally
bundle install
bundle exec jekyll serve

# Open http://localhost:4000 in browser
```

### Documentation Best Practices

- Write for your audience (beginners vs experts)
- Include practical examples
- Keep it up to date with code changes
- Use consistent formatting
- Add screenshots for UI features
- Link related documentation

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Assume good intentions
- Give constructive feedback
- Focus on the code, not the person

### Communication

- **Issues**: Bug reports and feature requests
- **Discussions**: Questions and general conversation
- **Pull Requests**: Code contributions
- **Email**: For sensitive matters

## Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- README.md (for significant contributions)

## Questions?

- Open an [issue](https://github.com/raux/pycefrl/issues) for bugs or features
- Start a [discussion](https://github.com/raux/pycefrl/discussions) for questions
- Check existing issues and discussions first

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Thank You!

Your contributions help make pycefrl better for everyone. Whether it's a small typo fix or a major feature, every contribution is valued and appreciated! 🎉

## Next Steps

- Read the [User Guide](./guide) to understand the project better
- Check the [API Reference](./api) for technical details
- Explore [Examples](./examples) for inspiration
- Browse [open issues](https://github.com/raux/pycefrl/issues) for contribution ideas
