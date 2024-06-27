import subprocess
import click
from pathlib import Path

def run_bash_script(script_path, repo_url):
    script_full_path = Path(__file__).resolve().parent / script_path
    try:
        result = subprocess.run(['bash', str(script_full_path), repo_url], check=True, text=True, capture_output=True)
        print("Script Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the script: {e.stderr}")

@click.command()
@click.argument('repo_url')
def main(repo_url):
    run_bash_script('get_repo.sh', repo_url)

if __name__ == "__main__":
    main()

