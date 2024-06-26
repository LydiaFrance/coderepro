from github import Github
from ollama import Client
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

gh = Github()

#for repo in gh.get_user().get_repos():
#    print(repo.name)
repo = gh.get_repo("LydiaFrance/coderepro")

contents = repo.get_contents("")

dirfiles = []
while contents:

    file_content = contents.pop(0)

    if file_content.type == "dir":

        contents.extend(repo.get_contents(file_content.path))

    else:

        #print(file_content)
        dirfiles.append(file_content)

print(talk_to_llama(dirfiles, "Is this a good github directory structure for a python package?    Can you give tips on how to improve it?"))