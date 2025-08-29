from transformers import pipeline

# Load summarization model
try:
    summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
    print("[INFO] Summarization model loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load summarization model: {e}")
    summarizer_pipeline = None

def generate_summary(text, max_length=130, min_length=30):
    """
    Generates a summary of the input text using a pre-trained HuggingFace summarizer.

    Args:
        text (str): Raw extracted text to summarize.
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.

    Returns:
        str: The summarized text.
    """
    if not summarizer_pipeline:
        return "[ERROR] Summarization model not loaded."

    try:
        # Limit input to about 800 words to avoid model token overflow
        words = text.split()
        if len(words) > 800:
            text = " ".join(words[:800])

        input_len = len(text.split())
        adjusted_max_len = min(max_length, int(input_len * 0.8))
        summary = summarizer_pipeline(text, max_length=adjusted_max_len, min_length=min_length, do_sample=False)

        return summary[0]['summary_text'].strip()

    except Exception as e:
        print(f"[ERROR in summarizer] {e}")
        return "[ERROR] Failed to generate summary."



if __name__ == "__main__":
    # Example usage
    sample_text = """Artificial Intelligence is transforming the world at an unprecedented pace. From self-driving cars to automated medical diagnostics, AI is being integrated into almost every field. However, concerns around bias, transparency, and ethics remain critical challenges. Governments and organizations are actively developing frameworks to regulate AI deployment while maximizing its potential benefits."""
    summary = generate_summary(sample_text)
    print("[SUMMARY] ", summary)