import subprocess
import click
import requests
from pathlib import Path
import logging

BERT_URL = "https://cernbox.cern.ch/remote.php/dav/public-files/QV47M3dk0eXGdbe/bert_classifier.pt"
CWD = Path(__file__).resolve().parent
# Logging format
LOGGING_FMT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGING_DATE_FMT = "%d-%b-%y %H:%M:%S"

def run_bash_script(script_path, repo_url):
    script_full_path = CWD / script_path
    try:
        logging.info(f"Running script '{script_path}' with repo_url '{repo_url}'...")
        result = subprocess.run(['bash', str(script_full_path), repo_url], check=True, text=True, capture_output=True)
        print("Script Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the script: {e.stderr}")

def check_directory_and_file(directory_path, file_name):
    dir_path = Path(directory_path)
    file_path = dir_path / file_name

    if dir_path.is_dir() and file_path.is_file():
        return True
    elif not dir_path.is_dir():
        return f"Directory '{directory_path}' does not exist."
    elif not file_path.is_file():
        return f"File '{file_name}' does not exist in directory '{directory_path}'."

def download_file_http(url, local_filename):
    # If the local filename directory does not exist, create it
    local_filename.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def download_bert():
    if check_directory_and_file(CWD / "data", "bert_classifier.pt") is not True:
        logging.info("Downloading BERT model to 'data/bert_classifier.pt'...")
        download_file_http(BERT_URL, CWD / "data/bert_classifier.pt")


@click.command()
@click.argument('repo_url')
def main(repo_url):
    logging.basicConfig(
        level=logging.INFO, format=LOGGING_FMT, datefmt=LOGGING_DATE_FMT
    )
    download_bert()
    run_bash_script('get_repo.sh', repo_url)

if __name__ == "__main__":
    main()

