import cv2
import pytesseract
import numpy as np
import os

def extract_text_from_image(image_path):
    """
    Extracts high-quality text from an image using enhanced Tesseract OCR preprocessing.
    Works well for scanned documents or poor-quality text images.
    """
    try:
        # Step 1: Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"[OCR] Image not found or unreadable: {image_path}")

        # Step 2: Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Step 3: Denoising using bilateral filter
        gray = cv2.bilateralFilter(gray, 9, 75, 75)

        # Optional: Improve contrast using histogram equalization
        gray = cv2.equalizeHist(gray)

        # Step 4: Adaptive thresholding for uneven lighting
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 2
        )

        # Step 5: Morphological operations to enhance features
        kernel = np.ones((1, 1), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Step 6: Resize for small images to improve OCR
        height, width = thresh.shape
        if height < 1000 or width < 1000:
            thresh = cv2.resize(thresh, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

        # Step 7: OCR with Tesseract
        custom_config = r'--oem 3 --psm 6 -l eng'
        extracted_text = pytesseract.image_to_string(thresh, config=custom_config)

        print("[OCR DEBUG] Text Preview:\n", extracted_text[:500])
        return extracted_text.strip()

    except Exception as e:
        print(f"[ERROR in extract_text_from_image] {e}")
        return ""
