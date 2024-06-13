import os

import lib_embeddings
import lib_vectordb

from pathlib import Path
import pickle

from elasticsearch import Elasticsearch
from tqdm import tqdm


# File path for the pickle file containing the books
bookFilePath = "tom.pickle"

# Elasticsearch index name
index_name = "book_wookieepedia_mpnet"
ca_certificate_path = "/home/certs/http_ca.crt"
ssl_verify_options = {
    'ca_certs': ca_certificate_path
}
# Preparing the local transformer
hf = lib_embeddings.setup_embeddings()

# Setting up Elasticsearch as a vector database
db, url = lib_vectordb.setup_vectordb(hf, index_name)

count = 0
files = sorted(Path('./Dataset').glob(bookFilePath))
for fn in files:
    print(f"Starting book: {fn}")
    with open(fn, 'rb') as f:
        part = pickle.load(f)
        for title, value in tqdm(part.items(), total=len(part)):
            title = title.strip()
            content = value.strip()  # Assuming each value represents a paragraph
            # Index document into Elasticsearch
            db.from_texts([content], embedding=hf, elasticsearch_url=url, index_name=index_name)
            count += 1
    print(f"Count: {count}")
