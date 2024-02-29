import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import os
import sys
import logging
import re

# Create a new logger instance for Seperate_verbs.py
logger = logging.getLogger('bracket_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO

# Create a file handler to output logs to a file
file_handler = logging.FileHandler('bracket.log')
file_handler.setLevel(logging.INFO)  # Set the log level for the handler to INFO

# Define a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)  # Attach the formatter to the handler

# Add the file handler to the logger
logger.addHandler(file_handler)

# Download NLTK data if not already installed
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

try:
    logger.info("start try")
    # Input CSV file name
    filename_with_identifier = sys.argv[1]
    filename_without_extension = os.path.splitext(filename_with_identifier)[0]
    file_path = os.path.join(filename_with_identifier)
    logger.info("Bracket.py :Input CSV file name.")
    logger.info(f"filename_with_identifier: {filename_with_identifier}")
    logger.info(f"filename_without_extension: {filename_without_extension}")
    logger.info(f"file_path: {file_path}")

 
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)

    input_file = file_path
    output_file = os.path.join(filename_without_extension +'SubBubbles'+'.csv')
    logger.info(f"output_file {output_file}")

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
    logger.info("start to write cells with parentheses to the output CSV file")
    with open(output_file, 'w', newline='') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerow(['Cell with Parentheses'])  # Header
        writer.writerows([[cell] for cell in cell_with_parentheses])

    logger.info(f"Cells with parentheses have been saved to '{output_file}'")

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
    logger.info("start to write words between parentheses to the output CSV file")
    with open(output_file, 'w', newline='') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerow(['Words Between Parentheses'])  # Header
        writer.writerows([[word] for word in parentheses_words])

    logger.info(f"Words between parentheses have been saved to '{output_file}'")

except Exception as e:
    # Log any exceptions that occur
    logger.error(f'An error occurred: {str(e)}')
