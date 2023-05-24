import argparse
import os

# Define command-line argument parser
parser = argparse.ArgumentParser(description='Parse lines of a file')
parser.add_argument('file_path', type=str, help='Path to file to be parsed')

# Parse command-line arguments
args = parser.parse_args()

# Get the filename and directory path from the input file path
dir_path, filename = os.path.split(args.file_path)

# Construct the output file path by appending '-parsed' to the filename
output_path = os.path.join(dir_path, f"{filename}-parsed")

# Open the input and output files
with open(args.file_path, 'r') as infile, open(output_path, 'w') as outfile:
    # Loop over the lines in the input file
    for line in infile:
        parsed_line = line.strip()  # Strip line

        # Target the right lines
        if (parsed_line.startswith("<circle")):
            # Hardcoded parse to remove "color = black/>" from the end of the line
            parsed_line = parsed_line[:len(parsed_line) - 17] + "/>"

        # Write the parsed line to the output file
        outfile.write(parsed_line + '\n')
