import openai
import sys
import os
from tqdm import tqdm

# Function to test an API key and return it if it's valid
def test_api_key(api_key):
    openai.api_key = api_key
    try:
        openai.Completion.create(engine="davinci", prompt="Hello, world!")
        return api_key, None
    except Exception as e:
        return api_key, str(e)

# Get the input file name from the command line argument
if len(sys.argv) != 2:
    print("Usage: python openai-key-tester.py <input_file>")
    sys.exit()
input_file = sys.argv[1]

# Open the input file for reading
with open(input_file, "r") as f:
    # Create the output file name
    output_file = os.path.splitext(input_file)[0] + "_tested.txt"
    # Create the error log file name
    error_file = os.path.splitext(input_file)[0] + "_failed_tests.log"
    # Open the output file for writing
    with open(output_file, "w") as out_f, open(error_file, "w") as error_f:
        # Loop through each line in the input file
        for line in tqdm(f):
            # Remove any whitespace from the beginning and end of the line
            api_key = line.strip()
            # Test the API key
            valid_key, error = test_api_key(api_key)
            # If the API key is valid, write it to the output file
            if not error:
                out_f.write(valid_key + "\n")
            # If there was an error, write it to the error log file
            else:
                error_f.write(valid_key + "\t" + error + "\n")
