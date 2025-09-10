def normalize_text(text):
    # Normalize the text by converting to lowercase and stripping whitespace
    return text.lower().strip()

def calculate_relevance(query, document):
    # A simple relevance scoring function based on keyword matching
    query_terms = set(normalize_text(query).split())
    document_terms = set(normalize_text(document.content).split())
    return len(query_terms.intersection(document_terms)) / len(query_terms) if query_terms else 0