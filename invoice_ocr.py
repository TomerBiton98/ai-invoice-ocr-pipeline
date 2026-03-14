import sys
import numpy as np
from fpdf import FPDF
from ocr_utils import load_images, run_easyocr, apply_corrections
from invoice_parser import parse_invoice


def save_pdf(json_data, output_path="invoice_output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "OCR Invoice Output", new_x="LMARGIN", new_y="NEXT")

    for k, v in json_data.items():
        pdf.cell(0, 8, f"{k}: {v}", new_x="LMARGIN", new_y="NEXT")

    pdf.output(output_path)
    print(f"\nPDF saved as: {output_path}")


def run(path):
    print("\n=== Loading images (PNG/JPG/PDF) ===")
    images = load_images(path)
    if not images:
        print("Error: No images extracted.")
        return

    print("\n=== Running EasyOCR ===")
    all_text = run_easyocr(images)

    print("\n=== RAW OCR ===")
    for t in all_text:
        print(t)

    print("\n=== APPLYING CORRECTIONS ===")
    clean = apply_corrections(all_text)
    for c in clean:
        print(c)

    print("\n=== CLEAN JSON OUTPUT ===")
    json_data = parse_invoice(clean)
    print(json_data)

    save_pdf(json_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python invoice_ocr.py <image_or_pdf>")
        sys.exit(1)
    run(sys.argv[1])
