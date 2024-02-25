import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import os
import sys
import logging


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
output_file = os.path.join(filename_without_extension +'verbs'+'.csv')

# List to store verbs
verbs_data = []

def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

with open(input_file, 'r', newline='') as csv_input:
    reader = csv.reader(csv_input)

    for row in reader:
        for cell in row:
            # Split the cell content into individual words
            words = word_tokenize(cell)
            
            # Part-of-speech tagging
            tagged_words = pos_tag(words)
            
            # Extract verbs
            verbs = [word for word, tag in tagged_words if is_verb(tag)]
            verbs_data.extend(verbs)

# Write verbs to the output CSV file
with open(output_file, 'w', newline='') as csv_output:
    writer = csv.writer(csv_output)
    writer.writerow(['Verb'])  # Header
    writer.writerows([[verb] for verb in verbs_data])

print(f"Verbs have been saved to '{output_file}'")
