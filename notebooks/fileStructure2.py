import os
from ollama import Client
client = Client(host='http://localhost:11434')
import ast

# Function to read data chunks from text files
def read_data_chunks(file_names):
    chunks = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            chunks.append(file.read())
    return chunks


# Function to augment the prompt with retrieved chunks
def augment_query_with_chunks(query, chunks):
    augmented_query = query
    for i, chunk in enumerate(chunks):
        augmented_query += f"\nCONTEXT CHUNK {i + 1}: {chunk}"
    return augmented_query


# Function to interact with the Llama model
def talk_to_llama(context, prompt):
    concat = f"CONTEXT: {context}\nINSTRUCTIONS: {prompt}"
    response = client.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': concat,
        },
    ])
    return response["message"]["content"]


# Example usage
def main():
    query = "Explain the process of photosynthesis."
    with open('prompts.txt', 'r') as file:
        fcontents= file.read()
    prompts = ast.literal_eval(fcontents)
    # List of text files to read
    file_names = ["documentation1.txt", "documentation2.txt", "documentation3.txt"]

    # Read data chunks from text files
    chunks = read_data_chunks(file_names)

    # Augment the query with the retrieved chunks
    augmented_query = augment_query_with_chunks(query, chunks)

    # Get response from the Llama model
    response = talk_to_llama(augmented_query, prompt)
    print(response)


if __name__ == "__main__":
    main()
