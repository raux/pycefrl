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
      python3 pycerfl.py repo-url <name_urlclone>
      ```
    * Analyze a GitHub user.
      ```
      python3 pycerfl.py user <name_user>
      ```
    
    **Note**: All analysis modes now provide **real-time progress updates**, showing:
    - File count and processing progress
    - Current file being analyzed
    - Status indicators with emoji icons (📁, 📄, ✓, etc.)

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

A Streamlit application is included to easily run analyses and visualize results **in real-time** with interactive charts (Bubble Charts, Heatmaps, Treemaps) and system statistics.

To run the Streamlit app:

```bash
streamlit run app.py
```

**Real-time Analysis Features:**
- ⚡ **Live Progress Tracking**: Watch files being processed in real-time with progress bars
- 📊 **File-by-File Updates**: See detailed progress as each Python file is analyzed
- 💻 **System Resource Monitoring**: Monitor CPU and RAM usage during analysis
- 📈 **Streaming Logs**: View analysis logs as they happen with real-time updates

**Analysis Modes:**
- 📁 **Local Directory**: Analyze Python files in any directory on your system
- 🔗 **GitHub Repository**: Analyze any public GitHub repository by URL (with validation)
- 👤 **GitHub User**: Analyze all Python repositories of a GitHub user

**Visualization Features:**
- Interactive charts with detailed breakdowns:
    - **Bubble Chart**: Category vs Level visualization
    - **File Heatmap**: File vs Level Count distribution
    - **Element Treemap**: Drill down into specific code elements
- Download reports in JSON and CSV formats

**Screenshots:**

![PyCEFRL Web Interface](https://github.com/user-attachments/assets/123b3933-15fb-48dc-8312-4beea1ba7fba)
*Main interface showing real-time analysis features*

![GitHub Repository Analysis](https://github.com/user-attachments/assets/c84937f9-641f-411e-82ee-ce8b743365d6)
*GitHub repository URL validation and analysis*

## Deploying the Web Application

The Streamlit web application can be easily deployed to the cloud for public access. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick Deploy to Streamlit Cloud:**
1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io/)
3. Create new app pointing to `app.py`
4. Your app will be live at `https://your-app-name.streamlit.app`

For other deployment options (Docker, Heroku, Railway, Render), see the [deployment guide](DEPLOYMENT.md).


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
