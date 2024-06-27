NCHAR=7000

def add_fname(file_path):
    # bla bla samvida will do this

def split_by_class(file_path, keyword):
    # Open the target file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Check if the content length is over 7000 characters
    if len(content) > NCHAR:
        # Split the content by the keyword
        parts = content.split(keyword)
    
    # Initialize a list to hold the modified parts
    split_text = []
    
    # Iterate over each part
    for index, part in enumerate(parts, start=1):
        # Add the keyword back to the beginning of each part except the first one
        if index > 1:
            part = keyword + part
        split_text.append(part)
    
    # Return the list of modified parts
    return split_text

# Run on file to split text by class in first instance
file_path = '/Users/user/Documents/CodeRepro/coderepro/temp_repo/PyBaMM/setup.py'
keyword = 'class '
split_text = split_by_class(file_path, keyword)

def split_by_def(file_path, keyword):
    # Check if the content length is over 7000 characters
    if len(split_text) > NCHAR:
        # Split the content by the keyword
        parts = content.split(keyword)
    
    # Initialize a list to hold the modified parts
    further_split_text= []
    
    # Iterate over each part
    for index, part in enumerate(parts, start=1):
        # Add the keyword back to the beginning of each part except the first one
        if index > 1:
            part = keyword + part
        further_split_text.append(part)
    
    # Return the list of split text
    return further_split_text

from langchain_text_splitters import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=NCHAR,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)

# Only read in N+1 characters as we only want 
# to keep the first chunk anyway
def split_by_character_number(input_text, output_fname):
    text_to_chunk = input_text[:NCHAR+1]
    chunked_text = text_splitter.create_documents([text_to_chunk])
    return chunked_text[0].page_content

# Example usage
new_keyword = 'def '
further_split_text = split_by_class(file_path, keyword)
