# **pycefrl**
## *Identifying Python3 Code Level Using the CEFR Framework as Inspiration*

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://raux.github.io/pycefrl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**📚 [Full Documentation](https://raux.github.io/pycefrl) | 🎯 [Quick Start](https://raux.github.io/pycefrl/quickstart) | 📊 [Dashboard](https://raux.github.io/pycefrl/dashboard) | 💡 [Examples](https://raux.github.io/pycefrl/examples)**

### What is this project about?
The goal of pycefrl is to create a tool capable of obtaining an evaluation inspired by the [''Common European Framework of Reference for Languages''](https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages) for code written in the Python programming language, version 3.

With this tool it is possible to analyze the level of GitHub repositories (and their developers) or code snippets in Python3.



### How does it work?

To put it into operation you have to follow the steps below:
1. Edit the 'configuration.cfg' file with the level assignment of your choice. If you want to use the default ones (recommended), just go to step 2.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Execute the file 'dict.py' to generate a level dictionary.
   ```
   python3 dict.py
   ```
4. Execute the main program 'pycerfl.py' in three different ways:

    * Analyze a directory.
      ```
      python3 pycerfl.py directory <name_path>
      ```
    * Analyze a GitHub repository.
      ```
      python3 pycerfl.py repo <name_urlclone>
      ```
    * Analyze a GitHub user.
      ```
      python3 pycerfl.py user <name_user>
      ```
5. After that, this program will generate two types of formats to view the results:
    * **JSON**: data.json
    * **CSV**: data.csv

  Both of them including following information:
  * Repository name
  * File name
  * Class of element
  * Start Line
  * End Line
  * Displacement
  * Level of element


6. If you want to visualize the results on a web page (legacy method):

    * Run the file 'main.js' to create the page 'index.html'. You will get one web page for each repository.
      ```
      node main.js
      ```

## Interactive Web Interface (Streamlit)

A Streamlit application is included to easily run analyses and visualize results with interactive charts (Bubble Charts, Heatmaps, Treemaps) and system statistics.

To run the Streamlit app:

```bash
streamlit run app.py
```

**Features:**
- Select analysis mode: Directory, GitHub Repository, or GitHub User.
- Real-time execution logs and system stats (CPU/RAM).
- Interactive visualizations:
    - **Bubble Chart**: Category vs Level.
    - **File Heatmap**: File vs Level Count.
    - **Element Treemap**: Drill down into specific elements.
- Download reports in JSON and CSV formats.

## Running Tests

The project includes a suite of unit tests to ensure the accuracy of level detection for various Python structures.

To run the tests:

```bash
python3 -m unittest discover tests
```

The tests cover:
- Simple and nested lists/loops (A1, A2).
- Control flow (If, While, Try/Except).
- Function and Class definitions (B1).
- Advanced structures like List Comprehensions and Generators (C1).

## 📚 Documentation Website

A comprehensive documentation website is available at **[https://raux.github.io/pycefrl](https://raux.github.io/pycefrl)**

### Features:
- **Interactive Dashboard**: Visualize analysis results with charts and graphs
- **Complete Documentation**: Installation guides, tutorials, and API reference
- **Examples**: Real-world usage examples and best practices
- **Dark/Light Theme**: Modern, responsive design with theme support
- **Search & Navigation**: Easy to navigate with sidebar and breadcrumb navigation

Visit the website to explore:
- 📖 [Installation Guide](https://raux.github.io/pycefrl/installation)
- 🚀 [Quick Start Tutorial](https://raux.github.io/pycefrl/quickstart)
- 📘 [User Guide](https://raux.github.io/pycefrl/guide)
- 🔧 [API Reference](https://raux.github.io/pycefrl/api)
- 💡 [Examples](https://raux.github.io/pycefrl/examples)
- 📊 [Interactive Dashboard](https://raux.github.io/pycefrl/dashboard)
- 🤝 [Contributing Guidelines](https://raux.github.io/pycefrl/contributing)

## Contributing

Contributions are welcome! Please see our [Contributing Guidelines](https://raux.github.io/pycefrl/contributing) for details on how to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License

This project is licensed under the MIT License.

## Support

- 🐛 [Report Issues](https://github.com/raux/pycefrl/issues)
- 💬 [Discussions](https://github.com/raux/pycefrl/discussions)
- 📖 [Documentation](https://raux.github.io/pycefrl)
