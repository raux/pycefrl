# **pycefr**
## *Identifying Python3 Code Level Using the CEFR Framework as Inspiration*

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://raux.github.io/pycefrl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


### What is this project about?
The goal of pycefrl is to create a tool capable of obtaining an evaluation inspired by the [''Common European Framework of Reference for Languages''](https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages) for code written in the Python programming language, version 3.

With this tool it is possible to analyze the level of GitHub repositories (and their developers) or code snippets in Python3.


### How does it work?

To put it into operation you have to follow the steps below:

1. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Edit the 'configuration.cfg' file with the level assignment of your choice. If you want to use the default ones (recommended), just go to step 3.
3. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
4. Execute the file 'dict.py' to generate a level dictionary.
   ```bash
   python3 dict.py
   ```
5. Execute the main program 'pycerfl.py' in three different ways:

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

## Interactive Web Interface (StreamLit)

A modern Flask-based web interface is included 

```bash
# Activate your virtual environment first
source venv/bin/activate
streamlit run app.py
```

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
