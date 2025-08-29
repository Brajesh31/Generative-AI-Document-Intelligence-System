import os
import re

def clean_text(text):
    """
    Cleans the extracted OCR text by removing unwanted characters,
    extra spaces, and non-printable symbols.

    Args:
        text (str): Raw text from OCR

    Returns:
        str: Cleaned text
    """
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable())
    
    # Replace multiple spaces/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Optional: Remove special symbols
    text = re.sub(r'[^\w\s.,;:!?()/-]', '', text)

    return text.strip()


def save_text_to_file(text, filepath):
    """
    Saves the given text to a specified file.

    Args:
        text (str): Text to save
        filepath (str): Path to output file
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)


def chunk_text(text, max_words=500):
    """
    Breaks long text into smaller chunks for processing by models with input limits.

    Args:
        text (str): Long input text
        max_words (int): Max words per chunk

    Returns:
        list[str]: List of text chunks
    """
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

