
#!/bin/bash

# Find the directory of the script
RELATIVE_PATH=$(dirname "$0")
echo $RELATIVE_PATH

BASH_PATH=$(realpath "$(dirname "$0")")
echo $BASH_PATH

CODEREPRO_PATH=$(realpath "$BASH_PATH"/../..)
echo $CODEREPRO_PATH

# Make a directory to clone the repo
cd $CODEREPRO_PATH
rm -rf $CODEREPRO_PATH/temp_repo/
mkdir -p temp_repo/
cd temp_repo/
echo $(pwd)

# # Clone the repo given by the user
REPO_URL=$1
git clone --depth 1 --no-checkout --filter=blob:none $REPO_URL

# Get the folder name of the repo
REPO_FOLDER=$(basename -s .git $REPO_URL)
cd $REPO_FOLDER
echo $(pwd)

# Initialise sparse-checkout
git sparse-checkout init

# # Replace .git/info/sparse-checkout with contents of sparse_file_exclude.txt
cat ${BASH_PATH}/sparse_file_exclude.txt > .git/info/sparse-checkout

# Now pull from github
git checkout
 
