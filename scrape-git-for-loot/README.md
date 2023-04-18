# WTF?!?

I was noticing a lot of people leaking their OpenAI keys in public repos and was trying to make a tool to compile a list of still valid keys to warn the repo owners. Upon actual use it turned out none of them were still valid so I guess my services were not as needed as I thought...

Leaving it here as a reference mostly.

# Explanation

## Step 1: `git-scraper.py {search phrase} {return_count} {offset}`

The `git-scraper.py` file performs the magic. It will perform the user defined search, loop through the returned repos, download each one locally, scan with GitLeaks, store the scan results, delete the repo, and continue looping. It will handle garbage-collection.

### Output

Script will create a `/{repo-name}-{curr-date}/` folder at the root of your working directory (where you called it)
Results stored to `/{repo-name}-{curr-date}/scraped.txt`

### Mandatory Params

-   `search_term` (string) Defines the search term to perform on GitHub API.

### Optional params

-   `return_count` (int) [default: 100]
-   `offset` (int) [default: 0]

### Example

```bash
python git-scraper.py "openai" 50 50
```

-   Would search GitHub for all repos containing the keyword 'openai', skip 50 and loop through the next 50.

## STEP 2: `post-process.py {path_to_recurse}`

### Mandatory Params

-   `source_path` (string) Path to recursively loop, checking and ingesting scraped.txt files.

### Output

Saves a new `scraped.txt` at the working directory (should not invoke inside one of the created folders from previous step or you will append to the existing file) - Loops through all scraped.txt reports matching an OpenAI key format (starts with sk-) and if found logs it in the new output file in a new line.

## Step 3: `dedupe.py scraped.txt`

Running `dedupe.py` will remove duplicate keys, as we don't want to add any unneeded calls to the key when we check validity.

### Output

Creates a `scraped_cleaned.txt` at the working directory.

## Step 4: `openai-key-tester.py scraped_cleaned.txt`

Loops through each line and tests it as an OpenAI key via a very cheap davinci prompt. If it gets a working response it logs it in a new output file.

### Output

Creates two new files.

`scraped_cleaned_tested.txt` which contains any working API keys

`scraped_cleaned_failed_tests.log` which contians a JSON response log of each failing API call.
