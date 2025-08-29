from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Model name
model_name = "dslim/bert-base-NER"

# Try loading the model
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    print("[INFO] NER model loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load NER model: {e}")
    ner_pipeline = None

def split_text_into_chunks(text, max_length=400):
    """
    Splits long text into smaller chunks for processing by the NER pipeline.
    """
    sentences = text.split(".")
    chunks = []
    chunk = ""

    for sentence in sentences:
        if len(chunk) + len(sentence) < max_length:
            chunk += sentence.strip() + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sentence.strip() + ". "
    
    if chunk:
        chunks.append(chunk.strip())
    
    return chunks

def extract_named_entities(text, min_score=0.7):
    """
    Extracts named entities from the input text using the NER pipeline.
    
    Args:
        text (str): The input text.
        min_score (float): Minimum confidence score threshold to include an entity.
        
    Returns:
        list[dict]: A list of entities with word, type, and confidence.
    """
    if not ner_pipeline:
        return [{"error": "NER model not loaded"}]

    all_entities = []
    try:
        chunks = split_text_into_chunks(text)
        for chunk in chunks:
            entities = ner_pipeline(chunk)
            for ent in entities:
                if ent['score'] >= min_score:
                    all_entities.append({
                        "word": ent['word'],
                        "entity": ent['entity_group'],
                        "score": round(ent['score'], 2)
                    })
        return all_entities
    except Exception as e:
        print(f"[ERROR in NER] {e}")
        return []
