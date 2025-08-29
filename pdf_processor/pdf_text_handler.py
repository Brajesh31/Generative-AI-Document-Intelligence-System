import fitz  # PyMuPDF
import os
from ai_engine.ocr_engine import extract_text_from_image


def extract_digital_text(pdf_path):
    """
    Extracts digital text from a PDF file using PyMuPDF.
    """
    try:
        text = ""
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text().strip() + "\n"
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"[ERROR in digital PDF extraction] {e}")
        return ""


def extract_text_from_pdf_images(pdf_path, temp_image_dir="temp_images"):
    """
    Converts each PDF page to image and performs OCR.
    """
    try:
        if not os.path.exists(temp_image_dir):
            os.makedirs(temp_image_dir)

        ocr_text = ""
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=300)  # High-res rendering
            image_path = os.path.join(temp_image_dir, f"page_{i + 1}.png")
            pix.save(image_path)

            # OCR on saved image
            text = extract_text_from_image(image_path)
            ocr_text += text + "\n"

        doc.close()
        return ocr_text.strip()
    except Exception as e:
        print(f"[ERROR in OCR image PDF extraction] {e}")
        return ""


def extract_all_text_from_pdf(pdf_path, min_text_length=100):
    """
    Combines digital + OCR text only if needed.
    """
    print("[INFO] Trying to extract digital text...")
    digital = extract_digital_text(pdf_path)

    # If digital text is meaningful, no need for OCR
    if len(digital.split()) > min_text_length:
        print("[INFO] Digital text is sufficient. Skipping OCR.")
        return digital.strip()

    # Otherwise, use OCR
    print("[WARNING] Digital text too short. Falling back to OCR...")
    ocr = extract_text_from_pdf_images(pdf_path)
    return ocr.strip()

