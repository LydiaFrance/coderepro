import os
import re
from datetime import datetime
import json
#from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, messagebox, Radiobutton, IntVar

class LocalRepoScraper:
    def __init__(self, repo_paths, output_path, output_filename, selected_file_types=[], filter_files=True):
        self.repo_paths = repo_paths
        self.output_path = output_path
        self.output_filename = output_filename
        self.selected_file_types = selected_file_types
        self.filter_files = filter_files

    def fetch_all_files(self):
        files_data = []
        for file_path in self.repo_paths:
            # Check if file type is in selected file types
            if not self.filter_files or any(file_path.endswith(file_type) for file_type in self.selected_file_types):
                relative_path = os.path.basename(file_path)
                print(relative_path)
                file_content = ""
                file_content += f"\n'''--- {relative_path} ---\n"
                try:
                    with open(file_path, 'rb') as f:  # Open file in binary mode
                        content = f.read()
                    try:
                        # Try decoding as UTF-8
                        content_decoded = content.decode('utf-8')
                    except UnicodeDecodeError:
                        # If decoding fails, replace non-decodable parts
                        content_decoded = content.decode('utf-8', errors='replace')
                    file_content += content_decoded
                except Exception as e:  # catch any reading errors
                    print(f"Error reading file {file_path}: {e}")
                    continue
                file_content += "\n'''"
                files_data.append(file_content)
                print(f"Processed file {file_path}: size {os.path.getsize(file_path)} bytes")  # Print file size
            else:
                print(f"Skipping file {file_path}: Does not match selected types.")
        return files_data

    def write_to_file(self, files_data):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{self.output_filename}_{timestamp}.txt"
        output_file_path = os.path.join(self.output_path, filename)
        with open(output_file_path, "w", encoding='utf-8') as f:
            f.write(f"*Local Files*\n")
            for file_data in files_data:
                f.write(file_data)
        return output_file_path

    def clean_up_text(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        cleaned_text = re.sub('\n{3,}', '\n\n', text)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

    def run(self):
        print("Fetching all files...")
        files_data = self.fetch_all_files()

        print("Writing to file...")
        filename = self.write_to_file(files_data)

        print("Cleaning up file...")
        self.clean_up_text(filename)

        print("Done.")
        return filename

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


# Search for BLAH
# readme_file = find_files_with_keyword(target_repo_path, "blah")
# if len(readme_file) == 0:
#     feedback_message("missing_readme", "No blah file found.", output_path)



# Search for python files and make a list of their paths
python_files = find_files(target_repo_path, ".py")
for file in python_files:
    print(file)

# Search for markdown files and make a list of their paths
md_files = find_files(target_repo_path, ".md")
for file in md_files:
    print(file)



# # Run the scraper
# all_repo_paths = Path(target_repo_path).glob("**/*")

# for path in all_repo_paths:
#     print(path)
# print(f"All repo paths: {all_repo_paths}")

# for root, d_names, f_names in os.walk(target_repo_path):
#     print(f"Root: {root}")
#     print(f"Dirs: {d_names}")
#     print(f"Files: {f_names}")
#     break



# repo_paths = Path("/Users/user/Documents/CodeRepro/coderepro/temp_repo/PyBaMM").glob("**/*")
# repo_paths = [str(repo_path) for repo_path in repo_paths]
# output_path = "/Users/user/Documents/CodeRepro/coderepro/temp_repo/output"
# output_filename = "output"
# selected_file_types = [".py",".md",".yaml"]
# filter_files = True

#     # Create an instance of LocalRepoScraper
# scraper = LocalRepoScraper(repo_paths, output_path, output_filename, selected_file_types, filter_files)

#     # Run the scraper
# scraper.run()