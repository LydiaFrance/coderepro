#from github import Github
from ollama import Client
import ast
import os
import random

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

with open('prompts.txt', 'r') as file:
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

folder_path = '/Users/danield/PycharmProjects/coderepro/coderepro/temp_repo/output/python/'
all_files = os.listdir(folder_path)
selected_files = random.sample(all_files, 5)

file_contents_codequality = []
for i, file_name in enumerate(selected_files):
  file_path = os.path.join(folder_path, file_name)
  with open(file_path, 'r') as file:
    file_contents_codequality.append(file.read())

folder_path = '/Users/danield/PycharmProjects/coderepro/coderepro/temp_repo/output/documenation/'
all_files = os.listdir(folder_path)
selected_files = random.sample(all_files, 5)
file_contents_documentation = []

for i, file_name in enumerate(selected_files):
  file_path = os.path.join(folder_path, file_name)
  with open(file_path, 'r') as file:
    file_contents_documentation.append(file.read())

folder_path = '/Users/danield/PycharmProjects/coderepro/coderepro/temp_repo/output/testing/'
all_files = os.listdir(folder_path)
selected_files = random.sample(all_files, 5)

file_contents_testing = []
for i, file_name in enumerate(selected_files):
  file_path = os.path.join(folder_path, file_name)
  with open(file_path, 'r') as file:
    file_contents_testing.append(file.read())

folder_path = '/Users/danield/PycharmProjects/coderepro/coderepro/temp_repo/output/notebooks'
all_files = os.listdir(folder_path)
selected_files = random.sample(all_files, 5)

file_contents_notebooks = []
for i, file_name in enumerate(selected_files):
  file_path = os.path.join(folder_path, file_name)
  with open(file_path, 'r') as file:
    file_contents_notebooks.append(file.read())
# f = open('/Users/danield/PycharmProjects/coderepro/coderepro/output_curaitor.txt')
# print(f.read())
# [Code quality, Documentation, Testing, Juypter Notebook check]

  for i, chunk in enumerate(file_contents_codequality):
    response = talk_to_llama(context=chunk, prompt=prompt[0])
    with open(f"response_codequality_{i+1}.txt", 'w') as file:
      file.write(response)
  for i, chunk in enumerate(file_contents_documentation):
    response = talk_to_llama(context=chunk, prompt=prompt[1])
    with open(f"response_documentation_{i+1}.txt", 'w') as file:
      file.write(response)
  for i, chunk in enumerate(file_contents_testing):
    response = talk_to_llama(context=chunk, prompt=prompt[2])
    with open(f"response_testing_{i+1}.txt", 'w') as file:
      file.write(response)
  for i, chunk in enumerate(file_contents_notebooks):
    response = talk_to_llama(context=chunk, prompt=prompt[3])
    with open(f"response_notebooks_{i+1}.txt", 'w') as file:
      file.write(response)


