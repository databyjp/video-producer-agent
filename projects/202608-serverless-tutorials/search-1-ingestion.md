# Search Tutorial 1 — Ingest data with Python

## Video intent

- **Audience:** Developers who have created an Elasticsearch Serverless project but have not added data.
- **Primary viewer job:** Build — connect to the project and ingest a small, searchable dataset.
- **Promise:** Take an empty Serverless project and turn it into a searchable books index with one short Python script.
- **Scope:** Focus on connection and ingestion, verify the data in Kibana, then contrast one ordinary full-text query with one semantic query. Explain only enough of the mapping and `semantic_text` automation to make the difference clear; leave hybrid search and aggregations for subsequent tutorials.
- **Example:** Use the same dataset and Python conventions as the draft quickstart.

## Outline

### 1. Open with the task

- Establish the promise: we will get from an empty project to searchable data by connecting a Python application and indexing JSON documents.
- Establish why: understand how to perform data ingestion so you can do it yourself with your own data.

[on-screen: agenda outline]

### 2. Set up Python SDK; connect to the existing project

- Show how to get the project’s endpoint + API key.
- Store them in a `.env` file.
- Set up the environment.

```shell
pip install elasticsearch python-dotenv
```

- Create the client and verify the connection.

```python
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv(overwrite=True)
es = Elasticsearch(os.getenv("ES_URL"), api_key=os.getenv("ES_API_KEY"))

print(es.info())
```

[on-screen: where to get connection details; move quickly through the prewritten setup]

### 3. Create the index and ingest the books

- Show one book as a normal Python dictionary containing a title, author, release year, and description.
- Reveal the dataset JSON file.
- Create an index with bare minimum configs.

```python
es.indices.create(
    index="books",
    mappings={"properties": {"description": {"type": "semantic_text"}}},
)
```

- Use the bulk helper to index all five documents in one operation.

```python
from elasticsearch import helpers

books = [
    # Books data - could be a raw list of dicts; or loaded from JSON - tbd
]

helpers.bulk(
    es,
    [{"_index": "books", "_source": book} for book in books],
    refresh="wait_for",
)

response = es.count(index="books")
print(f"Indexed documents: {response['count']}")
```

- Explain the core ideas briefly:
  - The bulk helper batches document operations for speed.
  - `refresh="wait_for"` waits until the new books are searchable.
- Show the successful completion and object count.
- Go back to the code, and highlight that the `[{"_index": "books", "_source": book} for book in books]` line is the data being ingested. This can be any iterable whether they came from a JSON file, database, API, or your application.

[on-screen: go through code and run the ingestion script]

### 4. Show the data in Kibana

- Open Discover and select the `books` data view.
- Show that all five documents arrived with the original title, author, release year, and description fields.
- Use this as the visible confirmation that ingestion worked before introducing search.

[on-screen: documents in Kibana Discover]

### 5. Run an ordinary full-text search

- Run a `match` query against the dynamically mapped `title` field.

```python
resp = es.search(
    index="books",
    query={"match": {"title": "Hail Mary"}},
)

for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

- Show *Project Hail Mary* returned because its title contains the query terms.
- Establish the limitation: this search works from the words in the field; what if the user describes the book without knowing its title?

[on-screen: run the query and highlight the matching title terms]

### 6. Explain the mapping, embeddings, and `semantic_text`

- Return to the index creation code and explain what an index is: analogous to a SQL table or NoSQL collection.
- Explain that a mapping defines how fields are indexed and searched.
- Highlight the one explicit mapping choice: declaring `description` as `semantic_text` before ingestion.
- Explain what `semantic_text` did automatically:
  - Selected the default inference endpoint for this Serverless project.
  - Configured the vector field details needed by that model.
  - Chunked each description when needed.
  - Generated and stored embeddings as the books were indexed.
- Explain why this matters: the application sent ordinary text, without generating vectors itself or building a separate inference pipeline, but the descriptions are now searchable by meaning.
- Note that the other field types were inferred from the imported documents.

[on-screen: return to the mapping, then show diagram of what happened during ingestion]
[diagram: book JSON document enters Elasticsearch; ordinary fields are indexed and the description is automatically chunked and embedded]

### 7. Run the semantic search to prove it

- Run the recommended `match` query against the `semantic_text` description field.

```python
resp = es.search(
    index="books",
    query={"match": {
        "description": {
            "query": "surviving alone in space",
        },
    }},
)

for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

- Show *Project Hail Mary* ranked first.
- Explain the result at the outcome level: because `description` is a `semantic_text` field, the `match` query searches by meaning rather than requiring the same words.
- Validate before recording that the final query demonstrates a semantic match rather than overlapping important terms from the winning description.

[on-screen: run the query, compare its wording with the winning description, and show the top result]

### 8. Close

- Recap the completed path: endpoint and API key → Python client → bulk ingestion → data in Kibana → full-text search → semantic search.
- Encourage the viewer to replace the five books with a small sample of their own JSON records.
- Point to a repo or gist for the completed script.
- Bridge to the next tutorial: build more queries that use this data.
