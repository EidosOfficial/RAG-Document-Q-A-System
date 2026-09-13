import os
import json
import uuid
import argparse
from langchain_core.documents import Document

from pypdf import PdfReader
from config import settings
from util import clear_json_file
from src.core.chunker import create_chunks
from src.db.session import clear_table, connect
from src.core.embedder import generate_embedding


def ingest_documents(force: int = 0):
    if force:
        print("[FORCE] Clearing the database...")
        clear_table()
        clear_json_file(settings.SCANNED_FILES_PATH)

    # We will be considering /documents as the default directory for storing our files for now
    docs_dir = settings.DOCUMENTS_DIRECTORY

    try:
        with open(settings.SCANNED_FILES_PATH, "r", encoding="utf-8") as file:
            scanned_files = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scanned_files = {}

    conn = connect()
    with os.scandir(docs_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name not in scanned_files:
                name, ext = os.path.splitext(entry.name)
                ext = ext.lower()
                print("-" * 50)
                print(f"[DBG] Processing file {name} | format {ext}")

                file_content = ""
                if ext in [".md", ".txt"]:
                    with open(entry.path, "r", encoding="utf-8") as file:
                        file_content = file.read()
                    print(f"[DBG] File read.")
                elif ext == ".pdf":
                    from pypdf import PdfReader

                    reader = PdfReader(entry.path)
                    number_of_pages = len(reader.pages)
                    print(f"[DBG] Reading file | Total pages: {number_of_pages}")
                    for i in range(number_of_pages):
                        page = reader.pages[i]
                        text_content = page.extract_text()
                        if text_content is not None:
                            file_content += text_content.replace("\x00", "")
                else:
                    print(f"[WARN] Skipping file | unsupported format {ext}")
                    continue

                docs = [
                    Document(page_content=file_content, metadata={"source": entry.path})
                ]

                chunks = create_chunks(docs)
                embeddings = generate_embedding(chunks)

                cur = conn.cursor()
                for i, chunk in enumerate(chunks):
                    cur.execute(
                        "INSERT INTO document_chunks (id, content, metadata, embedding) VALUES (%s, %s, %s, %s)",
                        (
                            uuid.uuid4(),
                            chunk.page_content,
                            json.dumps(chunk.metadata),
                            embeddings[i].tolist(),
                        ),
                    )
                conn.commit()
                cur.close()
                scanned_files[entry.name] = True
                with open(settings.SCANNED_FILES_PATH, "w", encoding="utf-8") as file:
                    json.dump(scanned_files, file, indent=4)
                print(f"[DBG] Ingested {entry.name} | Total chunks: {len(chunks)}")
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into the RAG system")
    parser.add_argument("--force", action="store_true", help="Force ingestion")
    args = parser.parse_args()
    ingest_documents(args.force)
