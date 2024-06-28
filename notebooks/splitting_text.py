import folder_to_text
from folder_to_text import target_repo_path, converted_notebooks, python_files, md_files, test_files
import os

NCHAR=7000

def clear_output_dir(output_path):
    # Make the folder if it doesn't exist
    # Clear the folder if it exists, then recreate it
    if os.path.exists(output_path):
        for filename in os.listdir(output_path):
            file_path = os.path.join(output_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        # No need to recreate the test_outputs directory as it's not deleted
    else:
        # Make the folder if it doesn't exist
        os.makedirs(output_path)

def add_fname_get_content(file_path):
    # Open the target file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Append the name of the file to the start of the content
    relative_path = os.path.basename(file_path)
    file_content = ""
    file_content += f"\n'''--- {relative_path} ---\n"
    file_content += content
    return file_content

def chunk_markdown_scripts(mdcontent):
    # Split the content by hash
    hash_splits = mdcontent.split('#')
    # If any chunk is too long, split by newline
    newline_splits = []
    for chunk in hash_splits:
        if len(chunk) > NCHAR:
            newline_splits.extend(chunk.split('\n'))
        else:
            newline_splits.append(chunk)
    # If any chunk is too long, force split
    final_splits = []
    for chunk in newline_splits:
        if len(chunk) > NCHAR:
            final_splits.extend(chunk[:NCHAR])
        else:
            final_splits.append(chunk)
    # Combine all the chunks
    combined_splits = []
    current_chunk = ""
    for chunk in final_splits:
        if len(current_chunk) + len(chunk) + 1 > NCHAR:
            combined_splits.append(current_chunk)
            current_chunk = chunk
        else:
            current_chunk += "\n" + chunk if current_chunk else chunk

    if current_chunk:
        combined_splits.append(current_chunk)

    return combined_splits

def chunk_python_scripts(pycontent):
    # Split the content by class
    class_splits = pycontent.split('class ')
    # If any chunk is too long, split by def
    def_splits = []
    for chunk in class_splits:
        if len(chunk) > NCHAR:
            def_splits.extend(chunk.split('def '))
        else:
            def_splits.append(chunk)
    # If any chunk is too long, split by newline
    newline_splits = []
    for chunk in def_splits:
        if len(chunk) > NCHAR:
            newline_splits.extend(chunk.split('\n'))
        else:
            newline_splits.append(chunk)
    # If any chunk is too long, force split
    final_splits = []
    for chunk in newline_splits:
        if len(chunk) > NCHAR:
            final_splits.extend(chunk[:NCHAR])
        else:
            final_splits.append(chunk)
    # Combine all the chunks
    combined_splits = []
    current_chunk = ""
    for chunk in final_splits:
        if len(current_chunk) + len(chunk) + 1 > NCHAR:
            combined_splits.append(current_chunk)
            current_chunk = chunk
        else:
            current_chunk += "\n" + chunk if current_chunk else chunk

    if current_chunk:
        combined_splits.append(current_chunk)

    return combined_splits

def chunk_notebooks(nbcontent):
    # Split the content by ```
    hash_splits = nbcontent.split('```')
    # If any chunk is too long, split by newline
    newline_splits = []
    for chunk in hash_splits:
        if len(chunk) > NCHAR:
            newline_splits.extend(chunk.split('\n'))
        else:
            newline_splits.append(chunk)
    # If any chunk is too long, force split
    final_splits = []
    for chunk in newline_splits:
        if len(chunk) > NCHAR:
            final_splits.extend(chunk[:NCHAR])
        else:
            final_splits.append(chunk)
    # Combine all the chunks
    combined_splits = []
    current_chunk = ""
    for chunk in final_splits:
        if len(current_chunk) + len(chunk) + 1 > NCHAR:
            combined_splits.append(current_chunk)
            current_chunk = chunk
        else:
            current_chunk += "\n" + chunk if current_chunk else chunk

    if current_chunk:
        combined_splits.append(current_chunk)

    return combined_splits

def write_chunks_to_files(chunked_text, output_directory):
    """
    Writes each chunk of text to a separate file in the specified output directory.

    Parameters:
    - chunked_text: A list of text chunks to be written to files.
    - output_directory: The directory where the chunk files will be saved.
    """
    for index, text in enumerate(chunked_text):
        output_fname = os.path.join(output_directory, f"chunk{index}.txt")
        with open(output_fname, "w", encoding='utf-8') as f:
            f.write(text)



# Create a new folder inside the temp_repo to store chunked text
path_to_temp = os.path.dirname(target_repo_path)
text_outputs = os.path.join(path_to_temp, "output/chunked_text_for_llms")

# ------- For notebooks -------
# Make the folder if it doesn't exist, clear files if it does
notebook_outputs = os.path.join(text_outputs, "notebooks")
clear_output_dir(notebook_outputs)

content_to_chunk = ""
for file in converted_notebooks:
    content_to_chunk += add_fname_get_content(file)

chunked_notebooks = chunk_notebooks(content_to_chunk)

# Write the chunks to files
write_chunks_to_files(chunked_notebooks, notebook_outputs)

# ------- For markdown documentation -------
# Make the folder if it doesn't exist, clear files if it does
md_outputs = os.path.join(text_outputs, "markdown")
clear_output_dir(md_outputs)

content_to_chunk = ""
for file in md_files:
    content_to_chunk += add_fname_get_content(file)

chunked_md = chunk_markdown_scripts(content_to_chunk)

# Write the chunks to files
write_chunks_to_files(chunked_md, md_outputs)

# ------- For python scripts -------
# Make the folder if it doesn't exist, clear files if it does
py_outputs = os.path.join(text_outputs, "python_scripts")
clear_output_dir(py_outputs)

content_to_chunk = ""
for file in python_files:
    content_to_chunk += add_fname_get_content(file) 

chunked_py = chunk_python_scripts(content_to_chunk)

# Write the chunks to files
write_chunks_to_files(chunked_py, py_outputs)


# ------- For test files (tests) -------
# Make the folder if it doesn't exist, clear files if it does
test_outputs = os.path.join(text_outputs, "test_files")
clear_output_dir(test_outputs)

# Make the folder if it doesn't exist
if not os.path.exists(test_outputs):
    os.makedirs(test_outputs)

content_to_chunk = ""
for file in test_files:
    content_to_chunk += add_fname_get_content(file)

chunked_test = chunk_python_scripts(content_to_chunk)

# Write the chunks to files
write_chunks_to_files(chunked_test, test_outputs)