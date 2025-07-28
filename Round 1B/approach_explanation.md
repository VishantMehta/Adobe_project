# Approach Explanation – Round 1B: Persona-Driven Document Intelligence

## Overview

This project is focused on building a simple and efficient document processing system that can understand the needs of a specific persona and extract useful information from a set of PDF files. For this round, the goal was to take a collection of documents and identify the most relevant sections based on what the user (persona) is trying to achieve.

## My Approach

I started by reading the `input.json` file which contains three main things:
- A list of PDF documents
- A persona (for example, HR professional)
- A job to be done (like creating fillable forms)

Once this data was loaded, I extracted keywords from the task description. These keywords were used to search through the PDFs using PyMuPDF. For each PDF, the script scans all the pages and checks each line of text to see if it contains any of the keywords from the task.

If a match is found, that line is considered a relevant section. I also tracked which page it came from and which document it was in. To keep things clean, I avoided duplicate results and removed irrelevant lines that were too short or too long.

From all the matched results, I selected the top 5 based on how early they appeared and how well they matched the task. These are added to the final output along with a basic subsection analysis using the same matched lines (this can be improved in the future to include summaries).

## Why This Works

- It’s fast and lightweight — no machine learning models, just smart filtering and keyword matching.
- Everything runs offline and on CPU only.
- The Docker image stays small because it only uses PyMuPDF and Python.

## Output

The script generates a single `output.json` file containing:
- Metadata about the input
- A list of the top 5 matched sections
- A brief subsection for each match

## Possible Improvements

- Use TF-IDF or embeddings to improve section relevance
- Extract full paragraphs instead of single lines
- Add heading structure detection (like H1, H2, etc.)
- Better handling of synonyms or variations in phrasing

For now, this version does the job accurately within the constraints and is easy to test and run.

