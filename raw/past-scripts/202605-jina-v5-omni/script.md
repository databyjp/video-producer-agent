# PDF, video, audio, and text walk into a search engine (jina-v5-omni)

---

### 1. Hook: The pain of fragmented information

Let me ask you. What if search could be as easy, or as fun, as this?

[Show clip of Florian saying "meow meow meow meow" into his computer and finding cat images]

Now, you might not speak fluent cat like our Principal Software Engineer and feline media librarian Florian here, but you can probably relate to the idea.
[image of Florian in a library full of cats - (get img of library, add cats, add Florian) - check with Florian if joke ok]

Because we've all had this experience, where you know that this thing exists, somewhere, but just.. you know, not in front of you.

It might have been in a PDF attachment, or an online meeting recording, or maybe it's in one of 120 presentation files, all named "Weekly stakeholder presentation".
[show visual of this - (fake Finder image - all same names, different suffixes)]

And your search engine can't help you here, because it only speaks text.

**[animation: different formats — PDF, audio waveform, video frame, screenshot — each with a NO cross in with arrow pointing to search bar]**

Now, you *could* rely on the old PanicSearch algorithm - where you scroll through files, ask coworkers on Slack, or hope that your memory has turned into an organised mind palace. But we all know how unreliable and costly these are.

Why is it so hard to search these media types together in one query?

-----

### 2. Why this is hard

The main problem is that searching across multiple types of media requires one of two compromises. One option is to combine multiple pipelines, with a separate embedding model and a separate index for each one.

**[animated system diagram: separate pipelines for text, images, audio — each with its own model, index, search endpoint]**

With this first approach, the system needs one model for text, another for vision, and a third for audio. Each produces its own embeddings, stored in its own index. And when a user searches, the system runs queries against each index separately, and getting back separate result sets.

It's a lot of infrastructure and maintenance. And the results might still be mediocre, because you need to combine these results from separate searches at the ranking stage, somehow comparing apples to oranges from separate embedding spaces.

The second option is to use a multimodal embedding model. The problem with this approach is that the models tend to be massive — we're talking multiple billions of parameters, with some as big as 7 billion parameters.

This means the models can be slow, and expensive to run. Some frontier models with these multi-modal capabilities are closed-weight, which means you don't really know what's inside and you can't run them locally.

-----

### 3. The reveal

The new jina-v5-omni models solve all of these, as compact omni-modality models that handle text, images, audio, and video, all mapped into a single embedding space.

**[show model comparison graphic]**

The v5-omni-small model is about 1.66 billion parameters with all extensions loaded, and the nano is about one billion parameters. Their compact size makes them very efficient, with the nano model, in particular, able to even run on commodity hardware.

The model's efficiency goes beyond the top line size. If you saw our video about Jina's v5-text model, you might remember that the LoRA adapters can be loaded at runtime, meaning that you weren't burdened with unused weights.

The v5-omni does something similar, at a much larger scale. With the omni models, each media encoder is a separate module loaded at runtime. If you only need image and video search, the audio encoder is not loaded. If you only need audio, the same thing - the vision module is skipped. You're not wasting resources on parts of the model that's not used. They call this dynamic weight loading.
[show paper section on this]

This is thanks to the general architecture of the model, which the Jina team's paper calls "Geometry-preserving embeddings via Locked Aligned TOwers", or [pause] GELATO. [add stock image of gelato with Jina logo]

The v5-omni models are composed of discrete models. It takes encoders that were already trained inside other large models, and bolts them onto the text backbone *without retraining any of them*.
[show screenshot - top right of p1 of paper, showing the vision encoder from Qwen 3.5, the audio encoder from Qwen 2.5 Omni]

The only new training is in the tiny projector layers that sit between each encoder and the text model — representing just 0.35% of the total model weights. Another reason that this model is so compact.

**[visualisation opportunity: figure 2 of paper, highlight new parts "0.35% of total weights" callout]**

But size means very little if the model isn't any good. Let's take a look at how the model performed in each of the four modalities, which were tested with these benchmarks:

MMTEB for text, MIEB for images, MMEB for video, and MAEB for audio.
[Show what each acronyms means as I say these]

Which, incidentally, is the highest number of Ms and Bs in a sentence since the lyrics of Hanson's MMMBop.
[picture of Wikipedia page on MMMBop]

Across all four, v5-omni-small averages a score of 53.93. That's the highest of any open-weight model under five billion parameters.
[show benchmark table screenshots — Table 1 from paper: omni model comparison across text/image/video/audio]

It also has the strongest text-only performance of any comparable omni model — because the text backbone is completely unchanged from jina-embeddings-v5-text, which already leads its size class on MMTEB.

-----

### 4. Example: Video search

[Note for reviewers - this may change depending on what demos are available at the time / I might just insert Florian]

For this first example, we took the trailer for the 1961 film Breakfast at Tiffany's, which is 158 seconds long.

What we did was to use PySceneDetect to split the trailer into 28 individual scenes, then generated an embedding for each scene using v5-omni-small. Which gives us 28 video embeddings sitting in a single Elasticsearch index, and we can search them with plain text.

**[mock search UI — type query, results appear with scores]**

When we query Elasticsearch with the word "cat", the top result is the one scene in the trailer with a cat in it. The next best match also makes sense, as it does show a man in a dog mask, which is probably the closest animal reference.
**[Show the top results]**

And, if we search for the word "kiss" instead, and look at the top results, they all correct contain kisses - apparently there's a fair bit of that in the trailer.

**[Show the top results]**


On the Charades-STA benchmark — a standard test for moment retrieval in video — v5-omni-small scores 55.57. ByteDance's Seed1.6-embedding, a closed-weight model, scores 29.30.

**[popup: Charades-STA scores — jina-v5-omni-small: 55.57, Seed 1.6: 29.30]**

The paper notes that moment retrieval — finding the right *moment* inside a video — is where the omni model really shines, which makes this an especially good choice for that type of a task.

-----

### 5. Example: Cross-modal search

Now, you'll remember that at the start of this video, we showed you this clip of Florian:
[Show same clip of Florian saying "meow meow meow meow". Leave up a thumbnail as I talk next]

You can probably now guess what's happening here. He's saying "meow meow meow meow" into the demo, where that audio is translated to an embedding, then used to find the right images.

This same principle extends to other modalities too. In the same video, Florian takes us through how he can find genres of music with a text search, find invoices among a set of documents just by uploading one as the query, and even combine modalities during search, using a drawing of a car and the text "white", so find images of white cars!

Our blog shows similar examples where a scan of a page matches the extracted text content
[show this part from the blog]

And match audios to text, of course.

All of that means you've got huge possibilities for search.

On visual document retrieval benchmarks, v5-omni-small, using just under a billion parameters, scores better than a leading 3-billion parameter model, and just under a 7-billion parmeter one, which is almost 8 times as large.

**[popup: ViDoRe scores - table 2 from paper]**

Before we get into how this works — I'm curious. What would you search for if you could query across all your data at once? Drop it in the comments. And if you're finding this useful, click that like button on the way - that helps others to find us.

-----

### 6. Under the hood

Let's talk a little more about what the team did to build this model.

First: they used encoders extracted from *trained VLMs* like Qwen, rather than raw SigLIP2 or Whisper directly. These VLMs suit these omni type models, because they already understand how their outputs relate to text. So the projectors in the jina omni model only need to bridge an already-small gap, not building a bridge from scratch.

**[architecture diagram animation: frozen encoders highlighted, then small projectors highlighted]**

And that leads to remarkably efficient training. Projector-only training runs about twice as fast for vision and nearly four times faster for audio compared to full training.

One detail that's easy to miss is this. The projectors aren't shared across tasks. Each task adapter — retrieval, clustering, classification, similarity — has its own projector weights. So when you select "retrieval," you're switching the LoRA adapter *and* the projector. It's task-specific all the way through.

And because the text backbone is completely untouched, v5-omni produces identical text embeddings to v5-text.

This is a huge win if you already have a text index that uses the v5-text model. You can add images, audio, and video to it without rebuilding anything.

The model also inherits v5-text's optimisation for Elasticsearch's Better Binary Quantisation, or BBQ, that gives you 93% storage reduction with less than 3% accuracy loss.

**[popup: BBQ — 93% storage reduction, <3% accuracy loss]**

And it inherits Matryoshka Representation Learning, so you can truncate embeddings to fewer dimensions. You can see the truncation tradeoff between vector length and recall here - some modalities like video are more sensitive than others to truncation, so keep that in mind to make the tradeoff that makes sense for you.

**[visualisation opportunity: line chart from paper — nDCG@10 vs truncation dimension, text/image steady, video dropping off]**

Between Matryoshka truncation and BBQ, you've got two levers. Truncate to 256 dimensions, apply binary quantisation, and you're looking at a dramatic reduction in index footprint — with most of the retrieval quality intact.

-----

### 7. Tradeoffs

Let's talk about key tradeoffs and details you should be aware of.

For video, the model extracts up to 64 evenly spaced frames of each clip, before embedding it.
[Add note - 32 if you're using the Jina API]

So the longer the video, the more details will be lost. What you should be doing is what we did with the trailer: split your video into short clips and embed each one individually. Then you can find the right sections more readily.

There are also some areas where the team is still actively working on improvements. Finding specific videos from natural language descriptions — as opposed to finding moments within a video. Image-to-image search and retrieval. And processing mixed media inputs, like an image with accompanying text. The authors are very honest about the details - so check out the paper and the blog.
[Show "Strengths and limitations" section of the blog]

One more thing: LoRA adapter selection matters. The retrieval adapter is not the same as the clustering adapter, which is not the same as the similarity adapter. Use the right one for your task, or your results will be off.

-----

### 8. Wrap

I'm personally really excited to see how you use the new jina-v5-omni models, and I'm going to certainly be putting it to good use. For one, I can finally put together a multimodal catalog of our YouTube and blog content to search through.
[show screenshot of YT channel & videos]

I'm sure many of you will be cataloging your personal knowledge base, or enterprise knowledge with this too. And hopefully it makes it easier to find that *one annoying thing* that you know you saw, with more efficiency and reliability. All without the wastage of a massive model.

jina-embeddings-v5-omni is available on the Elastic Inference Service, the Jina API, and Hugging Face. Links and details of what I talked about are in the description. Check the licensing details for usage, and you can contact Elastic sales for commercial use!

Thanks for watching. Let us know if you have any comments!

https://jina.ai/models/jina-embeddings-v5-omni-small/
https://huggingface.co/collections/jinaai/jina-embeddings-v5-omni
https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index
https://arxiv.org/pdf/2605.08384 [check for new version being published]
https://www.elastic.co/docs/explore-analyze/elastic-inference/eis-supported-models [check docs updated]
https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-jina
