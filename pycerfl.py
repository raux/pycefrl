#-- MAIN PROGRAMME

import ast
import os
import csv
from ClassIterTree import IterTree
from getjson import read_Json
from getcsv import read_FileCsv
import sys
import shlex, subprocess
import json
import requests
from datetime import datetime

#-- Create lists of each attribute
Literals = ['ast.List', 'ast.Tuple', 'ast.Dict']
Variables = ['ast.Name']
Expressions = ['ast.Call', 'ast.IfExp', 'ast.Attribute']
Comprehensions = ['ast.ListComp','ast.GeneratorExp', 'ast.DictComp']
Statements = ['ast.Assign', 'ast.AugAssign', 'ast.Raise', 'ast.Assert','ast.Pass']
Imports = ['ast.Import', 'ast.ImportFrom']
ControlFlow = ['ast.If', 'ast.For', 'ast.While', 'ast.Break', 'ast.Continue',
                'ast.Try', 'ast.With']
FunctionsClass = ['ast.FunctionDef', 'ast.Lambda', 'ast.Return', 'ast.Yield',
                  'ast.ClassDef']

#-- Create list of attribute lists
SetClass = [Literals, Variables, Expressions, Comprehensions, Statements,
            Imports, ControlFlow, FunctionsClass]

#-- Global storage for results
global_csv_rows = []
global_json_data = {}

#-- Global counters for progress tracking
total_files_found = 0
files_processed = 0

def choose_option():
    """ Choose option. """
    global total_files_found, files_processed
    
    # Reset counters
    files_processed = 0
    
    if type_option == 'directory':
        repo = option.split('/')[-1]
        # Count files before processing
        print('🔍 Counting Python files...')
        sys.stdout.flush()
        total_files_found = count_python_files(option)
        print(f'📊 Found {total_files_found} Python file(s) to analyze')
        sys.stdout.flush()
        read_Directory(option, repo)
    elif type_option == 'repo-url':
        request_url()
    elif type_option == 'user':
        run_user()
    else:
        sys.exit('Incorrect Option')


def request_url():
    """ Request url by shell. """
    values = option.split("/")
    try:
        protocol = values[0].split(':')[0]
        type_git = values[2]
        user = values[3]
        repo = values[4][0:-4]
    except:
        sys.exit('ERROR --> Usage: http://TYPEGIT/USER/NAMEREPO.git')
    #-- Check url
    check_url(protocol, type_git)
    #-- Check languaje
    check_lenguage(option, protocol, type_git, user, repo)


def check_url(protocol, type_git):
    """ Check url sintax. """
    if protocol != 'https':
        sys.exit('Usage: https protocol')
    elif type_git != 'github.com':
        sys.exit('Usage: github.com')


def check_lenguage(url, protocol, type_git, user, repo):
    """ Check lenguaje python. """
    total_elem = 0
    python_leng = False
    python_quantity = 0
    #-- Create the url of the api
    repo_url = (protocol + "://api." + type_git + "/repos/" + user + "/" +
                 repo + "/languages")
    print("Analyzing repository languages...")
    sys.stdout.flush()
    # Get content
    r = requests.get(repo_url)
    # Decode JSON response into a Python dict:
    content = r.json()
    #-- Get used languages and their quantity
    for key in content.keys():
        print(key + ": " + str(content[key]))
        sys.stdout.flush()
        if key == 'Python':
            python_leng = True
            python_quantity = content[key]
        total_elem += content[key]
    #-- Check if python is 50%
    if python_leng == True:
        amount = total_elem/2
        if python_quantity >= amount:
            print('\n✓ Python 50% OK')
            sys.stdout.flush()
            #-- Clone the repository
            run_url(url)
        else:
            print('\n✗ The repository does not contain 50% of the Python.')
            sys.stdout.flush()


def run_url(url):
    """ Run url. """
    command_line = "git clone " + url
    print('⏳ Cloning repository...')
    sys.stdout.flush()
    #print(command_line)
    #-- List everything and separate
    args = shlex.split(command_line)
    #-- Run in the shell the command_line
    subprocess.call(args)
    print('✓ Repository cloned successfully')
    sys.stdout.flush()
    get_directory(url)


def run_user():
    """ Run user. """
    #-- Create the url of the api
    user_url = ("https://api.github.com/users/"  + option)
    print(user_url)
    print("Analyzing user...")
    sys.stdout.flush()
    try:
        #-- Extract headers
        headers = requests.get(user_url)
        #-- Decode JSON response into a Python dict:
        content = headers.json()
        #-- Get repository url
        repo_url = content["repos_url"]
    except KeyError:
        sys.exit('An unavailable user has been entered')
    print("Analyzing repositories...")
    sys.stdout.flush()
    #-- Extract repository names
    names = requests.get(repo_url)
    #-- Decode JSON response into a Python dict:
    content = names.json()
    #-- Show repository names
    for repository in content:
        print('\nRepository: ' + str(repository["name"]))
        sys.stdout.flush()
        url = ("https://github.com/" + option + "/" + repository["name"])
        check_lenguage(url, 'https', 'github.com', option, repository["name"])


def get_directory(url):
    """ Get the name of the downloaded repository directory. """
    #-- Get values rom the url
    values = url.split('/')
    #-- Last item in the list
    name_directory = values[-1]
    #-- Remove extension .git
    if ('.git' in str(name_directory)):
        name_directory = name_directory[0:-4]
    print("The directory is: " + name_directory)
    get_path(name_directory)


def get_path(name_directory):
    """ Get the path to the directory. """
    global total_files_found
    
    absFilePath = os.path.abspath(name_directory)
    #-- Check if the last element is a file.py
    fichero = absFilePath.split('/')[-1]
    if fichero.endswith('.py'):
        absFilePath = absFilePath.replace("/" + fichero,"" )
    print("This script absolute path is ", absFilePath)
    sys.stdout.flush()
    
    # Count files before processing
    print('🔍 Counting Python files...')
    sys.stdout.flush()
    total_files_found = count_python_files(absFilePath)
    print(f'📊 Found {total_files_found} Python file(s) to analyze')
    sys.stdout.flush()
    
    read_Directory(absFilePath, name_directory)


def count_python_files(absFilePath):
    """ Count total Python files in directory tree. """
    count = 0
    try:
        for root, dirs, files in os.walk(absFilePath):
            for file in files:
                if file.endswith('.py'):
                    count += 1
    except Exception as e:
        print(f"Error counting files in {absFilePath}: {e}")
        sys.stdout.flush()
    return count


def read_Directory(absFilePath, repo):
    """ Extract the .py files from the directory. """
    global total_files_found, files_processed
    
    try:
        pos = ''
        print(f'📁 Scanning directory: {absFilePath}')
        sys.stdout.flush()
        path = absFilePath
        directory = os.listdir(path)
        
        # Count python files in current directory
        py_files = [f for f in directory if f.endswith('.py')]
        if py_files:
            print(f'   Found {len(py_files)} Python file(s)')
            sys.stdout.flush()
        
        for i in range(0, len(directory)):
            if directory[i].endswith('.py'):
                files_processed += 1
                print(f'📄 [{files_processed}/{total_files_found if total_files_found > 0 else "?"}] Processing: {directory[i]}')
                sys.stdout.flush()
                pos = path + "/" + directory[i]
                read_File(pos, repo)
                print(f'   ✓ Completed: {directory[i]}')
                sys.stdout.flush()
            elif not ('.') in directory[i]:
                path2 =  absFilePath + '/' + directory[i]
                if os.path.isdir(path2):
                    print(f'\n📂 Entering subdirectory: {directory[i]}')
                    sys.stdout.flush()
                    read_Directory(path2, directory[i])
    except Exception as e:
        print(f"Error processing {absFilePath}: {e}")
        sys.stdout.flush()


def read_File(pos, repo):
    """ Read the file and return the tree. """
    with open(pos) as fp:
        my_code = fp.read()
        tree = ast.parse(my_code)
        #print (ast.dump(tree))
        iterate_List(tree, pos, repo)


def iterate_List(tree, pos, repo):
    """ Iterate list and assign attributes."""
    for i in range(0, len(SetClass)):
        for j in range(0, len(SetClass[i])):
            attrib = SetClass[i][j]
            deepen(tree, attrib, pos,repo)


def deepen(tree, attrib, pos, repo):
    """ Create class object. """
    file = pos.split('/')[-1]
    object = IterTree(tree, attrib, file, repo)
    
    # Collect results
    csv_rows, json_data = object.get_results()
    
    if csv_rows:
        global_csv_rows.extend(csv_rows)
        
    if json_data:
        for repo_key, files in json_data.items():
            if repo_key not in global_json_data:
                global_json_data[repo_key] = {}
            
            for file_key, data_list in files.items():
                if file_key not in global_json_data[repo_key]:
                    global_json_data[repo_key][file_key] = []
                
                global_json_data[repo_key][file_key].extend(data_list)


def save_collected_data():
    """ Save collected data to files. """
    print('\n💾 Saving results...')
    sys.stdout.flush()
    
    # Save CSV
    with open('data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Repository', 'File Name', 'Class', 'Start Line', 'End Line', 'Displacement', 'Level'])
        writer.writerows(global_csv_rows)
    print('   ✓ CSV data saved to data.csv')
    sys.stdout.flush()
        
    # Save JSON
    with open('data.json', 'w') as f:
        json.dump(global_json_data, f, indent=4)
    print('   ✓ JSON data saved to data.json')
    sys.stdout.flush()

def summary_Levels():
    """ Summary of directory levels """
    save_collected_data()
    print('\n📊 Generating summary statistics...')
    sys.stdout.flush()
    result = read_Json()
    read_FileCsv()
    print('\n✅ Analysis complete!')
    print(f'\n{result}')
    sys.stdout.flush()


if __name__ == "__main__":
    try:
        type_option = sys.argv[1]
        option = sys.argv[2].strip()
    except:
        sys.exit("Usage: python3 file.py type-option('directory', 'repo-url', 'user') option(directory, url, user)")
    
    # Print banner
    print('=' * 60)
    print('  PyCEFRL - Python Code Level Analyzer')
    print('  Real-time Analysis Mode')
    print('=' * 60)
    print(f'Started at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Mode: {type_option}')
    print(f'Target: {option}')
    print('=' * 60)
    sys.stdout.flush()
    
    choose_option()
    summary_Levels()
    
    print('=' * 60)
    print(f'Finished at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 60)
    sys.stdout.flush()
