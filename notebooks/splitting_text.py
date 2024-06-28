from langchain_text_splitters import CharacterTextSplitter
import folder_to_text
from folder_to_text import target_repo_path, converted_notebooks, python_files, md_files
import os

NCHAR=7000

def add_fname_to_content(file_path):
    # Open the target file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Append the name of the file to the start of the content
    relative_path = os.path.basename(file_path)
    file_content = ""
    file_content += f"\n'''--- {relative_path} ---\n"
    file_content += content
    return file_content

def split_by_character(content, keyword):
    text_splitter = CharacterTextSplitter(
        separator=keyword,
        chunk_size=NCHAR,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )
    chunked_text = text_splitter.create_documents([content])
    return chunked_text

def chunk_markdown_scripts(mdcontent):
    if len(mdcontent) > NCHAR:
        # Split the content by class
        mdcontent = split_by_character(mdcontent, keyword = '#')
        if len(mdcontent) > NCHAR: 
            mdcontent = split_by_character(mdcontent, keyword = '\n')
    return mdcontent

def chunk_python_scripts(pycontent):
    if len(pycontent) > NCHAR:
        # Split the content
        pycontent = split_by_character(pycontent, keyword = 'class ')
        if len(pycontent) > NCHAR: 
            pycontent = split_by_character(pycontent, keyword = 'def ')
            if len(pycontent) > NCHAR:
                pycontent = split_by_character(pycontent, keyword = '\n\n')
    return pycontent

def chunk_notebooks(nbcontent):
    if len(nbcontent) > NCHAR:
        # Split the content 
        nbcontent = split_by_character(nbcontent, keyword = '```')
    return nbcontent

# Create a new folder inside the temp_repo to store chunked text
text_outputs = os.path.join(target_repo_path, "chunked_text_for_llms")
os.mkdir(text_outputs)

# For notebooks
notebook_outputs = os.path.join(text_outputs, "notebooks")
os.mkdir(notebook_outputs)

content_to_chunk = ""
for file in converted_notebooks:
    content_to_chunk += add_fname_to_content(file)

chunked_notebooks = chunk_notebooks(content_to_chunk)

# Print the chunks
for index, text in enumerate(chunked_notebooks):
    output_fname = notebook_outputs + "/chunk" + str(index) + ".txt"
    with open(output_fname, "w", encoding='utf-8') as f:
        f.write(text.page_content)

# For markdown documentation
md_outputs = os.path.join(text_outputs, "markdown")
os.mkdir(md_outputs)

content_to_chunk = ""
for file in md_files:
    content_to_chunk += add_fname_to_content(file)

chunked_md = chunk_markdown_scripts(content_to_chunk)

# Print the chunks
for index, text in enumerate(chunked_md):
    output_fname = md_outputs + "/chunk" + str(index) + ".txt"
    with open(output_fname, "w", encoding='utf-8') as f:
        f.write(text.page_content)

# For python scripts
py_outputs = os.path.join(text_outputs, "python_scripts")
os.mkdir(py_outputs)

content_to_chunk = ""
for file in python_files:
    content_to_chunk += add_fname_to_content(file)

chunked_py = chunk_python_scripts(content_to_chunk)

# Print the chunks
for index, text in enumerate(chunked_py):
    output_fname = py_outputs + "/chunk" + str(index) + ".txt"
    with open(output_fname, "w", encoding='utf-8') as f:
        f.write(text.page_content)
