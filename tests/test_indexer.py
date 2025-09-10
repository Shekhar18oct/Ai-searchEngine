import unittest
from src.engine.indexer import Indexer
from src.models.document import Document

class TestIndexer(unittest.TestCase):

    def setUp(self):
        self.indexer = Indexer()

    def test_index_document(self):
        doc = Document(title="Test Document", content="This is a test.")
        self.indexer.index_document(doc)
        self.assertIn(doc, self.indexer.get_index())

    def test_get_index(self):
        self.assertEqual(self.indexer.get_index(), [])

        doc1 = Document(title="Doc 1", content="Content 1")
        doc2 = Document(title="Doc 2", content="Content 2")
        self.indexer.index_document(doc1)
        self.indexer.index_document(doc2)

        indexed_docs = self.indexer.get_index()
        self.assertEqual(len(indexed_docs), 2)
        self.assertIn(doc1, indexed_docs)
        self.assertIn(doc2, indexed_docs)

if __name__ == '__main__':
    unittest.main()