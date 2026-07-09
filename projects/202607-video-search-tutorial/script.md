What if you could just search videos like this? [show demo searching 'kindle' have video with Jen holding kindle appear] 

Think about what else you could find visually. [popup thumbnails of objects highlighted in scenes as I talk] You could find video clips with a particular product, a specific type of presenter, or even based on an event, like one where the lawyer's turned himself into a cat. 

This is made possible by a newer class of models, called multimodal embedding models. In this video, I'll show you how they work, and how I built this app using an open-source and open-weight stack. 

Let's get into it, starting with how we used to catalog and embed videos. [scene transition]

If you spent any time on platforms like YouTube, you might have noticed that each video includes a title and a description, which provide a little preview of the video's contents. What you might not have known is that these are crucial parts of a video platform's search algorithm. 

When you search for a video, whether it's on a big platform like YouTube, or an internal knowledge base, what typically happens is just text search [Scooby-doo meme] dressed up as a video search. 

It might look through the metadata, like the video's title, description and tags, and maybe through its transcript. 

We used to catalog video this way because we are good at searching text. There's great solutions like Elasticsearch, which can do keyword searches, vector searches, AND what's called hybrid searches, combining the two. 

And look, this works *okay* in a lot of cases. But if you think about it, it is a problem that a video search isn't based on anything *visual*. It's a bit like a clothing catalog with everything except the pictures. You're missing a critical part of the information. 

But video search doesn't have to be this way. Embedding models, which turn your information into vectors, are multimodal now. Those multimodal models are what power image similarity searches, like face similarities or finding images with text. And these days, models like the `jina-v5-omni` family, can even search videos directly. 

Here's how these models work [show multimodal embedding diagram]. 

Generally, embedding models "embed", or essentially "translate", the meaning of a thing, like text, into a series of numbers. And the more similar something is, the closer these sets of numbers are. 

Multimodal embeddings, can convert not just text, but others like images. So whether you input the text "cat", an image of a cat, or a video of a cat, the model recognises that these are all cat-related, and generate similar embeddings. 

Some models, like the `jina-v5-omni` family can do this for other modalities, like sounds, or video. So if you embed "meow meow meow", you'll end up with something not too far from a cat, and the same will happen if you embed a video. 

And it's this multimodality that powers our video search architecture [show architecture image]. 

The videos in our libraries are split up, or "chunked", before being embedded with the Jina model. Then, those embeddings are added to a vector database like Elasticsearch. These can now be searched by the user, using any input that can itself be turned into a vector. 

If you've seen vector search before, this should seem pretty familiar to you. But there are a few key differences you should be aware of - so let's take a look, starting with chunking. [transition]

Chunking refers to the act of defining boundaries of each input to be vectorised. For text, it might be splitting up a long document like a report, into paragraphs, or pages, or even just fixed lengths. This allows a search to match a specific part of a document, leading to more effective retrieval. 

The same need exists in video retrieval. For most cases, it's usually not going to be useful to for a video search to return a 50-minute meeting recording or even a 15-minute YouTube video that doesn't point to a specific part. 

So then the question is - how do you exactly chunk a video? I think there are really three main strategies you should consider - by fixed length, by visual scene transition, and by semantics using the transcript. 

Just like text, fixed length chunking may be the least refined, but it's robust and allows you to be as granular as you want by picking the length. Using semantic chunking from a transcript is a good method, especially where the spoken word dominates, like meetings or instructional videos. 

But the form that might be the most interesting might be chunking by visual scene transition. I think of this as semantic chunking, but by visuals, not words. 

You don't have to re-invent the wheel to do this, either. There are existing tools like `PySceneDetect` which will look at the movie frame by frame, detect a change in scene, and let you know where the scene boundaries are. All you have to do then is to get those scene markers, and split them using another tool like `ffmpeg`. 

The result is a set of scenes that reflect the creator's intent, like these [show examples] - a change in the visual, like a change of the shot in a film, or change in graphics, leads to separates scenes.

Now, all that's left to do is to embed these video chunks, or clips. But - embed, what, exactly? [transition]

Embedding a video clip requires more of a design choice for the reason that a video is inherently multimodal. It is composed of really three layers - the visual layer, the audio layer, and the speech layer within in. 

You might be surprised that I'm counting audio and speech separately, but here's why - listen to a clip like this [play a clip of a rocket launch]. This has a lot of audio, but no speech. The same would be true if the clip included music, too.

And [show an explainer diagram as I talk] each of these, or actually any combination of them, can be embedded together. So really, you seven options - three alone, any combination of two modalities, or all three together. 

What you choose here is a function of what's in your videos, and what your goals are. If you are often looking for clips to use in, say, video composition, you might want the visual embedding by itself, and the audio, and the speech separately. So you can search by a particular look or object, by a sound or atmosphere, or what is said. 

My goal here was to find technical information from videos, so I chose [show code] to embed the audio+visual, and the speech, through the transcript. 

That meant extracting the audio from the video clip with `ffmpeg` and getting a transcript with `faster-whisper`, so that the audio and the visuals can be embedded together as one embedding, and the generated transcript was embedded separately. 

Remember that Kindle search? [show search result again, highlight the embedding badge] That hit, as you can see from the little badge here, comes from the audio+visual embedding. For this search, the clip's transcript [show transcript for the clip] is completely irrelevant, and relying on just the transcript wouldn't have helped me. 

Again, this what gives me the flexibility to search for what's on the screen. I found that when I search for the word "superhero", it finds this clip of me. Now, to be clear, it's not that the Jina model has uncovered my secret work as a vigilante, but I think what's happened it that the embedding may be taking this background Batman figure into account. 

And that's a nice segue into what it all means, and some of the tradeoffs. As fun as building this video search was, there are a few things you should be aware of, and some things that I'd do differently. 

One is that vector embeddings are inherently black boxes that lacks the explainability of keyword, or BM25 searches. In that "superhero" search example, it's hard for me to know exactly why that was the closest vector to the query vector. 

The best that I can do is probably to do some sort of reverse engineering and embedding different visuals to see how that changes the vector. In some fields, that lack of explainability may be an issue. But to be fair, we may all be very used to this, given that black box generative models are everywhere now.

Another thing that I'd do differently is the chunking. I initially went with scene based chunking as you saw. But on reflection, most of the catalog here is technical, where there's usually not much camera movements or scene changes. Instead, a lot of the movie is dictated by the script, and the visuals might be helpers for that. So from that perspective, I actually think semantic chunking based on the script may have been better. 

Lastly, it's the time taken to process and embed these videos. I am running everything for this demo locally, using open-source Elasticsearch, and open-weight versions of Jina models.  But between the video processing, and using the `jina-v5-omni-small` model, my little Mac is doing a lot of work. 

So if you need real-time embeddings, or have a lot of videos, I'd look at API-based solutions, like the Jina API, or making sure that you have GPUs available to accelerate your runs. 

All things considered, these are minor points. The main point is that you now have a brand new set of tools for video search, enabling searches [back to demo] by visual assets [search "movie poster"], or by what was said [search "elastic inference service"] - or some combination of those. 

As I said, I am using this as a part of my toolset for cataloging technical content. But I'd love to hear what you might be thinking of cataloging - is it internal meetings? library of personal videos? Are you a cat video and memes mogul? Let me know in the comments. 

Or, you could just say "hi". Sometimes I wonder if anyone watches this far. Tell you what, if you write "hi" in the comments, I **promise** I'll write back. 

The repo is available here - to use it, clone the repo, and follow the README. As I said, I've built this with the open-source version of Elasticsearch, and the open-weight Jina model. Note that for commercial use, you should use the Jina API, or talk to Elastic's sales team if you want to self-host the model.

If this video was useful, please give us a like and subscribe to the channel - it helps others discover the content. Thanks and see you next time!


