I watch a lot of videos these days. For me, it’s a good way to learn about new developments, *or* look for inspiration. 

But I’ve found video *search* just a bit… unsatisfying. My main issue is that it’s difficult to find clips based on what’s on the screen. 

This is because video search typically ignores the actual *visual*, part of the video. Instead, searches usually rely on *text* metadata, like the title and the description, or the video transcript. 

That’s fine for searching things by content, but not so much if I want to find clips with, say, code examples, or clips that *look* a certain way. 

So I built this: 
[show demo searching 'kindle' have video with Jen holding kindle appear] This goes through my catalog, and find clips by matching their visual and audio components to my query. 

Think about how much easier it would be to search clips like this, to find videos [popup thumbnails of objects highlighted in scenes as I talk] containing a particular product, or maybe a background object. Or, even a scene like this one containing a video conference with a lawyer cat. 

![image](projects/202607-video-search-tutorial/assets/lawyer-as-cat.png)

Today, I'll show you how I built this app and what's going on under the hood. I'll also provide the codebase that you can run for free, so you can adapt it for your own video search app. 

Let's get into it, starting with how video cataloging typically works. [scene transition]

As you know, Videos on YouTube and other platforms include a title and a description, which viewers use to decide what to watch. What you might *not* know, is that these are the main clues for the video platform's search algorithm. 

Most video databases, whether it's on a big platform like YouTube, or an internal knowledge base, aren't actually directly searching the *video*. 

Instead, what’s under the hood is [Scooby-doo meme, "text search" under the mask - "video search" on mask] simply a text search in different clothing. 

The search targets the metadata, like the video's title, description and tags, and maybe its transcript. 

And the reason for this is simple - text searches are well known, and they work really well. 

So most video searches use tools like Elasticsearch to look through what the video is *about*. 

But if you think about it, it's a little unsatisfying that a video search isn't actually based on what's on the *screen*. 

It's a bit like Minecraft without mining OR crafting [show reddit thread headline]. It might work, but it ignores a critical piece, and it's also just deeply unsatisfying. 

We can do better than that, by adopting video-enabled multimodal embedding models. [show multimodal embedding diagram]. 

You probably know what embedding models are. They power vector search by capturing the meaning of text into a series of numbers. The more similar the meanings, the closer the embeddings. 

Multimodal embeddings can convert not just text, but others like images. The CLIP models being a famous model family example.

Some models, like Jina's `v5-omni` family can do this for even more modalities, like audio, or video. Meaning you can embed a cat meowing into a microphone, and the results would be close to the embedding of the text "cat". 

That's what powers the app you saw at the start. And while embedding a video *sounds* complex, it's relatively straightforward. 

As a user, the code can be as simple as this if you're using an API [show code to generate embedding with Jina API]. You simply send a video, and get back an embedding.

The architecture isn't too complicated either. [show architecture diagram]

If you've used vector search before, this should seem pretty familiar to you. But there are a few key decisions you should be aware of - so let's take a look, starting with chunking. [transition]

Chunking simply refers to splitting up an input asset by size. For text, chunking splits up a long document like a report into shorter texts. This means a search can match and return a specific part of a document, which is typically more useful than just returning the whole document, like a report or a book, that you still have to look through. 

Now, the same need exists in video retrieval. For most cases, it's not going to be useful to for a video search to return a 50-minute meeting recording or even a 15-minute YouTube video that doesn't point to a specific part. 

But how should you chunk a video? Well, I think there are really three main strategies you should consider, being by fixed length, by visual scene transition, and by semantics using the transcript. 

The good news is, you can apply any of these using commonly available open-source libraries.

Just like text, fixed length chunking is a basic, robust method that actually works quite well. It also allows you to be as granular as you want by setting the length of each clip. To use this, just use `ffmpeg` [show library] to split each video by fixed lengths. 

Or, you could generate a transcript with something like `faster-whisper` [show faster-whisper] and apply a text-based chunking method. This is another good method, especially where the spoken word dominates, like speeches, meetings or instructional videos. Once you've chunked the text, use the generated timestamps to and `ffmpeg` to the cut videos.

But the form that might be the most interesting might be chunking by visual scene transition. I think of this as semantic chunking, but applied to the visuals, not words. 

You don't have to re-invent the wheel to do this, either. There are existing tools like `PySceneDetect` [show code] which will look at the movie, detect a change in scene, and output [show example output] a list of scene boundaries. All you have to do then is to get those scene markers, and split them using another tool like `ffmpeg`. [show code]

The result is a set of scenes that reflect the creator's visual choices, like these [show examples from my clips] - a change in the visual, like a change of the shot in a film, or change in graphics, leads to separates scenes.

Now, we're almost ready to embed these video chunks. But we have just one more another choice to make. [transition]

The thing is that a video is composed of really three layers of information - the visual layer, the speech layer, and the audio layer. 

Now, I'm counting audio and speech separately, because there's plenty of information in sound that's not speech, like this: [play a clip of a rocket launch]. This has a lot of audio, but no speech. The same would be true if the clip included music, too. 

An embedding can be based on any combination of these three layers. You should make this choice based on your goals, and the nature of your videos. 

If you are primarily needing visual inspiration or assets, you might want the visual embedding by itself. But if you're often looking through, say, meetings, you might want to concentrate on the speech, maybe via the transcript.

You can actually save multiple embeddings per clip, too - and it's not a problem since the model puts them all into the same embedding space. 

I'll show you what I did and why. My goal was to build a library of clips, from talks and so on, to find technical information. But also, I wanted to see how information was presented. So I chose [show code] to create two embeddings per video  - one embedding based on the speech, from the transcript, and another one based on the audio and the visual. 

[show code as I talk] Here, I extract the audio from the video clip with `ffmpeg` and get a transcript with `faster-whisper`. Both the video file and the audio file are provided to the model together like this, which produces one embedding. Second, I produce an embedding of the transcript by passing the transcript file to the model.

Let's go back to that "Kindle" search you saw at the start of the video. [show search result again, highlight the embedding badge] That result, as you can see from the little badge here, comes from the audio+visual embedding. For this search, the clip's transcript [show transcript for the clip] is completely irrelevant, and relying on just the transcript wouldn't have helped me. 

Again, this is what gives me the flexibility to search for what's on the screen. 

Here's an interesting one - I found that when I [show app] search for the word "superhero", it finds this clip of me as the best hit. 

Before you go further, it's not that the model has uncovered [bad photoshop of me as some sort of superhero] my tortured past and secret identity. I think what's happening is that the embedding may be taking this background Batman figure [zoom into image] into account, which is really neat. 

And that's a nice segue into what it all means, and some of the tradeoffs. Because there are a few things you should be aware of, and some things that I'd do differently even for this demo app. 

[show a graphic with each note as one part of a slide]
[note 1 - explainability]
One thing for you to keep in mind is that vector embeddings are deep learning models, and aren't very explainable. 

This is in steep contrast to keyword, or BM25 searches. They are based on exact matches and a formula, so you can easily verify and explain it. But embedding models are deep learning models, which are notorious black boxes. 

Let's take that "superhero" search example. There I can take a pretty good educated guess as to why that clip is the closest one in the library, but it's basically impossible for me to know for sure.

In some fields, that lack of explainability may be an issue. Just to be clear, this isn't unique to video searches. Basically all vector searches suffer from this limitation, but you should be aware of this.

[note 2 - sampling]
You should be also aware video embeddings are based on sampling. The Jina model here embeds videos based on up to 32 sampled frames of a video. 

That means as the source video gets longer, and the more scene changes, the more information will be missed. This is another very important reason to get chunking right. 

[note 3 - chunking]
Speaking of which - I think that if I built this demo again, I'd use a different chunking method than scene based chunking. Most of these videos that I'm collecting are technical. They're not like Hollywood movies - these videos don't involve much camera movements or scene changes. 

Instead, technical videos are largely script-driven, with the visuals being somewhat secondary. So thinking about it again, I actually think semantic chunking based on the script may have been better. 

[note 4 - processing power]
Lastly, you should be aware of the time taken to process and embed these videos. I am running everything for this demo locally, using open-source Elasticsearch, and open-weight versions of Jina models.  But between the video processing, and using the `v5-omni-small` model, my little Mac is doing a lot of work. 

So if you need real-time embeddings, or have a lot of videos, I'd make sure that these processing times are acceptable, or that you have GPUs available to accelerate your runs. 

You can also use the Jina API [show code example] to generate embeddings. Which might be a great solution for many of you. If you're using Elasticsearch, it's [show screenshot] available on Elastic Inference Service as well. 

But these are minor points. The key idea is that you now have a brand new set of tools for video search, enabling searches [back to demo] by visual assets [search "presenter with glasses" to surface visual hit], or by what was said [search "elastic inference service" to surface transcript-based hits] - or some combination of those. 

The repo is available [show GH repo & link] here - to use it, clone the repo, and follow the README. The link is below. As I said, I've built this with the open-source version of Elasticsearch, and the open-weight Jina model. Note that for commercial use, you should use the Jina API, or talk to Elastic's sales team if you want to self-host the model.

Now, I'm using this as a part of my toolset for cataloging technical content. But I'd love to hear what you might be thinking of cataloging - is it internal meetings? library of personal videos? Are you a cat video and memes mogul? Let me know in the comments. 

Or, you could just say "hi". Sometimes I wonder if anyone watches this far. Tell you what, if you write "hi" in the comments, I **promise** I'll write back. 

If this video was useful, please give us a like and subscribe to the channel - it helps others discover the content. Thanks and happy video cataloging!


