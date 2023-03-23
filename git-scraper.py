import os
import subprocess
import requests
import sys
import time
import shutil
import json
import uuid
from tqdm import tqdm

# Define the search phrase, number of repositories to check, and offset from command-line arguments
search_phrase = sys.argv[1]
return_count = int(sys.argv[2]) if len(sys.argv) > 2 else 100
offset = int(sys.argv[3]) if len(sys.argv) > 3 else 0

# Define the name of the output folder based on the search phrase and a random UUID
output_folder = search_phrase.replace(" ", "-") + "-" + str(int(time.time()))

# Create a new directory for the output
os.mkdir(output_folder)

# Define the GitHub API URL for searching repositories
api_url = "https://api.github.com/search/repositories"

# Define the search parameters for the GitHub API
params = {"q": search_phrase, "per_page": return_count, "page": (offset // return_count) + 1}

# Send a GET request to the GitHub API to search for repositories
response = requests.get(api_url, params=params)

# Parse the JSON response from the GitHub API and extract the repository URLs
repository_urls = []
if response.ok:
    total_count = response.json()["total_count"]
    while len(repository_urls) < min(return_count, total_count):
        for item in response.json()["items"]:
            repository_urls.append(item["clone_url"])
            if len(repository_urls) == min(return_count, total_count):
                break
        if len(repository_urls) < min(return_count, total_count):
            next_page = response.links.get("next")
            if next_page:
                response = requests.get(next_page["url"])
            else:
                break
else:
    print(f"Error: Failed to retrieve repositories for search phrase '{search_phrase}'.")
    sys.exit(1)

# Define the log dictionary to store the issues found in each repository
log = {}
for url in repository_urls:
    repo_name = url.split("/")[-1].replace(".git", "")
    log[repo_name] = {"url": url, "issues_found": 0, "uuid": str(uuid.uuid4())}

# Loop through the repository URLs and run gitleaks detect -v on each repository
for url in tqdm(repository_urls, desc="Scanning repositories"):
    print(f"Scanning repository: {url}")
    try:
        # Clone the repository
        repo_name = url.split("/")[-1].replace(".git", "")
        subprocess.check_output(["git", "clone", url, repo_name])

        # Run gitleaks detect -v on the cloned repository
        output_folder_for_repo = os.path.join(output_folder, repo_name + "_" + log[repo_name]["uuid"])
        os.mkdir(output_folder_for_repo)
        report_file = os.path.join(
            os.path.abspath(output_folder_for_repo), f"{repo_name}.json"
        )
        subprocess.check_output(
            ["gitleaks", "detect", "-v", "-r", report_file],
            stderr=subprocess.STDOUT,
            cwd=repo_name,
        )
    except subprocess.CalledProcessError as e:
        print(e.output.decode())
    finally:

        # Count the number of issues found in the report and store it in the log
        with open(report_file, "r") as f:
            report = json.load(f)
        issues_found = len(report)

        log[repo_name] = {"url": url, "issues_found": issues_found}
        print(f"Issues found: {issues_found}")
        # Delete the cloned repository
        shutil.rmtree(repo_name)

# Write the log and summary to a file
with open(os.path.join(output_folder, "report.md"), "w") as f:
    # Write the header of the report file
    f.write(f"# GitLeaks Scan Report\n\n")
    f.write("| Parameter | Value |\n")
    f.write("| --- | --- |\n")
    f.write(f"| Search Phrase | {search_phrase} |\n")
    f.write(f"| Return Count | {return_count} |\n")
    f.write(f"| Offset | {offset} |\n")
    f.write(f"| Total Repositories Searched | {len(repository_urls)} |\n")
    f.write(f"| Timestamp | {int(time.time())} |\n\n")

    # Write the log table to the report file
    f.write("| Repository Name | URL | Issues Found | JSON File |\n")
    f.write("| --- | --- | --- | --- |\n")
    total_issues = 0
    for repo_name, repo_log in log.items():
        print(f"Checking log for {repo_name}: {repo_log}")
        total_issues += repo_log["issues_found"]
        json_link = f"[{repo_name}.json]({os.path.join(output_folder, repo_name + '_' + log[repo_name]['uuid'], repo_name + '.json')})"
        f.write(f"| {repo_name} | [{repo_log['url']}]({repo_log['url']}) | {repo_log['issues_found']} | {json_link} |\n")

    # Write the summary to the report file
    f.write("\n\n")
    f.write(f"Total issues found: {total_issues}\n")
    f.flush()