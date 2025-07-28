'''import fitz

File_path = "C:\\Users\\Yanshu\\Documents\\PEA305 workbook pdf_250118_234745.pdf"

pdf = fitz.open(File_path)
print(pdf.metadata)
print(pdf.get_toc())
print(pdf.page_count)

print(pdf.load_page(20).get_text())
# -------------saving page in png format-----------------
page = pdf.load_page(20)
pix = page.get_pixmap()
pix.save(f"pdf-{page.number}.png")

for i in range(pdf.page_count):
    page = pdf.load_page(i)
    link = page.get_links()
    print(link)

#Entire book as text starting from 0 to last page
#get all the text as list
# from sys import ps1
def get_book_content(pdf_file):
    num_page= pdf_file.page_count
    book_content = []
    for i in range(0, num_page):
        page = pdf_file.load_page(i)
        page_text = page.get_text()
        raw_text = page_text.replace("\t", " ")
        book_content.append(raw_text)
        
    return book_content
    
book = get_book_content(pdf)
print(book[55])
# print(len(book))   # Check how many pages were extracted'''


import fitz  # PyMuPDF
import os
from json_writer import save_outline_json  # assumes json_writer.py exists with save_outline_json


def is_heading_text(text, size, flags, min_font_size):
    if len(text) < 5 or len(text) > 100:
        return False
    if '.' in text and len(text) > 25:
        return False
    is_bold = (flags & 2) != 0
    is_all_caps = text.strip() == text.strip().upper()
    if size < min_font_size:
        return False
    if is_bold or is_all_caps or size >= min_font_size + 1.5:
        return True
    return False


def extract_headings_from_pdf(pdf_path):
    pdf = fitz.open(pdf_path)

    spans_info = []
    font_sizes = set()
    for page_num in range(pdf.page_count):
        page = pdf.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        size = span["size"]
                        flags = span.get("flags", 0)
                        spans_info.append({
                            "text": text,
                            "page": page_num + 1,
                            "size": size,
                            "flags": flags
                        })
                        font_sizes.add(size)

    if not spans_info:
        return None

    sorted_sizes = sorted(font_sizes, reverse=True)
    level_map = {}
    if len(sorted_sizes) > 0:
        level_map[sorted_sizes[0]] = "H1"
    if len(sorted_sizes) > 1:
        level_map[sorted_sizes[1]] = "H2"
    if len(sorted_sizes) > 2:
        level_map[sorted_sizes[2]] = "H3"

    first_page_spans = [s for s in spans_info if s["page"] == 1]
    if first_page_spans:
        max_size = max(s["size"] for s in first_page_spans)
        title_parts = [s["text"] for s in first_page_spans if s["size"] == max_size]
        title = " ".join(title_parts)
    else:
        title = "Unknown Title"

    min_heading_size = sorted_sizes[-1] if sorted_sizes else 0

    outline = []
    used_texts = set()

    for span in spans_info:
        size = span["size"]
        flags = span["flags"]
        text = span["text"].strip()
        if size in level_map:
            if text not in used_texts and len(text) > 2:
                if is_heading_text(text, size, flags, min_heading_size):
                    outline.append({
                        "level": level_map[size],
                        "text": text,
                        "page": span["page"]
                    })
                    used_texts.add(text)

    level_order = {"H1": 1, "H2": 2, "H3": 3}
    outline = sorted(outline, key=lambda x: (x["page"], level_order.get(x["level"], 99)))

    return {
        "title": title.strip(),
        "outline": outline
    }


def process_all_pdfs(input_dir="Round 1A/input", output_dir="Round 1A/output"):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            print(f"Processing: {pdf_path}")
            try:
                out_data = extract_headings_from_pdf(pdf_path)
                if not out_data:
                    print(f"No text extracted from {filename}")
                    continue
                output_filename = os.path.splitext(filename)[0] + ".json"
                save_outline_json(output_dir, output_filename, out_data)
                print(f" Saved outline JSON: {output_filename}")
            except Exception as e:
                print(f" Error processing {filename}: {e}")


if __name__ == "__main__":
    process_all_pdfs()
