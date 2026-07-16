I watch a lot of videos these days. For me, it’s a good way to learn about new developments, *or* look for inspiration.
- [ ] [add thumbnails - elastic videos, ai engineer - leonie, Matt pocock, Tom Scott ]

But I’ve found video *search* a bit inadequate.
- [ ] [add search graphic]

It works well for searching things by content, but not so much if I want to find clips with, say, code examples, or clips that *look* a certain way.
- [ ] [show typing queries into the box like “code example” or “presenter head”]

This is because video search typically ignores the actual *visual*, part of the video. Instead, searches use *text* metadata, like the title and the description, or the video transcript.
- [ ] [graphic indicates search doesn’t link to video]

So I built this:
[show demo searching 'kindle' have video with Jen holding kindle appear] When I run a search here, the app finds clips by matching my query to each clip's visual and audio components.

Think about how much easier it would be to search clips like this, to find videos containing a particular product, or maybe a background object.

Today, I'll show you how I built this app and what's going on under the hood. I'll also provide the codebase which you can run for free, so you can adapt it for your own video search app.

Let's get into it, starting with why this problem exists in the first place. [scene transition]

The main reason that video searches don't actually use visuals is simple - we just haven't had good ways to search videos, while we are very good at text search.
- [ ] Graphic - video search: hard, text search: easy

But if you think about it, it's not ideal that a video search isn't actually based on what's on the *screen*.

It's a bit like Minecraft without mining OR crafting [show reddit thread headline]. It might work, but it ignores a critical piece, and it's also just deeply unsatisfying.

We can do better than that, by adopting video-enabled multimodal embedding models. [show multimodal embedding diagram].

You probably know what embedding models are. They power vector search by capturing the meaning of text into a series of numbers. The more similar the meanings, the closer the embeddings.
- [ ] [show basic embedding model diagram]

Multimodal embeddings can convert not just text, but others like images. One famous example of this being the CLIP family of models.

Some models, like Jina's `v5-omni` family can do this for even more modalities, like audio, or video.
- [ ] [show multimodal embedding model diagram]

Meaning you can even embed sounds, like a cat meowing into a microphone, and the results would be close to the embedding of the text "cat".
- [ ] [show embedding comparison]

That's what powers the app you saw at the start. And while embedding a video *sounds* complex, it's relatively straightforward.

As a user, the code can be as simple as this if you're using an API [show code to generate embedding with Jina API]. You simply send a video, and get back an embedding.
- [ ] [show code example]

And the architecture to build an app like mine isn't too complicated either. [show architecture diagram]
- [ ] [show app architecture]

If you've used vector search before, this should seem pretty familiar to you. But there are a few key decisions you should be aware of - so let's take a look, starting with chunking. [transition]

Chunking just means splitting up the input. For text, that means cutting up a long document into shorter texts.
- [ ] [show text chucking]

This means a search can match and return a specific part of the document. A search with good chunking will return the right passage, rather than saying the answer is *somewhere* in a document.

That same need exists in video retrieval. You can imagine it's not so useful for a video search to return the entire meeting recording or even a 15-minute YouTube video.
- [ ] [show good vs bad video search]

It would be much better for the search to return a specific clip.

But how should you chunk a video? In my opinion, there are three main strategies you should consider.

These are chunking by fixed length, by semantics using the transcript, and by visual changes.
- [ ] [overview chunking methods - highlight one at a time]

The good news is, you can apply any of these using commonly available open-source libraries.

Just like text, fixed length chunking is basic but robust. It allows you to be as granular as you want by setting the length of each clip.

Or, you could generate a transcript and apply a text-based chunking method. This is especially good where the spoken word dominates, like meetings or instructional videos.

Once you've chunked the text, you can use the generated timestamps to cut the videos.

But this next chunking method might be the most interesting. I think of this as semantic chunking, but applied to the visuals, not words. Let's call this scene-based, or visual, chunking.

You don't have to re-invent the wheel to do this, either. There are existing tools like `PySceneDetect` [show code] which will look at the movie, detect a change in visual characteristics, and output [show example output] a list of scene boundaries.

All you have to do then is to get those scene markers, and split them using another tool.

The result is a set of scenes that reflect the creator's visual choices, like these [show examples from my clips].
- [ ] [show scene examples from one video]

A change in the visual, like a change of the shot in a film, or change in graphics, leads to separate scenes.

Once you've set up chunking, there's just one more decision to make before creating embeddings. That is deciding what to embed - let me explain. [transition]

A video is composed of really three layers of information - the visual layer, the speech layer, and the audio layer.
- [ ] [show video being three layers]

Now, I'm counting audio and speech separately. That's because there's plenty of information in sound that's not speech, like this: [play a clip of a rocket launch]. This has a lot of audio, but no speech.

You can think of other examples, like music, animal noises and so on, which isn't speech, but carries plenty of information.

An embedding can be based on any combination of these three layers. You should make this choice based on your goals, and the nature of your videos.

Embedding models like Jina's omni model give you the options to capture as much of these as you want. Meaning that embeddings can be based on any one, or any combination of these three layers.

You should make this choice based on your goals, and the nature of your videos.

If you are primarily needing visual inspiration or assets, you might want the visual embedding by itself. But if you're often looking through, say, meetings, you might want to concentrate on the speech, maybe via the transcript.

You can actually save multiple embeddings per clip, too, with Elasticsearch. And it's not a problem since the model puts them all into the same embedding space.

Let me show you what I did for this demo app and why.

My goal was to build a library of clips, from talks and so on, to find technical information. But also, I wanted to see how information was presented.

So I chose [show code] to create two embeddings per video  - one embedding based on the speech, from the transcript, and another one combining the audio and the visual.

[show code as I talk] Here, I extract the audio from the video clip with `ffmpeg` and get a transcript with `faster-whisper`.

Both the video file and the audio file are provided to the model together like this, which produces one embedding. Second, I produce an embedding of the transcript by passing the transcript file to the model.

Let's go back to that "Kindle" search you saw at the start of the video. That result, as you can see from the little badge here, comes from the combined audio visual embedding.

For this search, the clip's transcript [show transcript for the clip] is completely irrelevant, and actually, relying on just the transcript wouldn't have helped me find the right result.

You know, I was trying different queries, and came across an interesting result. I found that when I [show app] search for the word "batman", it finds this clip of me as the best hit.

It's not that the model's uncovered my tortured past and secret identity. I think what's happening is this:

The video embedding is taking this background Batman figure [zoom into image] into account, and identifying these clips as the closest hits to "batman", even though it's just a small background item.

And that's a nice segue into what it all means, and some of the tradeoffs. Because there are a few things you should be aware of, and some things that I'd do differently even for this demo app.

One thing for you to keep in mind is that vector embeddings are deep learning models, and aren't necessarily very explainable.

This is a big difference to keyword, or BM25 searches. Keyword searches are based on exact matches and a formula, so you can easily verify and explain them.

But embedding models are deep learning models, which are notorious black boxes.

Let's take that "Batman" search for example. There I can take a pretty good educated guess as to why that clip of me with the batman figure is the closest one in the library.

But it's basically impossible for me to know for sure. And I wouldn't be able to break down how much of the embedding's meaning comes from the figure.

In some fields, that lack of explainability may be an issue.

Just to be clear, all vector searches have this limitation of low explainability. So this isn't unique to video searches, but you should be aware of it.

That means as the source video gets longer, and the more scene changes, the more information will be missed. This is another very important reason to get chunking right.

My second note is that video embeddings are based on sampling. The Jina model that I use here creates each embedding based on up to 32 sampled frames of a video.

That means as the source video gets longer, and the more scene changes, the more information will be missed. This is another very important reason to get chunking right.

Speaking of which, I used scene based chunking, but on reflection, I think that might not be the best choice.

Most of these videos that I'm collecting are technical. They're not like Hollywood movies - these videos don't involve much camera movements or set changes.

Instead, technical videos are largely script-driven, with the visuals being somewhat secondary. So thinking about it again, I actually think semantic chunking based on the script may have been better.

Lastly, you should be aware of the time taken to process and embed these videos.

I am running everything for this demo locally on my MacBook Pro, using open-source Elasticsearch, and open-weight versions of Jina models.

But between the video processing, and using the `v5-omni-small` model, my little Mac is doing a lot of work.

So if you need real-time embeddings, or have a lot of videos, I'd recommend that you try it out, and sure that the processing times are acceptable, because video processing takes a lot of compute.

No surprise there really - and if you have access to GPUs, you'll probably be able to do this much faster than me on my little laptop.

You can also use the Jina API [show code example] to generate embeddings and just pay for what you need. Which might be a great solution for many of you.

If you're already using Elasticsearch, the model is [show screenshot] available on Elastic Inference Service as well.

With all that said, I hope I was able to convice you that video search can be better.

That you can find the right clips [back to demo] by what's on the screen [search "presenter with glasses"], by what was said [search "elastic inference service"] - or some combination of those.

The repo is available [show GH repo & link] here. To use it, clone the repo, and follow the README, it's just a few commands to set up and get going.

As I said, I've built this with the open-source version of Elasticsearch, and the open-weight Jina model. Note that for commercial use, you should use the Jina API, or talk to Elastic's sales team if you want to self-host the model.

Now, I built this app to search my technical content library. But I'd love to hear what you might use these tools for - is it internal meetings? library of personal videos? Are you a cat video and memes mogul? Let me know in the comments - I do read all of them.

Or, you could just say "hi". Sometimes I wonder if anyone watches this far. Tell you what, if you write "hi" in the comments, I **promise** I'll write back.

If this video was useful, please give us a like and subscribe to the channel - it helps others discover the content. Thanks  and see you shortly!
