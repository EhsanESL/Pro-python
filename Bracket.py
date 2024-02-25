import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import os
import sys
import logging
import re


# Download NLTK data if not already installed
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Input CSV file name
filename_with_identifier = sys.argv[1]
filename_without_extension = os.path.splitext(filename_with_identifier)[0]
file_path = os.path.join(filename_with_identifier)
 

with open(file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

input_file = os.path.join(filename_with_identifier) 
output_file = os.path.join(filename_without_extension +'SubBubbles'+'.csv')


# List to store cells with parentheses
cell_with_parentheses = []

with open(input_file, 'r', newline='') as csv_input:
    reader = csv.reader(csv_input)

    for row in reader:
        for cell in row:
            # Check if the cell contains parentheses
            if '(' in cell or ')' in cell:
                cell_with_parentheses.append(cell)

# Write cells with parentheses to the output CSV file
with open(output_file, 'w', newline='') as csv_output:
    writer = csv.writer(csv_output)
    writer.writerow(['Cell with Parentheses'])  # Header
    writer.writerows([[cell] for cell in cell_with_parentheses])

print(f"Cells with parentheses have been saved to '{output_file}'")


# List to store words between parentheses
parentheses_words = []

# Regular expression pattern to find words between parentheses
pattern = r'\(([^)]*)\)'  # Match everything between '(' and ')'

with open(input_file, 'r', newline='') as csv_input:
    reader = csv.reader(csv_input)

    for row in reader:
        for cell in row:
            # Find all words between parentheses in the cell and store them
            matches = re.findall(pattern, cell)
            parentheses_words.extend(matches)

# Write words between parentheses to the output CSV file
with open(output_file, 'w', newline='') as csv_output:
    writer = csv.writer(csv_output)
    writer.writerow(['Words Between Parentheses'])  # Header
    writer.writerows([[word] for word in parentheses_words])

print(f"Words between parentheses have been saved to '{output_file}'")
