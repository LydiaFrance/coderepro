#from github import Github
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

dirfiles = 'directory'

#prompt = "I want to create a python package from my github repo. The file structure is given. I need detailed advice on what files are missing or to include to make this good software."
prompt = """Act as a research software code expert.
Your task is to review the research software code and provide a detailed analysis and assessment of the quality of research software code. Consider the following in your review.
Repository overview: Provide a brief overview of the repository, including its purpose, and primary functionalities.
Code quality: Analyze the overall structure and organization of the code. Assess the readability and maintainability of the code. Look for consistent naming conventions,
clear documentation, and use of comments. Check for adherence to coding standards and best practices relevant to the Python language.
Documentation: Evaluate the quality and completeness of the documentation. Check if there are clear instructions on how to install, configure, and use the software.
Review the presence of comments within the code and the usefulness of those comments.
Testing: Assess the presence and quality of tests (unit tests, integration tests, etc.). Evaluate the coverage of the tests and how well they cover the codebase.
Identify any continuous integration or continuous deployment (CI/CD) setups and evaluate their effectiveness.
Dependencies and build system: Review the management of dependencies and the build system in use.
Check if the dependencies are up-to-date and if there are any deprecated or vulnerable packages being used.
Community and Collaboration: Evaluate the process for contributing to the project (presence of contribution guidelines, code of conduct, etc.).
Provide a detailed report summarizing the findings in each of these areas, highlighting strengths, weaknesses, and areas for improvement.
Include specific examples from the codebase to support your assessment where relevant."""

prompt = """Act as a research software code expert. Your task is to review the research software code and provide a detailed analysis and assessment of its quality in the following areas.
Code Quality:
Analyze the overall structure and organization of the code.
Assess the readability and maintainability of the code.
Look for consistent naming conventions, clear documentation, and use of comments.
Check for adherence to coding standards and best practices relevant to the Python language.
Documentation:
Do the authors clearly state what problems the software is designed to solve and who the target audience is?
Is there a clearly-stated list of dependencies?
Do the authors include examples of how to use the software (ideally to solve real-world analysis problems)?
Is the core functionality of the software documented to a satisfactory level (e.g., API method documentation)?
Testing:
Assess the presence of tests (unit tests, integration tests, etc.).
Are there automated tests or manual steps described so that the functionality of the software can be verified?
Provide a detailed review summarizing the findings in each of these areas, highlighting strengths, weaknesses, and areas for improvement.
"""

f = open('/Users/danield/PycharmProjects/coderepro/coderepro/output_curaitor.txt')
# print(f.read())
print(talk_to_llama(f.read(), prompt))

