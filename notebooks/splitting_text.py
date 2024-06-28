import re
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


def chunk_content_with_delimiters(content, splitters):

    def split_and_keep_delimiters(content, delimiter):
        parts = re.split(f'({delimiter})', content)

        chunks = []
        # Combine each pair of parts
        for i in range(0, len(parts) - 1, 2):
            chunk = parts[i] + parts[i + 1]
            chunks.append(chunk)

        # Add the last part if it's not empty
        if parts[-1]:
            chunks.append(parts[-1])

        return chunks
    
    def recursive_split(content, splitters):
        # Base case: no more splitters
        if not splitters:
            return [content]

        # Split the content using the first splitter
        delimiter = splitters[0]
        splits = split_and_keep_delimiters(content, delimiter)

        # Recursively split each chunk
        result = []
        for split in splits:
            split = re.sub(r'\n+', '\n', split)  # Replace multiple newlines with a single newline
            if len(split) > NCHAR and len(splitters) > 1:
                result.extend(recursive_split(split, splitters[1:]))
            else:
                result.append(split)
    
        return result
    
    def force_split_chunks(chunks, max_length):
        """
        Splits chunks of text into smaller parts if they exceed a specified maximum length.

        Parameters:
        - chunks: A list of text chunks to be potentially split.
        - max_length: The maximum allowed length for any single chunk.

        Returns:
        A list of text chunks, none of which exceeds the specified maximum length.
        """
        final_splits = []
        for chunk in chunks:
            while len(chunk) > max_length:
                final_splits.append(chunk[:max_length])
                chunk = chunk[max_length:]
            final_splits.append(chunk)
        return final_splits
    
    def combine_chunks(chunks, max_length):
        """
        Combines chunks of text into larger parts until the total length of the combined text exceeds a specified maximum length.

        Parameters:
        - chunks: A list of text chunks to be combined.
        - max_length: The maximum allowed length for the combined text.

        Returns:
        A list of text chunks, each of which is the concatenation of the input chunks, such that no chunk exceeds the specified maximum length.
        """
        combined_chunks = []
        current_chunk = ""
        for chunk in chunks:
            # If adding the next chunk would exceed the maximum length, start a new chunk
            if len(current_chunk) + len(chunk) + 1 > max_length:
                combined_chunks.append(current_chunk)
                current_chunk = chunk
            else:
                # Add a newline between chunks
                current_chunk += "\n" + chunk if current_chunk else chunk

        # Add the last chunk if it's not empty
        if current_chunk:
            combined_chunks.append(current_chunk)

        return combined_chunks

    # Split the content recursively using the splitters. 
    # Always split by newline if the content is too long
    split_content = recursive_split(content, splitters + ['\n'])

    # Force split any chunks that are too long
    split_content = force_split_chunks(split_content, NCHAR)

    # Combine the chunks into parts that are not too long
    combined_content = combine_chunks(split_content, NCHAR)

    # Once again, remove multiple newlines
    combined_content = [re.sub(r'\n+', '\n', chunk) for chunk in combined_content]
    
    return combined_content

def add_fname_get_content(file_path):
    # Open the target file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Replace multiple newlines with a single newline
    content = re.sub(r'\n+', '\n', content)
    # Append the name of the file to the start of the content
    relative_path = os.path.basename(file_path)
    file_content = f"\n'''--- {relative_path} ---\n" + content
    return file_content


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

chunked_notebooks = chunk_content_with_delimiters(content_to_chunk, ['```python\n', '```markdown\n', '```\n'])

# Write the chunks to files
write_chunks_to_files(chunked_notebooks, notebook_outputs)

# ------- For markdown documentation -------
# Make the folder if it doesn't exist, clear files if it does
md_outputs = os.path.join(text_outputs, "markdown")
clear_output_dir(md_outputs)

content_to_chunk = ""
for file in md_files:
    content_to_chunk += add_fname_get_content(file)

chunked_md = chunk_content_with_delimiters(content_to_chunk, ['\n# ', '\n## ', '\n### ', '\n#### ', '\n##### '])

# Write the chunks to files
write_chunks_to_files(chunked_md, md_outputs)

# ------- For python scripts -------
# Make the folder if it doesn't exist, clear files if it does
py_outputs = os.path.join(text_outputs, "python_scripts")
clear_output_dir(py_outputs)

content_to_chunk = ""
for file in python_files:
    content_to_chunk += add_fname_get_content(file) 

chunked_py = chunk_content_with_delimiters(content_to_chunk, ['\nclass ', '\ndef ', '\nif ', '\nfor ', '\nwhile '])

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

chunked_test = chunk_content_with_delimiters(content_to_chunk, ['\nclass ','\ndef ', '\nif '])

# Write the chunks to files
write_chunks_to_files(chunked_test, test_outputs)