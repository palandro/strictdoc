from strictdoc.backend.sdoc.reader import SDReader
from strictdoc.core.document_iterator import DocumentCachingIterator

DOC_FILE = "docs/strictdoc.sdoc"


class SDocInMemoryDatabase:
    document = SDReader().read_from_file(DOC_FILE)

    @staticmethod
    def iterate_nodes():
        iterator = DocumentCachingIterator(SDocInMemoryDatabase.document)
        for node in iterator.all_content():
            yield node

