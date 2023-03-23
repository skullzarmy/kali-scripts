import sys

if len(sys.argv) < 2:
    print("Usage: python dedupe.py <file_path> : Removes all duplicate lines in text file and saves as a new file at [filename]_cleaned.txt")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = input_filename.replace(".txt", "_cleaned.txt")

seen_lines = set()
with open(input_filename, "r") as f_in, open(output_filename, "w") as f_out:
    for line in f_in:
        line = line.strip()
        if line not in seen_lines:
            f_out.write(line + "\n")
            seen_lines.add(line)

print(f"Cleaned file written to {output_filename}.")
