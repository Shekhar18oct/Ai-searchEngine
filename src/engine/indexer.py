import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class Indexer:
    def __init__(self):
        self.documents = []
        self.vectorizer = TfidfVectorizer()
        self.document_vectors = None
        
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('punkt_tab')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')  # Open Multilingual Wordnet
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        # Basic tokenization (split on whitespace)
        tokens = text.split()
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) 
                 for token in tokens 
                 if token.isalnum() and token not in self.stop_words]
        return ' '.join(tokens)

    def index_document(self, document):
        self.documents.append(document)
        # Update document vectors
        self._update_vectors()

    def _update_vectors(self):
        # Extract preprocessed content from documents
        processed_contents = [self.preprocess_text(doc.content) for doc in self.documents]
        # Create TF-IDF vectors
        self.document_vectors = self.vectorizer.fit_transform(processed_contents)

    def get_similar_documents(self, query, top_k=5):
        # Preprocess query
        processed_query = self.preprocess_text(query)
        # Transform query to vector
        query_vector = self.vectorizer.transform([processed_query])
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        # Get top k similar documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'document': self.documents[idx],
                'similarity': float(similarities[idx])
            })
        return results

    def get_index(self):
        return self.documents