# 📄 Adobe India Hackathon 2025 – Round 1A & 1B Submission

This repository contains my solutions for the **Adobe India Hackathon 2025** challenges:
- **Round 1A**: Offline Structured Outline Extraction from PDFs
- **Round 1B**: Persona-Driven Document Intelligence

---

##  Problem Statements

### 🔹 Round 1A – PDF Outline Extraction
Build a lightweight, fast offline solution to extract structured outlines (Title, H1, H2, H3) from raw PDFs without using any cloud APIs.

### 🔹 Round 1B – Persona-Driven Document Intelligence
Extract and prioritize the most relevant sections from a set of documents based on a given **persona** and **job-to-be-done**, generating a clean JSON output.

---

## 🧠 Key Features

### ✅ Round 1A
- Extracts document structure including Title, H1, H2, H3
- Uses `PyMuPDF` to detect font sizes, boldness, and heading patterns
- Lightweight and fast (Tested with multiple PDFs)
- Integrated optional **language detection** using `langdetect`
- Dockerized for reproducible results

### ✅ Round 1B
- Extracts relevant sections/subsections based on job keywords
- Ranking logic to prioritize top sections
- Cleanly structured input and output JSON
- Runs fully offline in < 60 seconds for 5+ documents
- Compliant with model size (<1GB) and no-internet constraints

---

## 📁 Folder Structure

├── Round 1A/
│ ├── extraction.py
│ ├── json_writer.py
│ ├── test_time.py
│ ├── Dockerfile
│ └── input/ + output/
│
├── Round 1B/
│ ├── extraction.py
│ ├── input/
│ │ ├── input.json
│ │ └── pdfs/
│ ├── output/
│ ├── Dockerfile
│ ├── requirements.txt
│ └── approach_explanation.md




---

## ⚙️ Tech Stack

- Python 3
- PyMuPDF
- Docker
- JSON I/O
- (Optional) LangDetect
- (Optional) Scikit-learn / Numpy (not used to stay under 1GB limit)

---

## 🧪 Sample Outputs

| PDF Name | Extracted Headings (Round 1A) |
|----------|-------------------------------|
| file02.pdf | `Title`, `H1`, `H2`, `H3` as shown in output JSON |
| Learn Acrobat - Fill and Sign.pdf | Ranked section titles and detailed snippets (Round 1B) |

---

## 📝 How to Run

```bash
# Round 1A
cd Round\ 1A
docker build -t pdfoutline .
docker run --rm -v "$PWD/input:/app/input" -v "$PWD/output:/app/output" --network none pdfoutline

# Round 1B
cd ../Round\ 1B
docker build -t round1b_pdf_extractor .
docker run --rm -v "$PWD/input:/app/input" -v "$PWD/output:/app/output" --network none round1b_pdf_extractor
