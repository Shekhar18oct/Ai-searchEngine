import unittest
from src.engine.searcher import Searcher
from src.engine.indexer import Indexer
from src.models.document import Document

class TestSearcher(unittest.TestCase):

    def setUp(self):
        self.indexer = Indexer()
        self.searcher = Searcher(self.indexer)

        # Sample documents
        doc1 = Document(title="First Document", content="This is the content of the first document.")
        doc2 = Document(title="Second Document", content="This document is about something else.")
        
        # Indexing documents
        self.indexer.index_document(doc1)
        self.indexer.index_document(doc2)

    def test_search(self):
        results = self.searcher.search("first")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "First Document")

    def test_get_results(self):
        self.searcher.search("document")
        results = self.searcher.get_results()
        self.assertEqual(len(results), 2)

if __name__ == '__main__':
    unittest.main()