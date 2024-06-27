import os
from langchain_text_splitters import CharacterTextSplitter

NCHAR=7000

def add_fname_to_content(file_path):
    # Open the target file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Append the name of the file to the start of the content
    relative_path = os.path.basename(file_path)
    file_content = ""
    file_content += f"\n'''--- {relative_path} ---\n"
    file_content += "\n'''"
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
    return chunked_text[0].page_content

file_path = '/Users/user/Documents/CodeRepro/coderepro/notebooks/folder_to_text.py'

content_to_chunk = add_fname_to_content(file_path)

if len(content_to_chunk) > NCHAR:
    # Split the content by class
    content_to_chunk = split_by_character(content_to_chunk, keyword = 'class ')
    if len(content_to_chunk) > NCHAR: 
        content_to_chunk = split_by_character(content_to_chunk, keyword = 'def ')
        if len(content_to_chunk) > NCHAR:
            content_to_chunk = split_by_character(content_to_chunk, keyword = '\n\n')

print(content_to_chunk) 
