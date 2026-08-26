[Note: not all overlays are described in the script]

-----

[JP name & title in chyron]
Hi I’m JP - I’m a developer advocate with Elasstic. Let me show you in the next few minutes how to ingest data into Elasticsearch so it turns into a searchable resource. We’ll use a Serverless instance and the Python SDK, but the general principle should be the same, regardless of what type of Elastic instance or any of the other SDKs, or even the direct REST API.

[on-screen: overlay showing each stage]

-----

## CONNECT TO ELASTICSEARCH

First, we need the connection details - that’s the URL and the API key.

Open your Serverless project. This is a brand new instance, so it sends me to the "Getting Started" page. If this isn't what you see, you can click on this icon to get there.

You should see a URL here, and you *might* have a default API key that's created for you. If you don’t see this API key, you can create one by clicking through here, and creating an API key with the default options. These are the credentials we’ll use to authenticate against Elasticsearch today.

You can copy each one with this copy button, and I’m going to paste them into this `.env` file, so we don’t hard-code them.

[screen recording: browser: Show new instance; Kibana w/ Getting Started -> screencast in VSCode / Jupyter]

```dotenv
ES_URL="YOUR_ELASTICSEARCH_ENDPOINT"
ES_API_KEY="YOUR_ENCODED_API_KEY"
```

I’ve got a Jupyter notebook so we can run these snippets bit-by-bit; if you’re new to Jupyter, it’ just a REPL environment where the state persists.

I’ve installed these libraries already, but if you haven’t, you can uncomment and run this cell to do so.

We'll start by import the modules, functions et cetera that we'll use here.

```python
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
```

This here will load the env variables in our `.env` file:
```python
load_dotenv(overwrite=True)
```

And we can now connect to Elasticsearch like so
```python
es = Elasticsearch(
    hosts=os.environ["ES_URL"],
    api_key=os.environ["ES_API_KEY"],
)
```

And run this method - to print some details about your cluster.

```python
print(es.info())
```

What you see here should be similar, but slightly different.

-----

## INGEST THE BOOKS

Here's the data that we're going to ingest - it's just a list of dictionaries of book data. Each one contains a title, author, release year, and description, and you probably recognise a few of them.

First, let's create an index to store our data. We've got nicely structured data, so we'll let Elasticsearch infer the data structure from them. The only thing we'll do is to is to set up the `description` field as a `semantic_text` type.

That will let us search objects by meaning, using the default semantic search model, some of you might know what that means, but if you don't that's fine we'll come back to that.

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

And once we have the index, we can add data to it.

The fastest, easiest way is probably to use this `helpers.bulk` helper function.

Pass the Elasticsearch handle here,
Pass the iterable with the index to add the data to, which is `books`, and the source object - I'm building this as a list comprehension here, containing dictionaries.

And since there's just five elements - I'll ask Elasticsearch to only send a response when these objects are not only ingested, but ready for search.

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

And since we have a response, that means all these books are in Elasticsearch!

We can confirm this programmatically, with the `.count` method, like this.

We'll get the response,
And print the 'count' attribute.

```python
response = es.count(index="books")
print(response["count"])
```

And it confirms that we've got five documents in Elasticsearch.

Let me quickly show you where to view them in Kibana, and then we'll run some searches.

-----

## SEE THE DATA IN KIBANA

Now back in Kibana - if we go to the Discover tab here -

[screen recording: open Discover → show the five rows on display]

You see the five documents, with the same fields and values that we sent. You can run queries here as well, but let’s save that for another time.

So the data is in Elasticsearch. Let's run a search on it.

-----

## RUN A FULL-TEXT SEARCH

Now that we've got the books in Elasticsearch, let me show you how easy it is to search through them.

To search the books index, use the `es.search` method, specify the index name, and then the query.

To start, let's look for books based on its title, and look for the terms "Hail Mary".

```python
resp = es.search(
    index="books",
    query={"match": {"title": "Hail Mary"}},
)
```

And to look at the results,
we want to look through the hits - the outer one is the results container, and the inner one is the documents.
Then, let's look at their score, and the title.

```python
for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

We see that there's just the only result - Project Hail Mary. Because none of the other titles contain these words.

-----

## SEARCH BY MEANING

So, when you can find the right words, search seems pretty straigthforward. But what about searches with typos, synonyms, and so on? In other words, where the query doesn't use the same words as the document?

That's where semantic search comes in. Let me show you.

We'll call `es.search` again, and search the same `books` index.

This time, instead of a `match` query, we'll use a `semantic` query.

The field we want to search is `description`, and for the query, let's use the phrase "surviving alone in space".

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
```

Let's run that.

We can use the same loop as before to print the score and title for each result.

```python
for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

And *Project Hail Mary* is the first result again! Even though its description doesn't contain the exact phrase "surviving alone in space".

Elasticsearch found it because this query searches the meaning of the description, rather than only looking for matching words. This is semantic search, which works based on similarity of meaning.

Let's scroll back to the mapping we created earlier.

[show mapping code again]

We set `description` to the `semantic_text` field type. That tells Elasticsearch to generate the data it needs for semantic search. On this Serverless project, Elasticsearch uses Jina's embedding model by default, but this is configurable.

So once that field was mapped and the books were ingested, we could search their descriptions by meaning without setting up a separate model ourselves.

-----

## WRAP-UP

Let's quickly recap what we did.

We connected to a Serverless Elasticsearch project with the Python client. Then we created a `books` index, mapped the `description` as `semantic_text`, and ingested five documents with the bulk helper. That meant Elastic inferred the necessary fields based on our data, and the books data was already ready for search.

With all that done, we performed a couple of searches -one through the titles for matching words, and searched the descriptions based on meaning.

The data here was a small list of books, but the same steps apply to your own documents: create an index, define any mappings you need, ingest the documents, and query them.

I've included links nearby so you can try this yourself.

If you'd like help getting this set up in your own environment, the Customer Architecture team is here for exactly that. You can book a free session using the provided link, they can get you sorted.

Thanks for watching. See you next time.
