import os
import re
from datetime import datetime
import json
import nbformat
from nbconvert import MarkdownExporter


def find_repo_path(current_path, temp_repo_dir="temp_repo"):

    # Find the path of the target repository
    target_repo_path = current_path + "/" + temp_repo_dir

    # Next find the target repo name.
    # - list the folders in the directory. 
    # - To make sure it only gets the first folder, it will break after the first folder is found
    directory_list = os.listdir(target_repo_path)
    for dir_name in directory_list:
        if dir_name.startswith("output") or dir_name.startswith("."):
            continue
        target_repo_name = dir_name
        break

    # Combine the path and the name
    target_repo_path = target_repo_path + "/" + target_repo_name

    return target_repo_path

def find_script_path():
    # find the path of this script
    script_path = os.path.realpath(__file__)

    # Find the directory of the script
    script_path = os.path.dirname(script_path)

    # Go up one directory
    root_path = os.path.dirname(script_path)

    return script_path, root_path

def find_files(directory, file_extension=".py"):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                python_files.append(os.path.join(root, file))
    return python_files


def find_files_with_keyword(directory, keyword):
    matched_files = []

    # If keyword is a list, loop through the list
    if isinstance(keyword, list):
        for key in keyword:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if key.lower() in file.lower():
                        matched_files.append(os.path.join(root, file))
        return matched_files
    elif isinstance(keyword, str):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if keyword.lower() in file.lower():
                    matched_files.append(os.path.join(root, file))
        return matched_files

def find_folders_with_keyword(base_path, dir_names):
    """
    Check for directories in the base path.
    """
    found_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and d.lower() in dir_names]
    return found_dirs

def check_folder_structure(base_path):
    depth_dict = {}
    subdir_count = {}
    for root, dirs, files in os.walk(base_path):
        depth = root.replace(base_path, '').count(os.sep)
        if depth not in depth_dict:
            depth_dict[depth] = 0
        depth_dict[depth] += 1

        subdir_count[depth] = len(dirs)

    return depth_dict, subdir_count

def evaluate_folder_structure(depth_dict, subdir_count):
    max_depth = max(depth_dict.keys())
    total_folders = sum(depth_dict.values())

    overview = []
    overview.append(f"The repository has a total of {total_folders} folders.")
    overview.append(f"The maximum depth of the folder structure is {max_depth}.")

    if max_depth == 0:
        overview.append("The repository has a completely flat structure. Consider organizing files into directories to improve manageability.")
    elif max_depth > 3:
        overview.append(f"The repository structure is quite deep. Consider simplifying the directory hierarchy to improve navigability.")

    for depth, count in depth_dict.items():
        overview.append(f"  Depth {depth}: {count} folder(s)")

    for dir_path, count in subdir_count.items():
        if count > 10:  # Arbitrary threshold for too many subdirectories
            overview.append(f"The directory '{dir_path}' contains too many subdirectories ({count}). Consider restructuring to improve clarity.")

    return "".join(overview)


def find_absolute_paths(repo_path):
    absolute_path_pattern = re.compile(r'(?:[A-Z]:\\|\/|Users|user|home)', re.IGNORECASE)

    hardcoded_paths = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, start=1):
                        if absolute_path_pattern.search(line):
                            hardcoded_paths.append((file_path, line_num, line.strip()))
            except (UnicodeDecodeError, IOError):
                continue

    return hardcoded_paths


def feedback_message(topic, message, output_path):
    """
    Add to a feedback .json file
    """
    feedback_path = os.path.join(output_path, "feedback.json")

    # Check if the file exists and load existing data
    if os.path.exists(feedback_path):
        with open(feedback_path, "r") as f:
            feedback_data = json.load(f)
    else:
        feedback_data = {}

    # Add the new feedback
    feedback_data[topic.upper()] = message

    # Write the updated feedback data back to the file
    with open(feedback_path, "w") as f:
        json.dump(feedback_data, f, indent=4)

def report_hardcoded_paths(hardcoded_paths, target_repo_path, output_path, feedback_message):
    """
    Reports hardcoded paths found in files by sending feedback messages.

    Parameters:
    - hardcoded_paths: A list of tuples containing the file path, line number, and the line content of the hardcoded path.
    - target_repo_path: The base path of the repository to calculate relative paths.
    - output_path: The path where the feedback messages are to be sent or stored.
    - feedback_message: A function to send or store feedback messages. It takes a type, message, and output path as arguments.
    """
    if hardcoded_paths:
        feedback_message("hardcoded_paths", "Absolute and hardcoded paths found in the following files:", output_path)
        for file_path, line_num, line in hardcoded_paths:
            relative_path = os.path.relpath(file_path, target_repo_path)
            feedback_message("hardcoded_path_detail", f"File: {relative_path}, Line: {line_num}, Content: '{line}'", output_path)


def convert_jupyter_notebooks(notebook_path_list, converted_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)

    # Create an instance of the MarkdownExporter
    exporter = MarkdownExporter()

    # Process each notebook
    for notebook_path in notebook_path_list:
        # Determine the output markdown file path
        notebook_name = os.path.basename(notebook_path)
        output_path = os.path.join(converted_folder, notebook_name.replace(".ipynb", ".md"))

        try:
            # Read the notebook content
            with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
                notebook_content = nbformat.read(notebook_file, as_version=4)

            # Convert the notebook to markdown
            (body, resources) = exporter.from_notebook_node(notebook_content)

            # Write the markdown content to the output file
            with open(output_path, 'w', encoding='utf-8') as md_file:
                md_file.write(body)
                
            #print(f"Converted {notebook_path} to {output_path}")
        except Exception as e:
            print(f"Error converting {notebook_path}: {e}")

# ----- Define the paths to the local repositories
# find the path of this script
script_path, root_path = find_script_path()

# Use the root of this path to find the temp_repo folder
target_repo_path = find_repo_path(root_path)

# ----- Setup output folder -----
# Find the path of the output folder
output_path = os.path.dirname(target_repo_path) + "/output"

# Make the folder if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# ----- Critique the file structure of the repository -----
depth_dict, subdir_count = check_folder_structure(target_repo_path)

# Evaluate and provide an overview of the folder structure
folder_structure_overview = evaluate_folder_structure(depth_dict, subdir_count)
feedback_message("folder_structure_overview", folder_structure_overview, output_path)



# ----- Search for src/source/app
source_folders = find_folders_with_keyword(target_repo_path, ["src", "source", "app"])
if len(source_folders) == 0:
    feedback_message("missing_src", "No source folder found. A source folder is a common convention for storing the main code of a project. It helps keep the project organized and makes it easier for others to understand the structure of the code.", output_path)

# ----- Search for tests
test_folders = find_folders_with_keyword(target_repo_path, ["tests", "test"])
test_files = find_files_with_keyword(target_repo_path, ["test", "tests"])
if len(test_folders) == 0 and len(test_files) == 0:
    feedback_message("missing_tests", "Couldn't find test files. Writing and running tests to ensure the correctness of your code. Without tests, it is difficult to verify that your code works as expected and to catch bugs early.", output_path)

# ----- Search for tutorials or examples
tutorial_files = find_files_with_keyword(target_repo_path, ["tutorial", "example"])
tutorial_folders = find_folders_with_keyword(target_repo_path, ["tutorial", "example"])
if len(tutorial_files) == 0 and len(tutorial_folders) == 0:
    feedback_message("missing_tutorials", "No tutorial or example files found. Tutorials and examples help users understand how to use your code and can serve as a reference for new contributors.", output_path)

# ----- Search for License
license_files = find_files_with_keyword(target_repo_path, "license")
if len(license_files) == 0:
    feedback_message("missing_license", "No license file found. Without a license, others may not legally use, copy, modify, or distribute your code. Without a license, this creates legal uncertainty, reduces collaboration, and limits use.", output_path)

# ----- Search for README
readme_file = find_files_with_keyword(target_repo_path, "readme")
if len(readme_file) == 0:
    feedback_message("missing_readme", "No readme file found. Without a readme, users won't know how to use or read your software.", output_path)


# ----- Search for requirements
requirements_file = find_files_with_keyword(target_repo_path, [".toml","requirements.txt", "setup.py", "setup", "requirements" ])
if len(requirements_file) == 0:
    feedback_message("missing_requirements", "Your repository is missing a requirements.txt, .toml, or setup.py file. Without these files, users and contributors cannot easily install dependencies or understand the project’s configuration, leading to difficulties in setting up and running the project.", output_path)



# ----- Search for docs
doc_folders = find_folders_with_keyword(target_repo_path, ["docs", "doc"])
if len(doc_folders) == 0:
    feedback_message("missing_docs", "Note: No docs folder found. Consider adding a docs folder -- it helps users and contributors understand how to use and contribute to the project.", output_path)

# ----- Search for data
data_folders = find_folders_with_keyword(target_repo_path, ["data"])
if len(data_folders) == 0:
    feedback_message("missing_data", "Note: No data folder found. For reproducibility, make sure data is available.", output_path)


# ----- Search for python files and make a list of their paths -----
python_files = find_files(target_repo_path, ".py")

# Exclude any test files from the list using the test_files list
if test_files:
    python_files = [file for file in python_files if file not in test_files]



# ----- Search for markdown files and make a list of their paths -----
md_files = find_files(target_repo_path, ".md")

# ----- Search for notebooks and make a list of their paths -----
notebook_files = find_files(target_repo_path, ".ipynb")

if len(notebook_files) == 0:
    feedback_message("missing_notebooks", "No Jupyter notebooks found. Jupyter notebooks are a great way to document your code, explain your thought process, and show examples of how to use your code.", output_path)
    converted_notebooks = []
else:
    # Create a new folder inside the temp_repo to store converted notebooks
    temp_repo_path = os.path.dirname(target_repo_path)
    converted_folder = os.path.join(temp_repo_path, "output/converted_notebooks")

    # Convert the notebooks to markdown
    # Check whether the converted folder has files already
    if not os.path.exists(converted_folder) or (len(os.listdir(converted_folder)) == 0):
        convert_jupyter_notebooks(notebook_files, converted_folder)

    # Make a list of the converted notebooks
    converted_notebooks = find_files(converted_folder, ".md")

# ----- Search for hardcoded and absolute paths
    hardcoded_paths = find_absolute_paths(target_repo_path)
    hardcoded_notebook_paths = find_absolute_paths(converted_folder)
    hardcoded_paths.extend(hardcoded_notebook_paths)
    if hardcoded_paths:
        feedback_message("hardcoded_paths", "Absolute and hardcoded paths found in the following files:", output_path)
        for file_path, line_num, line in hardcoded_paths:
            # relative version of the file path:
            relative_path = os.path.relpath(file_path, target_repo_path)
            feedback_message("hardcoded_path_detail", f"File: {relative_path}, Line: {line_num}, Content: '{line}'", output_path)

