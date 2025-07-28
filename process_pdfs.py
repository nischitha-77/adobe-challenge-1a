import os
import json
from collections import defaultdict, Counter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar

def extract_font_key(line):
    for char in line:
        if isinstance(char, LTChar):
            return (char.fontname, round(char.size, 1))
    return None

def is_numbered(text):
    import re
    return bool(re.match(r"^\s*(\d+[\.\)]|[a-zA-Z]\)|[IVXLC]+\.)", text.strip()))

def is_all_caps(text):
    return text.isupper() and len(text) > 3

def is_title_case(text):
    return text.istitle() and len(text.split()) <= 10

def extract_headings_from_pdf(pdf_path):
    blocks = []
    font_counter = Counter()
    font_blocks = defaultdict(list)
    max_font_size = 0
    max_font_key = None

    for page_number, layout in enumerate(extract_pages(pdf_path)):
        for element in layout:
            if not isinstance(element, LTTextContainer):
                continue

            block_lines = []
            font_keys = []

            for text_line in element:
                if isinstance(text_line, LTTextLine):
                    text = text_line.get_text().strip()
                    if not text:
                        continue
                    font_key = extract_font_key(text_line)
                    if font_key:
                        font_keys.append(font_key)
                        font_blocks[font_key].append(text)
                        font_counter[font_key] += 1
                        if font_key[1] > max_font_size:
                            max_font_size = font_key[1]
                            max_font_key = font_key
                    block_lines.append(text)

            if block_lines:
                full_text = " ".join(block_lines)
                blocks.append({
                    "text": full_text,
                    "lines": len(block_lines),
                    "font_keys": font_keys,
                    "page": page_number + 1
                })

    most_common_font = font_counter.most_common(1)[0][0] if font_counter else None
    headings = []

    for block in blocks:
        text = block["text"]
        lines = block["lines"]
        page = block["page"]
        font_keys = block["font_keys"]

        if not text or len(text) < 3:
            continue

        if any(fk[1] == max_font_size for fk in font_keys):
            continue

        if lines > 2:
            continue

        if all(fk == most_common_font for fk in font_keys):
            if not is_numbered(text):
                continue

        if is_numbered(text) or is_all_caps(text) or is_title_case(text):
            headings.append({
                "level": "H1",
                "text": text,
                "page": page
            })

    return headings

def extract_title_from_pdf(pdf_path):
    font_sizes = defaultdict(list)

    for layout in extract_pages(pdf_path):
        for element in layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if isinstance(text_line, LTTextLine):
                        line_text = text_line.get_text().strip()
                        font_size = None
                        for char in text_line:
                            if isinstance(char, LTChar):
                                font_size = round(char.size, 2)
                                break
                        if font_size and line_text:
                            font_sizes[font_size].append((text_line.y0, line_text))

    if not font_sizes:
        return ""

    largest_font = max(font_sizes.keys())
    title_lines = font_sizes[largest_font]
    title_lines_sorted = sorted(title_lines, key=lambda x: -x[0])
    full_title = " ".join([text for _, text in title_lines_sorted]).strip()
    return full_title

def process_all_pdfs(input_dir="sample_dataset/pdfs", output_dir="sample_dataset/outputs"):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(input_dir, filename)
            title = extract_title_from_pdf(path)
            outline = extract_headings_from_pdf(path)

            output = {
                "title": title,
                "outline": outline
            }

            json_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"[✓] Processed {filename}")

if __name__ == "__main__":
    process_all_pdfs()
