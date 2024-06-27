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
    feedback_data[topic] = message

    # Write the updated feedback data back to the file
    with open(feedback_path, "w") as f:
        json.dump(feedback_data, f, indent=4)

def fetch_file_content(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8', errors='replace')
        
        file_content = f"\n'''--- {file_path} ---\n{content}\n'''"
        return file_content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def fetch_from_file_list(file_list):
    files_data = []
    for file_path in file_list:
        file_content = fetch_file_content(file_path)
        if file_content:
            files_data.append(file_content)
    return files_data


def write_to_file(files_data, output_path, filename):
    # Generate a timestamp and create the filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{filename}_{timestamp}.txt"
    
    # Combine the output path and filename to get the full output file path
    output_file_path = os.path.join(output_path, filename)
    
    # Write the collected file data to the output file
    with open(output_file_path, "w", encoding='utf-8') as f:
        f.write("*Local Files*\n")
        for file_data in files_data:
            f.write(file_data)
    return output_file_path

def clean_up_text(output_name):
    with open(output_name, 'r', encoding='utf-8') as f:
        text = f.read()
    cleaned_text = re.sub('\n{3,}', '\n\n', text)
    with open(output_name, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

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
                
            print(f"Converted {notebook_path} to {output_path}")
        except Exception as e:
            print(f"Error converting {notebook_path}: {e}")

# Define the paths to the local repositories
# find the path of this script
script_path, root_path = find_script_path()

# Use the root of this path to find the temp_repo folder
target_repo_path = find_repo_path(root_path)

# Find the path of the output folder
output_path = os.path.dirname(target_repo_path) + "/output"

# Make the folder if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)


# Search for License
license_files = find_files_with_keyword(target_repo_path, "license")
if len(license_files) == 0:
    feedback_message("missing_license", "No license file found. Without a license, others may not legally use, copy, modify, or distribute your code. Without a license, this creates legal uncertainty, reduces collaboration, and limits use.", output_path)

# Search for README
readme_file = find_files_with_keyword(target_repo_path, "readme")
if len(readme_file) == 0:
    feedback_message("missing_readme", "No readme file found. Without a readme, users won't know how to use or read your software.", output_path)


# Search for requirements
requirements_file = find_files_with_keyword(target_repo_path, [".toml","requirements.txt", "setup.py", ])
if len(requirements_file) == 0:
    feedback_message("missing_requirements", "Your repository is missing a requirements.txt, .toml, or setup.py file. Without these files, users and contributors cannot easily install dependencies or understand the project’s configuration, leading to difficulties in setting up and running the project.", output_path)


# Search for python files and make a list of their paths
python_files = find_files(target_repo_path, ".py")

# Search for markdown files and make a list of their paths
md_files = find_files(target_repo_path, ".md")


# Search for notebooks and make a list of their paths
notebook_files = find_files(target_repo_path, ".ipynb")



if len(notebook_files) == 0:
    feedback_message("missing_notebooks", "No Jupyter notebooks found. Jupyter notebooks are a great way to document your code, explain your thought process, and show examples of how to use your code.", output_path)
    converted_notebooks = []
else:
    # Create a new folder inside the temp_repo to store converted notebooks
    converted_folder = os.path.join(target_repo_path, "converted_notebooks")

    # Convert the notebooks to markdown
    convert_jupyter_notebooks(notebook_files, converted_folder)

    # Make a list of the converted notebooks
    converted_notebooks = find_files(converted_folder, ".md")

