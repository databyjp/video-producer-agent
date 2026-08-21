Hey there, let me show you how to turn your data into a searchable resource with Elasticsearch.

We’ll add data, view it in Kibana, and even run lexical and semantic searches, in just a few minutes.
-----

First, we need the connection details - the URL and the API key.

Open your Serverless project. At the time of recording, it opens the "Getting Started" page, which has the URL, and a default API key that's created for you. You can copy each one with this copy button.

Let's put these values into an `.env` file to avoid hard-coding them.

Now, we’ve got everything we need.

We'll import the required pieces,
load the environment variables,
and connect to it with the details that we just grabbed.
And we'll print out some info about our instance here.

You should see information about the cluster here.
-----

Now, we're ready to send data to Elasticsearch

Here's a list of books - each containing a title, author, release year, and description.

First, I'll create an index called `books` to store our data.

Then use the bulk helper to send the source data to the index.

That's all we need to do - to confirm this, let's get a document count with the `.count` method:

You can see we've got five documents in Elasticsearch. Let me show you where to view them in Kibana, and then we'll run some searches.
-----

Back in Kibana - if we go to Discover:

You see the five documents, with the same fields and values that we sent. You can run queries here as well, but let’s save that for another time.

So the data is in Elasticsearch. Let's run a search on it.
-----

We can search the books index, with a lexical, `match` query, against the title.

And if we print the results:

We get *Project Hail Mary* - because those words appear in the title.

-----

Let me show you one more cool thing you can do with Elasticsearch.

What if we wanted to search the documents, without using the same words?

Here's another query - with the phrase "surviving alone in space".

And *Project Hail Mary* is ranked first again. Even though there's no exact match, we were able to find the right document.

That's because this time, we targeted the `description`.

This is why the mapping that we set up was important. The `description` field was set up as `semantic_text`, which told Elasticsearch to set it up for semantic, or vector, search, that makes use of Jina's embedding models by default.

But we can talk more about that another time.
-----

As you can see, you can turn static data into a searchable set of documents in just a few steps. I showed a small list of books data, but it can be any format, and any size.

Once you've created an index and ingested documents into Elasticsearch - they're available for searches, including meaning-based semantic searches.

I've got links to the resources nearby, so you can try it out yourself.

Thanks for watching. See you next time.
