import os
import json
import fitz  # PyMuPDF
from datetime import datetime

# ----------- CONFIGURATION -----------
INPUT_JSON_PATH = "input/input.json"
PDF_FOLDER = "input/pdfs"
OUTPUT_JSON_PATH = "output/output.json"

# ------------- HELPERS ---------------
def extract_text_snippets(pdf_path, max_pages=3):
    """
    Extracts section titles and sub-snippets from a given PDF.
    Returns: list of {"page_number", "section_title", "refined_text"}
    """
    doc = fitz.open(pdf_path)
    sections = []
    for page_number in range(min(len(doc), max_pages)):
        page = doc[page_number]
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if block['type'] == 0:  # Text block
                lines = block.get("lines", [])
                for line in lines:
                    line_text = " ".join(span['text'].strip() for span in line['spans']).strip()
                    if 10 <= len(line_text) <= 120 and not line_text.endswith(":"):
                        sections.append({
                            "page_number": page_number + 1,
                            "section_title": line_text,
                            "refined_text": line_text  # For simplicity, same text
                        })
    return sections


def rank_sections(sections, job_keywords):
    ranked = []
    seen_titles = set()
    for sec in sections:
        score = sum(1 for kw in job_keywords if kw.lower() in sec["section_title"].lower())
        if sec["section_title"] not in seen_titles:
            ranked.append((score, sec))
            seen_titles.add(sec["section_title"])
    ranked.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in ranked if item[0] > 0][:5]


# ------------ MAIN PIPELINE -----------
def process_documents():
    with open(INPUT_JSON_PATH, 'r') as f:
        input_data = json.load(f)

    documents = input_data["documents"]
    persona = input_data["persona"]["role"]
    job = input_data["job_to_be_done"]["task"]
    job_keywords = job.lower().split()

    all_sections = []

    for doc in documents:
        file_path = os.path.join(PDF_FOLDER, doc["filename"])
        print(f"Extracting from {file_path}...")
        try:
            sec = extract_text_snippets(file_path)
            for s in sec:
                s["document"] = doc["filename"]
                all_sections.append(s)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    ranked_sections = rank_sections(all_sections, job_keywords)

    extracted_sections = []
    subsection_analysis = []

    for i, sec in enumerate(ranked_sections):
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": i + 1,
            "page_number": sec["page_number"]
        })
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": sec["refined_text"],
            "page_number": sec["page_number"]
        })

    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": str(datetime.now())
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, 'w') as f:
        json.dump(output, f, indent=4)
    print("✅ output/output.json generated.")


if __name__ == "__main__":
    process_documents()
