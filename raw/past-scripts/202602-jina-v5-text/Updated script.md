You’re building a RAG application. But the embedding model is eating half your latency and GPU budget, and you’re starting to wonder - what would you actually lose by going smaller?

That’s the question behind Jina AI's new v5 text embedding models. The two models; v5-small and v5-nano; compete head-to-head with models many times their size, while being state of the art in their own size class.

[popup] Benchmark screenshots

The Jina AI team also released a paper with a ton of detail about their two-stage training approach. They combined knowledge distillation with task-specific LoRA adapters, and they’re refreshingly open about what worked and what didn’t.

-----

## Model Details & Performance

[scene transition overlay]

First, the key facts.

The jina-v5-text-small is a 677 million parameter model, with a 32k token context length and 1024-dimension embeddings. The jina-v5-text-nano is 239 million parameters, with an 8k context length and 768-dimension embeddings.

Both include four task-specific LoRA adapters that let you pick a specialized version of each model at inference time: asymmetric retrieval, text matching, clustering, or classification.

[popup] “LoRA adapters are small, lightweight modules that adapt the model using far fewer parameters”

Both were trained with Matryoshka Representation Learning, and optimised for binary quantisation.

The small model is based on Qwen 3, 0.6 billion base; the nano is based on Euro-BERT 210 million. Both base models are multilingual, and the Jina models were further trained on a corpus spanning 30 languages.

So; how do they actually perform?

[show MTEB English benchmark table]

Both models lead or near-lead their size class on the MTEB. The v5-small scores 71.7, the nano scores 71.0.

To put that in perspective; the nano, at 239 million parameters, is outperforming the Qwen3-0.6B, which is more than twice its size. And both are within a couple of points of the 4-billion-parameter Qwen3.

[beat]

The multilingual MTEB tells the same story:

[popup] MTEB multilingual benchmarks
[show multilingual benchmark table]

V5-small at 67.0, v5-nano at 65.5; again, top of class and not far off the much larger models.

-----

## Retrieval

Jina’s v5 models are trained for asymmetric retrieval; meaning they’re designed to fetch the right documents based on much shorter queries.

Beyond the MTEB, the authors tested against three additional retrieval benchmarks; RTEB, BeIR, and LongEmbed; each probing different aspects.

[popup]

- “RTEB: Private datasets to prevent overfitting / data leakage”
- “BeIR: Zero-shot retrieval across diverse domains”
- “LongEmbed: Retrieval over long-context documents”

[show retrieval benchmark table]

But the picture is consistent. There are a few cases where specific competitors edge ahead; Qwen 3 0.6 billion on English MTEB and LongEmbed, Voyage 4 Nano on a few multilingual benchmarks; but Voyage outputs quite large embeddings at two thousand and fourty-eight (2048) dimensions.

The key takeaway is, neither v5 model has a weak spot with abnormally low scores on any benchmark. That makes them very safe, versatile choices.

-----

## Quantization & Truncation

Both models were trained with Matryoshka Representation Learning to allow output embedding truncation down to 32 dimensions. 

And the performance loss really isn’t bad. Take a look at this:

[show truncation performance graph]

Until you get below 256 dimensions, the loss is relatively minimal. So in many cases, you can significantly reduce your vector index footprint just by shortening your embedding length without giving up much retrieval quality.

Now, what about quantisation? The authors tested binary quantisation, which reduces the precision of each embedding dimension from a floating-point number to a single bit. Even with that massive reduction in size, the v5 models only lost a couple of points on their benchmark scores.

[popup] Show difference between full float embedding vs binary

[show quantisation benchmark table]

So if you’re running on constrained infrastructure; like a 4GB VPS; you could go nano, truncate to 256 dimensions, apply binary quantisation, and still have a very capable retrieval system at a tiny footprint.

-----

## Multilingual Capability

We’ve seen the aggregate multilingual numbers; but the more useful view is the per-language breakdown.

[show multilingual heatmap grid]

Each square in this grid shows how well the v5-small performs compared to other similar models. The greener the better; the redder, the worse.

This is the kind of chart worth bookmarking. Say you’re building a multilingual RAG pipeline and your knowledge base has documents in English, German, and Japanese. You look at this grid; green across the board for those languages. You’d be well served.

But say your corpus is heavily Romanian. You’d see some red here, and it would be worth evaluating alternatives for that specific case. That honesty in the results is actually useful; it helps you make a real decision rather than just trusting a single aggregate number.

-----

## Model Inference

[scene transition overlay]

[show architecture diagram]

The architecture is a standard transformer-based embedding model. You feed in text, it passes through the transformer layers, and the embedding of the end-of-sequence token becomes the output; using last-token pooling.

Notice those LoRA adapters we mentioned earlier.

[graphics: zoom in on LoRA adapters]

At inference time, you pick the adapter that matches your task; you can see the retrieval adapter highlighted here; and the model loads those lightweight adapter weights on top of the base model.

For local deployment, Jina provides standalone weight files with the LoRA weights pre-merged, so you don’t have to deal with conditional adapter loading yourself. They’ve also released 14 GGUF quantisation variants for each model, so you can pick the right size-performance trade-off for your infrastructure. And the models work with popular inference tools like vLLM and llama.cpp for production deployments.

These models are also already available on Jina AI’s inference API, as well as the Elastic Inference Service, so you can try them out with minimal setup overhead.

-----

## Model Training: Stage 1: Distillation

[scene transition overlay]

The v5 Jina models were trained with a two-stage process. 

The first stage transfers knowledge from the larger Qwen 3 Embedding 4 billion teacher model to the student.

[popup] “Knowledge distillation: a smaller ‘student’ model learns to mimic a larger ‘teacher’ model”

It works like this: both models process the same text pairs to produce embeddings; things like title-abstract pairs, or question-answer pairs. 

Then the student is continually updated to minimise the distance between its embeddings and the teacher’s.

The training data is a mix of weakly supervised web-crawled pairs, synthetic data generated by language models, and curated high-quality datasets across 30 languages. The scale and diversity of this data matters; distillation is only as good as the examples you distil on.

There’s a practical problem, though:

The Qwen3 teacher model outputs 2560 dimensional vectors, while the v5 small model outputs 1024 dimensional vectors. So you need a projection layer to bridge the gap. A projection layer is like a translator that allows the two embedding spaces to be compared.

Here, the authors had to decide whether that layer would project an embedding from student up to teacher, or vice versa? And whether to freeze that projection layer during training? 

[show projection layer results]

They tested all four combinations, and found that projecting the teacher’s embeddings down, with an unfrozen projection layer, works very poorly. The projection layer absorbs all the learning and becomes a shortcut, while the student model itself barely improves.

The best approach is in fact the opposite: project the student up to the teacher’s space, and let both the projection layer and student model update together.

One more detail: the initial distillation didn’t work well for retrieving long documents. The authors fixed this with additional training on a curated dataset; synthetic documents with key information hidden in noisy text, plus long book chapters and articles paired with short queries. They highlight that this extra training phase was key to the models’ long-document retrieval performance. The paper goes deeper into the specifics if you’re interested.

-----

### Stage 2: Task-Specific LoRA Adapters

After distillation, they froze the base model weights and trained the four LoRA adapters, each with its own loss function and training data. The good thing about LoRA adapters is that each of them is only around 3 to 4 percent of the base model’s size, so this is much faster.

They trained the retrieval adapter by retaining the same distillation loss from the first stage, and adding two other loss functions.

First, a contrastive loss with hard negatives.

[popup] “A hard negative is a ‘difficult’ negative; like ‘tablet computer’ results for a ‘medicine tablet’ query”

This is what teaches the model to distinguish between results that are semantically close but not actually relevant.

Second, a global orthogonal regulariser, or GOR loss.

[popup] “GOR loss pushes embeddings apart, improving expressiveness and quantisation robustness”

This is why the model retains so much quality under binary quantisation. 

The authors go into further detail on the text matching, clustering, and classification adapters; and if you’re interested in training methods for those tasks, it’s well worth the read.

-----

## Wrap-Up

[scene transition overlay]

So, to wrap up, what you get from this two-stage approach is genuinely impressive for the size. Distil a 4-billion-parameter teacher, layer on task-specific LoRA adapters, and you get these new models at a fraction of the parameter count.

The v5-small matches the 3.8-billion-parameter jina-v4 on retrieval at one-sixth the size, and the v5-nano outperforms models twice as large. Add long-context support, strong multilingual coverage, Matryoshka truncation and quantisation robustness, and these are models you can confidently deploy across a wide range of use cases.

They’re available on HuggingFace, the Jina AI API, and the Elastic Inference Service. Just note the license details if you’re considering commercial use.

[popup] Model card & highlight license details (CC BY-NC-SA 4.0)

What’s interesting is where this leaves the efficiency curve. If models this small can perform at this level today, the next generation of distillation techniques should be really something. 

Okay, thanks for watching. Links to further resources are in the description, and don't forget to hit like and subscribe, to help others find us more easily. 
