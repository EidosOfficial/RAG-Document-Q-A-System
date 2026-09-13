from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        keep_separator=True,
        is_separator_regex=False,
        chunk_size=500,
        chunk_overlap=50,
    )
    return text_splitter.split_documents(docs)
