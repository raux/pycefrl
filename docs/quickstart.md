---
layout: docs
title: Quick Start Guide
description: Get up and running with pycefrl in just a few minutes
toc: true
---

## Overview

Get started with pycefrl in just a few minutes! This guide will walk you through running your first code analysis.

## Prerequisites

Make sure you have completed the [Installation](./installation) steps:
- ✅ Installed Python 3.7+
- ✅ Cloned the repository
- ✅ Installed dependencies
- ✅ Generated the level dictionary with `dict.py`

## Basic Usage

pycefrl can analyze code from three different sources:

### 1. Analyze a Local Directory

Analyze Python files in a local directory:

```bash
python3 pycerfl.py directory /path/to/your/project
```

Example:
```bash
# Analyze the current directory
python3 pycerfl.py directory .

# Analyze a specific project
python3 pycerfl.py directory ~/projects/my-python-app
```

### 2. Analyze a GitHub Repository

Analyze any public GitHub repository by providing its clone URL:

```bash
python3 pycerfl.py repo https://github.com/username/repository
```

Example:
```bash
python3 pycerfl.py repo https://github.com/django/django
```

### 3. Analyze a GitHub User

Analyze all public repositories of a GitHub user:

```bash
python3 pycerfl.py user username
```

Example:
```bash
python3 pycerfl.py user guido
```

## Understanding the Output

After running an analysis, pycefrl generates two output files:

### data.json

A JSON file containing detailed analysis results:

```json
{
  "Repository": "my-project",
  "File Name": "main.py",
  "Class": "Simple Function",
  "Start Line": 10,
  "End Line": 15,
  "Displacement": 4,
  "Level": "B1"
}
```

### data.csv

A CSV file with the same information in spreadsheet format:

```csv
Repository,File Name,Class,Start Line,End Line,Displacement,Level
my-project,main.py,Simple Function,10,15,4,B1
```

### Additional Files

The analysis also creates:
- `DATA_JSON/summary_data.json`: Aggregated level statistics
- `DATA_JSON/total_data.json`: File-level breakdown
- `DATA_CSV/*.csv`: Individual CSV files per analyzed file

## Interpreting Results

### CEFR Levels

Code elements are categorized into six levels:

| Level | Description | Examples |
|-------|-------------|----------|
| **A1** | Basic | Simple lists, assignments, print statements |
| **A2** | Elementary | File operations, simple loops, basic functions |
| **B1** | Intermediate | Functions with arguments, classes, try/except |
| **B2** | Upper Intermediate | Decorators, class inheritance, advanced functions |
| **C1** | Advanced | List comprehensions, generators, metaclasses |
| **C2** | Proficient | Complex comprehensions, advanced OOP patterns |

### Understanding the Fields

- **Repository**: Source repository or directory name
- **File Name**: Python file being analyzed
- **Class**: Type of code element (e.g., "Simple Function", "For Loop")
- **Start Line**: Line where the element starts
- **End Line**: Line where the element ends
- **Displacement**: Indentation level (spaces from left margin)
- **Level**: CEFR-inspired complexity level (A1-C2)

## Example Walkthrough

Let's analyze a simple Python file:

```python
# example.py
def greet(name):
    """A simple greeting function"""
    message = f"Hello, {name}!"
    print(message)
    return message

if __name__ == "__main__":
    greet("World")
```

Run the analysis:
```bash
python3 pycerfl.py directory .
```

Expected results might show:
- **Function definition** (B1): Lines 1-6
- **Assignment** (A1): Line 3
- **Print statement** (A1): Line 4
- **Return statement** (B1): Line 5
- **If statement** (A2): Line 7
- **Function call** (A2): Line 8

## Using the Streamlit Interface

For a more interactive experience, use the Streamlit web app:

```bash
streamlit run app.py
```

The interface provides:
1. **Mode Selection**: Choose between Directory, Repository, or User analysis
2. **Real-time Logs**: Watch the analysis progress
3. **System Stats**: Monitor CPU and RAM usage
4. **Visualizations**: 
   - Bubble charts showing category vs level
   - Heatmaps of file vs level distribution
   - Treemaps for drilling down into elements
5. **Downloads**: Export results as JSON or CSV

## Viewing Results on the Dashboard

Open the [Results Dashboard](./dashboard) in your web browser to:
- View interactive charts and visualizations
- Filter results by level or code element
- Explore file-by-file breakdowns
- Export customized reports

Simply load your `data.json` file in the dashboard to see the analysis.

## Common Use Cases

### Assess Code Complexity

Identify which files or functions have the highest complexity:

```bash
python3 pycerfl.py directory ./src
# Look for high concentrations of C1/C2 elements
```

### Compare Repositories

Analyze multiple repositories to compare complexity:

```bash
python3 pycerfl.py repo https://github.com/user/repo1
python3 pycerfl.py repo https://github.com/user/repo2
# Compare the summary_data.json files
```

### Track Learning Progress

Analyze your own code over time to see how your coding complexity evolves:

```bash
python3 pycerfl.py user your-github-username
# Review the distribution of levels in your projects
```

## Next Steps

Now that you've run your first analysis, explore:

- [User Guide](./guide) - Comprehensive guide to all features
- [Examples](./examples) - Real-world usage examples
- [API Reference](./api) - Detailed API documentation
- [Dashboard](./dashboard) - Interactive results viewer

## Tips and Best Practices

1. **Start Small**: Begin with a single file or small directory to familiarize yourself with the output
2. **Review Configuration**: Check `configuration.cfg` to understand and customize level assignments
3. **Use Visualizations**: The Streamlit app and dashboard make it easier to understand complex results
4. **Combine with Code Review**: Use pycefrl as part of your code review process to identify areas for improvement
5. **Track Changes**: Run periodic analyses to track how code complexity evolves over time

## Troubleshooting

**No output files generated?**
- Ensure the target contains Python (.py) files
- Check that `dicc.txt` exists (run `dict.py` if missing)
- Verify you have write permissions in the directory

**Empty or minimal results?**
- Some simple Python files may have few detectable elements
- Check that the files contain actual code (not just comments/docstrings)

**GitHub API errors?**
- You may be hitting rate limits; wait a few minutes and try again
- For private repositories, you'll need to clone them locally first

For more help, see the [Installation](./installation#troubleshooting) troubleshooting section.

