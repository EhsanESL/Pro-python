import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from pptx import Presentation
from pptx.util import Inches
import pydot
import os
import sys
import logging
from pptx.enum.text import PP_ALIGN

# Configure logging
logging.basicConfig(filename='separate_verbs.log', level=logging.INFO)

# Download NLTK data if not already installed
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

filename_with_identifier = sys.argv[1]
filename_without_extension = os.path.splitext(filename_with_identifier)[0]
file_path = os.path.join(filename_with_identifier)

try:
    # Read the CSV file and extract verbs
    verbs_data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)
        for row in rows:
            for cell in row:
                # Split the cell content into individual words
                words = word_tokenize(cell)
                # Part-of-speech tagging
                tagged_words = pos_tag(words)
                # Extract verbs
                verbs = [word for word, tag in tagged_words if tag.startswith('VB')]
                verbs_data.extend(verbs)

    # Write verbs to a temporary CSV file
    temp_csv_filename = filename_without_extension + '_verbs.csv'
    with open(temp_csv_filename, 'w', newline='') as temp_csv_file:
        writer = csv.writer(temp_csv_file)
        writer.writerow(['Verb'])  # Header
        writer.writerows([[verb] for verb in verbs_data])
    
    # Create a PowerPoint presentation
    prs = Presentation()
    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)

    # Calculate the positions to fit all verbs within the slide
    max_verbs_per_row = 5
    num_verbs = len(verbs_data)
    num_rows = (num_verbs + max_verbs_per_row - 1) // max_verbs_per_row
    node_width = Inches(1.5)
    node_height = Inches(0.5)
    left_margin = Inches(0.5)
    top_margin = Inches(1)

    # Create shapes in PowerPoint
    left = left_margin
    top = top_margin
    for verb in verbs_data:
        if left + node_width > Inches(10):
            left = left_margin
            top += node_height
        textbox = slide.shapes.add_textbox(left, top, node_width, node_height)
        textbox.text_frame.text = verb
        textbox.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER  # Center align text
        left += node_width
    
    # Save the PowerPoint presentation
    output_pptx_file = filename_without_extension + '_verbs.pptx'
    prs.save(output_pptx_file)
    print(f"PPTX file with verbs has been created: '{output_pptx_file}'")
    
except Exception as e:
    # Log any exceptions that occur
    logging.error(f'An error occurred: {str(e)}')
