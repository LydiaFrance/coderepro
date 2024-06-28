#from github import Github
from pathlib import Path
from ollama import Client
import ast
import os
import random
from folder_to_text import find_script_path, find_repo_path

file_contents_notebooks = []
file_contents_testing = []
file_contents_documentation = []
file_contents_codequality = []

CWD = Path(__file__).resolve().parent

client = Client(host='http://localhost:11434')
def talk_to_llama(context, prompt):
  concat = f"CONTEXT: {context} \n INSTRUCTIONS: {prompt}"
  response = client.chat(model='llama3', messages=[
    {
      'role': 'user',
      'content': concat,
    },
  ])
  return response["message"]["content"]

#gh = Github()

#for repo in gh.get_user().get_repos():
#    print(repo.name)
#repo = gh.get_repo("LydiaFrance/coderepro")

#contents = repo.get_contents("")

#dirfiles = []
#while contents:

#    file_content = contents.pop(0)

#    if file_content.type == "dir":

#        contents.extend(repo.get_contents(file_content.path))

#    else:

        #print(file_content)
#        dirfiles.append(file_content)

with open(CWD / 'prompts.txt', 'r') as file:
  fcontents = file.read()
prompt = ast.literal_eval(fcontents)

# List of text files to read for RAG
# file_names = ["documentation1.txt", "documentation2.txt", "documentation3.txt"]

#folder_path = '/Users/danield/PycharmProjects/coderepro/'
#all_files = os.listdir(folder_path)
#selected_files = random.sample(all_files, 5)

#file_contents_general_checks = []
#for i, file_name in enumerate(selected_files):
#    file_path = os.path.join(folder_path, file_name)
#    with open(file_path, 'r') as file:
#        file_contents_general_checks.append(file.read())

script_path, root_path = find_script_path()
target_repo_path = find_repo_path(root_path)
output_path = os.path.dirname(target_repo_path) + "/output"

folder_path = f'{output_path}/chunked_text_for_llms/python_scripts'
if (len(os.listdir(folder_path)) <= 1):
  pass
else:
  all_files = os.listdir(folder_path)
  selected_files = random.sample(all_files, 1)

  file_contents_codequality = []
  for i, file_name in enumerate(selected_files):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
      file_contents_codequality.append(file.read())

folder_path = f'{output_path}/chunked_text_for_llms/markdown'
if (len(os.listdir(folder_path)) <= 1):
  pass
else:
  all_files = os.listdir(folder_path)
  selected_files = random.sample(all_files, 1)
  file_contents_documentation = []

  for i, file_name in enumerate(selected_files):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
      file_contents_documentation.append(file.read())

folder_path = f'{output_path}/chunked_text_for_llms/test_files'
if (len(os.listdir(folder_path)) <= 1):
  pass
else:
  all_files = os.listdir(folder_path)
  selected_files = random.sample(all_files, 1)

  file_contents_testing = []
  for i, file_name in enumerate(selected_files):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
      file_contents_testing.append(file.read())

folder_path = f'{output_path}/chunked_text_for_llms/notebooks'
if (len(os.listdir(folder_path)) <= 1):
  pass
else:
  all_files = os.listdir(folder_path)
  selected_files = random.sample(all_files, 1)

  file_contents_notebooks = []
  for i, file_name in enumerate(selected_files):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
      file_contents_notebooks.append(file.read())
# f = open('/Users/danield/PycharmProjects/coderepro/coderepro/output_curaitor.txt')
# print(f.read())
# [Code quality, Documentation, Testing, Juypter Notebook check]

if file_contents_codequality:
  for i, chunk in enumerate(file_contents_codequality):
    response = talk_to_llama(context=chunk, prompt=prompt[0])
    with open(f"./temp_repo/output/response_codequality_{i+1}.txt", 'w') as file:
      file.write(response)
else:
  with open(f"./temp_repo/output/response_codequality_{i+1}.txt", 'w') as file:
      file.write("File is not present in the repository")
if file_contents_documentation:
  for i, chunk in enumerate(file_contents_documentation):
    response = talk_to_llama(context=chunk, prompt=prompt[1])
    with open(f"./temp_repo/output/response_documentation_{i+1}.txt", 'w') as file:
      file.write(response)
else:
  with open(f"./temp_repo/output/response_documentation_{i+1}.txt", 'w') as file:
      file.write("File is not present in the repository")
if file_contents_testing:
  for i, chunk in enumerate(file_contents_testing):
    response = talk_to_llama(context=chunk, prompt=prompt[2])
    with open(f"./temp_repo/output/response_testing_{i+1}.txt", 'w') as file:
      file.write(response)
else:
  with open(f"./temp_repo/output/response_testing_{i+1}.txt", 'w') as file:
      file.write("File is not present in the repository")
if file_contents_notebooks:
  for i, chunk in enumerate(file_contents_notebooks):
    response = talk_to_llama(context=chunk, prompt=prompt[3])
    with open(f"./temp_repo/output/response_notebooks_{i+1}.txt", 'w') as file:
      file.write(response)
else:
  with open(f"./temp_repo/output/response_notebooks_{i+1}.txt", 'w') as file:
      file.write("File is not present in the repository")
