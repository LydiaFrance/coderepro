import os
import re
from datetime import datetime
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
    
# Define the paths to the local repositories
repo_paths = os.scandir("/Users/danield/PycharmProjects/coderepro/coderepro")
output_path = "/Users/danield/PycharmProjects/coderepro/coderepro/temp_repo/output"
output_filename = "output"
selected_file_types = [".yaml"]
filter_files = False

    # Create an instance of LocalRepoScraper
scraper = LocalRepoScraper(repo_paths, output_path, output_filename, selected_file_types, filter_files)

    # Run the scraper
scraper.run()
