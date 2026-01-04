---
layout: docs
title: Installation
description: How to install and set up pycefrl
toc: true
---

## Requirements

Before installing pycefrl, ensure you have:

- **Python 3.7 or higher**
- **pip** (Python package installer)
- **Git** (for cloning repositories)

## Installation Steps

### Step 1: Clone the Repository

Clone the pycefrl repository from GitHub:

```bash
git clone https://github.com/raux/pycefrl.git
cd pycefrl
```

### Step 2: Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes all necessary dependencies for running pycefrl.

### Step 3: Generate Level Dictionary

Before running your first analysis, you need to generate the level dictionary:

```bash
python3 dict.py
```

This creates a `dicc.txt` file that contains the level assignments for different Python code elements.

## Verify Installation

To verify that pycefrl is installed correctly, try running the help command:

```bash
python3 pycerfl.py --help
```

Or run a simple test analysis on the project itself:

```bash
python3 pycerfl.py directory .
```

This should generate `data.json` and `data.csv` files with the analysis results.

## Optional: Streamlit Interface

If you want to use the interactive Streamlit web interface, ensure Streamlit is installed:

```bash
pip install streamlit
```

Then launch the application:

```bash
streamlit run app.py
```

The Streamlit app will open in your default web browser, providing an interactive interface for running analyses and viewing results.

## Configuration

### Custom Level Assignments

You can customize the level assignments by editing the `configuration.cfg` file before running `dict.py`:

```bash
# Edit configuration.cfg with your preferred text editor
nano configuration.cfg

# Then regenerate the dictionary
python3 dict.py
```

The configuration file allows you to:
- Assign custom CEFR levels to different Python constructs
- Define which code elements should be tracked
- Customize analysis parameters

## Dependencies

The main dependencies include:

- **ast** (built-in): For parsing Python code
- **requests**: For fetching data from GitHub
- **pandas**: For data manipulation (optional, for Streamlit)
- **streamlit**: For the web interface (optional)
- **plotly**: For interactive visualizations (optional, for Streamlit)
- **matplotlib**: For charts (optional, for Streamlit)
- **psutil**: For system statistics (optional, for Streamlit)

## Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError`**
```
Solution: Ensure all dependencies are installed:
pip install -r requirements.txt
```

**Issue: `dicc.txt not found`**
```
Solution: Run the dictionary generation script:
python3 dict.py
```

**Issue: GitHub API rate limiting**
```
Solution: If analyzing many repositories, you may hit GitHub's API rate limit. 
Consider using a GitHub token or waiting before running more analyses.
```

## Next Steps

Now that pycefrl is installed, you can:

1. [Follow the Quick Start Guide](./quickstart) to run your first analysis
2. [Read the User Guide](./guide) for detailed usage information
3. [Explore Examples](./examples) to see pycefrl in action
4. [Check the API Reference](./api) for advanced usage

## Support

If you encounter any issues during installation:

- Check the [GitHub Issues](https://github.com/raux/pycefrl/issues) page
- Open a new issue with details about your problem
- Include your Python version, OS, and error messages

