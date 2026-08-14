---
type: Script
title: "Ingest and search data in Elasticsearch Serverless with Python"
description: "Connect a Python application to Elasticsearch Serverless, ingest a books dataset, and prove it with full-text and semantic search."
tags: [elastic, elasticsearch, serverless, python, ingestion, semantic-search]
status: draft-v1
timestamp: 2026-08-12T16:34:57Z
---

# Ingest and search data in Elasticsearch Serverless with Python

[Note: not all overlays are described in the script]

-----

[JP name & title in chyron]
Hey there, let me show you how to turn your data into a searchable resource with Elasticsearch.

We add data, view it in Kibana, and even run lexical and semantic searches, in just a few minutes.

[on-screen: overlay showing each stage]

-----

## CONNECT TO ELASTICSEARCH

First, we need the connection details - the URL and the API key.

Open your Serverless project. At the time of recording, it opens the "Getting Started" page, which has the URL, and a default API key that's created for you. You can copy each one with this copy button.

[screen recording: browser: Show new instance; Kibana w/ Getting Started -> screencast in Jupyter]

Let's put these values into an `.env` file to avoid hard-coding them.

```dotenv
ES_URL="YOUR_ELASTICSEARCH_ENDPOINT"
ES_API_KEY="YOUR_ENCODED_API_KEY"
```

Now, we actually have everything we need.

[narrate through video of typing]

[Show cell installing requirements]

We'll import the required pieces,
load the environment variables,
and connect to it with the details that we just grabbed.
And we'll print out some info about our instance here.

You should see information about the cluster here.

```python
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

load_dotenv(overwrite=True)

es = Elasticsearch(
    hosts=os.getenv("ES_URL"),
    api_key=os.getenv("ES_API_KEY"),
)

print(es.info())
```

-----

## INGEST THE BOOKS

Now, we're ready to send data to Elasticsearch

[show one book dictionary, then reveal the five-item dataset]

Here's a list of books - each containing a title, author, release year, and description. This could be any data here.

First, I'll create an index called `books`.

```python
es.indices.create(
    index="books",
    mappings={
        "properties": {
            "description": {"type": "semantic_text"},
        }
    },
)
```

Then use the bulk helper to send our data to the index.

```python
helpers.bulk(
    es,
    [
        {"_index": "books", "_source": book}
        for book in books
    ],
    refresh="wait_for",
)
```

That's all we need to do - to confirm this, let's get a document count with the `.count` method:

```python
response = es.count(index="books")
print(response["count"])
```

You can see we've got five documents in Elasticsearch. Let me show you where to view them in Kibana, and then we'll run some searches.

-----

## SEE THE DATA IN KIBANA

Back in Kibana - if we go to Discover:

[screen recording: open Discover → show the five rows on display]

You see the five documents, with the same fields and values that we sent. You can run queries here as well, but maybe for another time.

So the data is in Elasticsearch. Let's search it.

-----

## RUN A FULL-TEXT SEARCH

Let's search the books index, with a lexical, `match` query, against the title.

```python
resp = es.search(
    index="books",
    query={"match": {"title": "Hail Mary"}},
)
```

And if we print the results:

```python
for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

We get *Project Hail Mary* - because those words appear in the title.

-----

## SEARCH BY MEANING

Let me show you one more cool thing you can do with Elasticsearch.

What if we wanted to search the documents, without using the same words?

Here's another query - with the phrase "surviving alone in space".

```python
resp = es.search(
    index="books",
    query={
        "semantic": {
            "field": "description",
            "query": "surviving alone in space",
        }
    },
)

for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

And *Project Hail Mary* is ranked first again. Even though there's no exact match, we were able to find the right document.

That's because this time, we targeted the `description`.

[show mapping code again]
This is why the mapping that we set up was important. The `description` field was set up as `semantic_text`, which told Elasticsearch to set it up for semantic, or vector, search, that makes use of Jina's embedding models by default.

But we can talk more about that another time.

-----

## WRAP-UP

As you can see, you can turn static data into a searchable set of documents in just a few steps. I showed a small list of books data, but it can be any format, and any size.

Once you've created an index and ingested documents into Elasticsearch - they're available for searches, including meaning-based semantic searches.

I've got links to the resources nearby, so you can try it out yourself.

Thanks for watching. See you next time.
