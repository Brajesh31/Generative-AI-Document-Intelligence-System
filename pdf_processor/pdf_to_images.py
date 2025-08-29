import os
from pdf2image import convert_from_path
import uuid

def convert_pdf_to_images(pdf_path, output_folder="uploads", dpi=300):
    """
    Converts a PDF file into a list of image file paths, one per page.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Folder where the images will be saved.
        dpi (int): Resolution (dots per inch) for image conversion.

    Returns:
        list[str]: Paths to the generated image files.
    """
    try:
        # Make sure output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Convert PDF to list of PIL images
        images = convert_from_path(pdf_path, dpi=dpi)

        image_paths = []
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        for i, img in enumerate(images):
            filename = f"{base_name}_page_{i+1}_{uuid.uuid4().hex[:6]}.png"
            full_path = os.path.join(output_folder, filename)
            img.save(full_path, "PNG")
            image_paths.append(full_path)

        return image_paths

    except Exception as e:
        print(f"[ERROR] PDF to image conversion failed: {e}")
        return []
