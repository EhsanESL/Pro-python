import csv
import nltk
import os
import sys
import logging
import re
import subprocess

# Create a new logger instance for bracket.py
logger = logging.getLogger('bracket_logger')
logger.setLevel(logging.INFO)

# Create a file handler to output logs to a file
file_handler = logging.FileHandler('bracket.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Download NLTK data if not already installed
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

try:
    # Input CSV file name
    filename_with_identifier = sys.argv[1]
    filename_without_extension = os.path.splitext(filename_with_identifier)[0]
    file_path = os.path.join(filename_with_identifier)

    output_file = os.path.join(filename_without_extension + '_subbubbles'+'.pptx')
   
    # List to store cells with parentheses
    cell_with_parentheses = []

    with open(file_path, 'r', newline='') as csv_input:
        reader = csv.reader(csv_input)

        for row in reader:
            for cell in row:
                # Check if the cell contains parentheses
                if '(' in cell or ')' in cell:
                    cell_with_parentheses.append(cell)

    # Write cells with parentheses to the output CSV file
    #with open(output_file, 'w', newline='') as csv_output:
        #writer = csv.writer(csv_output)
        #writer.writerow(['Cell with Parentheses'])  # Header
        #writer.writerows([[cell] for cell in cell_with_parentheses])

    #logger.info(f"Cells with parentheses have been saved to '{output_file}'")

    # List to store words between parentheses
    parentheses_words = []

    # Regular expression pattern to find words between parentheses
    pattern = r'\(([^)]*)\)'  # Match everything between '(' and ')'

    with open(file_path, 'r', newline='') as csv_input:
        reader = csv.reader(csv_input)

        for row in reader:
            for cell in row:
                # Find all words between parentheses in the cell and store them
                matches = re.findall(pattern, cell)
                parentheses_words.extend(matches)

    # Write words between parentheses to the output CSV file
    with open(output_file, 'a', newline='') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerow(['Words Between Parentheses'])  # Header
        writer.writerows([[word] for word in parentheses_words])

    logger.info(f"Words between parentheses have been saved to '{output_file}'")

    # Call the Bracket-Sketch-unique.py script with the output of this script as its input
    subprocess.run(['python', 'Bracket-Sketch-unique.py', output_file])

except Exception as e:
    logger.error(f'An error occurred: {str(e)}')
