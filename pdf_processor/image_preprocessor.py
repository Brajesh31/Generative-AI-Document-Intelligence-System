import cv2
import numpy as np
import os

def enhance_image(image_path):
    """
    Enhances a document image to improve OCR accuracy.

    Steps:
    - Convert to grayscale
    - Denoise
    - Thresholding
    - Deskew (optional)

    Args:
        image_path (str): Path to the input image

    Returns:
        str: Path to the enhanced image (temp file)
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot read image at {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Deskew image
    deskewed = deskew(thresh)

    # Save temporary enhanced image
    enhanced_path = os.path.join("uploads", "enhanced_temp.png")
    cv2.imwrite(enhanced_path, deskewed)

    return enhanced_path


def deskew(image):
    """
    Rotates image to correct skew using contours and minAreaRect.

    Args:
        image (np.ndarray): Grayscale or binary image

    Returns:
        np.ndarray: Deskewed image
    """
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated