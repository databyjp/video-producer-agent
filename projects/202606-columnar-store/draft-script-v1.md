# Intro

If you use Elasticsearch for logs, there’s a good chance you use another system for metrics - something like Prometheus.

Historically, that split made sense. Elasticsearch *could* store metrics, but it maintained several copies and indexes of the same data. That made many metrics workloads slower and more expensive.

But Elasticsearch now gives you the option to remove that duplication: inverted indexes, BKD trees, even stored identifiers and sequence numbers in specific cases.

What’s left looks less like a traditional search index and more like a columnar metrics engine. Let’s look at the engineering underneath—and whether it makes consolidating your stack technically credible.

-----
