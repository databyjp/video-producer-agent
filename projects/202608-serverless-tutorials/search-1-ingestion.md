# Search Tutorial 1 — Ingest data with Python

## Video intent

- **Audience:** Developers who have created an Elasticsearch Serverless project but have not added data.
- **Primary viewer job:** Build — connect to the project and ingest a small, searchable dataset.
- **Promise:** Take an empty Serverless project and turn it into a searchable books index with one short Python script.
- **Scope:** Focus on connection, index creation, and ingestion. Show one prewritten semantic query as proof of the outcome, but leave query details (e.g. construction, hybrid search, and aggregations) for subsequent tutorials.
- **Example:** Use the same dataset and Python conventions as the draft quickstart.

## Outline

### 1. Open with the result

- Preview the finished result: search for `surviving alone in space` and show *Project Hail Mary* returned first.
- Establish the promise: we will get from the empty project to this result by connecting a Python application and indexing five JSON documents.
- Establish why - understand how to perform data ingestion, enable you to do it yourself with your own data

[on-screen: outline graphic -> preview completed query being run -> graphic indicating use cases for search]

### 2. Set up Python SDK; connect to the existing project

- Show how to get the project’s endpoint + API key
- Store into .env file
- Set up environment

```shell
pip install elasticsearch python-dotenv
```

- Create the client and verify the connection.

```python
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv(overwrite=True)
es = Elasticsearch(os.environ["ES_URL"], api_key=os.environ["ES_API_KEY"])

print(es.info())
```

[on-screen: where to get connection details; screencast coding]

### 3. Create the books index

- Explain what an index is (analogous of a SQL table, or NOSQL collection), why this is helpful (defines how fields are indexed and searched, speed up search)
- We'll create an index to hold book entries

```python
es.indices.create(
    index="books",
    mappings={"properties": {"description": {"type": "semantic_text"}}},
)

assert es.indices.exists("books")  # confirm index exists
```

- Explain what this does under the hood
    - Declare `description` as `semantic_text` before ingestion - powers semantic search, i.e. search by meaning.
    - Infers the other field types from the documents as imported.
    - Sets the default embedding model to power semantic search

- Explain the ingestion consequence: when each book is indexed, Elasticsearch automatically chunks and embeds its description and stores what it needs for semantic search.

- Note to users that if the index exists, an error will be thrown; show code to delete the index

[on-screen: what an index is, screencast code, show diagram of what happens upon ingestion]
[diagram: book JSON document enters Elasticsearch; ordinary fields are indexed and the description is automatically embedded]


### 4. Ingest the books

- Show one book as a normal Python dictionary containing a title, author, release year, and description.
- Reveal the dataset JSON file
- Use the bulk helper to index all five documents in one operation.

```python
from elasticsearch import helpers

books = [
    # The five books from the quickstart
]

helpers.bulk(
    es,
    [{"_index": "books", "_source": book} for book in books],
    refresh="wait_for",
)

response = es.count(index="books")
print(f"Indexed documents: {response['count']}")
```

- Explain the core ideas:
  - The bulk helper batches document operations instead of sending each book manually.
  - `refresh="wait_for"` ensures the new books are searchable before the script continues, which is convenient for this demonstration.
- Show the successful completion & object count
- Show the kibana console with documents

- Go back to the code, and highlight that the the `[{"_index": "books", "_source": book} for book in books]` line is the data being ingested. This can be any iterable of Python dictionaries whether they came from a JSON file, database, API, or your application.

- Note to users that if the re-ingested, they'll get multiple copies of items; but can be prevented by adding unique "_id" to each document

[on-screen: go through code, run the ingestion script, show docs in Kibana w/ Discover, show on-screen recap with graphic]

### 5. Prove the data is ready to search

- Return to the prewritten semantic query from the opening.

```python
resp = es.search(
    index="books",
    query={"semantic": {
        "field": "description",
        "query": "surviving alone in space",  # Note: Might be a different search in video than the quickstart - just for variety
    }},
)

for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

- Show *Project Hail Mary* ranked first.
- Explain the result at the outcome level: the query asks about an idea, and Elasticsearch finds the description with the closest meaning.

[on-screen: go through code, run the query and show what else we can do]

### 6. Show the next questions this data can answer

- Briefly preview what other queries are possible:
  - **Full-text:** Which books mention an exact title, author, or phrase?
  - **Semantic:** Which books match an idea even when the wording differs? (Even when languages differ - w/ current default Jina model)
  - **Hybrid:** Which results best combine exact terms and semantic meaning?
  - **Aggregation:** How is the catalogue distributed by decade or author?
- Connect the example back to the viewer’s own application: the same document pattern can represent products, documentation pages, support articles, or other application records.

[show four question/result pairs: exact words, meaning, hybrid relevance, books by decade]

### 8. Close

- Recap the completed path: endpoint and API key → Python client → index mapping → bulk ingestion → searchable result.
- Encourage the viewer to replace the five books with a small sample of their own JSON records.
- Point to a repo or gist for the completed script.
- Bridge to the next tutorial: build the queries that use this data.
