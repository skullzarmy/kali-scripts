import openai
import sys
import os

# Enter your OpenAI API key here
openai.api_key = "YOUR_API_KEY"

# Function to test an API key and return it if it's valid
def test_api_key(api_key):
    openai.api_key = api_key
    try:
        openai.Completion.create(engine="davinci", prompt="Hello, world!")
        return api_key
    except:
        return None

# Get the input file name from the command line argument
if len(sys.argv) != 2:
    print("Usage: python test_api_keys.py <input_file>")
    sys.exit()
input_file = sys.argv[1]

# Open the input file for reading
with open(input_file, "r") as f:
    # Create the output file name
    output_file = os.path.splitext(input_file)[0] + "_tested.txt"
    # Open the output file for writing
    with open(output_file, "w") as out_f:
        # Loop through each line in the input file
        for line in f:
            # Remove any whitespace from the beginning and end of the line
            api_key = line.strip()
            # Test the API key
            valid_key = test_api_key(api_key)
            # If the API key is valid, write it to the output file
            if valid_key:
                out_f.write(valid_key + "\n")
