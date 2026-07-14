[video with old-timey black & white filter, saloon music]
Back in the olden days, the only way to do video search was by text - using the video's title and description, or the transcript. These early humans were forced to spend valuable time and resources on tagging and metadata, with no guarantee of successfully hunting for the right video clips.

[transition to normal video]
These were truly difficult times. So - what if I told you that you can run vision-based video searches, like this? [show demo searching 'kindle' have video with Jen holding kindle appear] 

Think about what else you could find in your library. [popup thumbnails of objects highlighted in scenes as I talk] You could find video clips with a particular product, a specific type of presenter, or even based on an event, like this lawyer turning himself into a cat during an actual legal proceeding. 

![image](projects/202607-video-search-tutorial/assets/lawyer-as-cat.png)

In this video, I'll show you how I built this app and what's going on under the hood. I'll also provide the codebase that you can run for free, so you can build your own video search app. 

Let's get into it, starting with how video cataloging typically works. [scene transition]

Videos on YouTube and similar platforms usually include a title and a description that help you decide whether you click on it or not. What you might not have known, though, is that these are crucial parts of the video platform's search algorithm. 

Most video databases, whether it's on a big platform like YouTube, or an internal knowledge base, aren't actually directly "searching" the video. Instead, what typically happens is actually [Scooby-doo meme, "text search" under the mask - "video search" on mask] a text search dressed up as a video search. 

These video databases typically look through the metadata, like the video's title, description and tags, and maybe through its transcript. 

The reason for this is simple - text searches are well known, and work really well. Tools like Elasticsearch can perform keyword searches, vector searches, and hybrid searches, combining the two, really well. 

And look, searching texts that *describes* the video works *okay* in a lot of cases. But if you think about it, it's a little unsatisfying that a video search isn't actually based on anything *visual*. 

It's a bit like Minecraft without mining OR crafting [show reddit thread about this]. It might kind of work, but it ignores a critical piece of the whole thing, and it's also a deeply unsatisfying concept. 

But video search doesn't have to be this way. That's thanks to multimodal embedding models. [show multimodal embedding diagram]. 

As you know, embedding models capture the meaning of an object, like text, into a series of numbers. The more similar the meanings, the closer the embeddings. 

Multimodal embeddings can convert not just text, but others like images. The CLIP models being a famous example.

Some models, like Jina's `v5-omni` family can do this for even more modalities, like sounds, or video. Meaning you can embed a cat meowing into a microphone, and the results would be not too far from the embedding of the text "cat". 

And it's this model, more specifically the `jina-embeddings-v5-omni-small` models that I built the video search app around. And while embedding a video might sound like it should be complex, it's relatively straightforward [show architecture image]. 

If you've seen vector search before, this should seem pretty familiar to you. But there are a few key differences you should be aware of - so let's take a look, starting with chunking. [transition]

The first decision relates to how much of the video to embed at a time. This concept is called "chunking".

Chunking simply refers to splitting up an input asset by size. For text, chunking splits up a long document like a report into shorter texts, based on paragraphs, or topic changes, or just fixed lengths. This means a search can find match a specific part of a document, which is typically more useful than just returning a long document. 

Now, the same need exists in video retrieval. For most cases, it's not going to be useful to for a video search to return a 50-minute meeting recording or even a 15-minute YouTube video that doesn't point to a specific part. 

So then the question is - how do you exactly chunk a video? I think there are really three main strategies you should consider - by fixed length, by visual scene transition, and by semantics using the transcript. 

Just like text, fixed length chunking is a basic, robust method that actually works quite well. It also allows you to be as granular as you want by setting the length of each clip. 

Or, you could generate a transcript and apply semantic chunking. This is another good method, especially where the spoken word dominates, like speeches, meetings or instructional videos. 

But the form that might be the most interesting might be chunking by visual scene transition. I think of this as semantic chunking, but applied to the visuals, not words. 

You don't have to re-invent the wheel to do this, either. There are existing tools like `PySceneDetect` [show code] which will look at the movie, detect a change in scene, and output [show example output] a list of scene boundaries. All you have to do then is to get those scene markers, and split them using another tool like `ffmpeg`. [show code]

The result is a set of scenes that reflect the creator's visual choices, like these [show examples from my clips] - a change in the visual, like a change of the shot in a film, or change in graphics, leads to separates scenes.

Now, we just need to embed these video chunks, or clips. But actually, you have another choice to make here. [transition]

Embedding a video clip is a bit different from embedding text. And that's because video is inherently multimodal. When you think about it, a video is composed of really three layers - the visual layer, the audio layer, and the speech layer. 

You might be surprised that I'm counting audio and speech separately, but here's why - listen to a clip like this [play a clip of a rocket launch]. This has a lot of audio, but no speech. The same would be true if the clip included music, too. 

So information like these sounds would largely get lost if you generated a transcript. But at the same time, the audio track might actually be a distraction to the model if what you're interested in is the words. 

These are the three distinct layers of information. The good news is, you can embed any combination of these three layers, based on what's in your videos, and what your goals are. 

If you are often looking for clips to use in, like, video composition, you might want the visual embedding by itself, and the audio, and the speech separately. So you can search by a particular look or object, by a sound or atmosphere, or what is said. 

You can actually save multiple embeddings per clip, too - and it's not a problem since the model puts them all into the same embedding space. 

My goal was to find technical information from videos. So I chose [show code] to create two embeddings per video  - one combining the audio and the visual, and another based on the speech. 

How I did it was to [show code as I talk] extract the audio from the video clip with `ffmpeg` and getting a transcript with `faster-whisper`. First, I produce the combined audio and visual embedding by providing the video file and the audio file to the model. Second, I produce the transcript embedding by passing the transcript file to the model.

Let's go back to that "Kindle" search you saw at the start of the video. [show search result again, highlight the embedding badge] That result, as you can see from the little badge here, comes from the audio+visual embedding. For this search, the clip's transcript [show transcript for the clip] is completely irrelevant, and relying on just the transcript wouldn't have helped me. 

Again, this is what gives me the flexibility to search for what's on the screen. 

Here's an interesting one - I found that when I [show app] search for the word "superhero", it finds this clip of me as the best hit. 

Now, I don't think the Jina model has uncovered [bad photoshop of me as batman] my tortured past and secret identity. I think what's happening is that the embedding may actually be taking this background Batman figure [zoom into image] into account. 

And that's a nice segue into what it all means, and some of the tradeoffs. Because there are a few things you should be aware of, and some things that I'd do differently even for this demo app. 

[show a graphic with each note as one part of a slide]
[note 1 - explainability]
One thing for you to keep in mind is that vector embeddings are inherently black boxes. Meaning that they lack the clear explainability of keyword, or BM25 searches that are based on exact matches. In that "superhero" search example, it's hard for me to know exactly why that was the closest clip to the query. 

In some fields, that lack of explainability may be an issue. But to be fair, this isn't unique to video searches - all vector searches kind of suffer from this limitation. 
given that black box generative models are everywhere now.

[note 2 - sampling]
You should be also aware that the Jina model embeds videos based on up to 32 sampled frames of a video. So that means as the source video gets longer, and the more scene changes, the more information will be missed. This is another very important reason to get chunking right. 

[note 3 - chunking]
Speaking of which - If I built this demo again, I'd actually use a different chunking method than scene based chunking. On reflection, most of the videos that I'm interested in are technical, where there's usually not much camera movements or scene changes. 

 Technical videos are largely script-driven with the visuals being somewhat secondary. So from that perspective, I actually think semantic chunking based on the script may have been better. 

[note 4 - processing power]
Lastly, you should be aware of the time taken to process and embed these videos. I am running everything for this demo locally, using open-source Elasticsearch, and open-weight versions of Jina models.  But between the video processing, and using the `v5-omni-small` model, my little Mac is doing a lot of work. 

So if you need real-time embeddings, or have a lot of videos, I'd make sure that these processing times are acceptable, or that you have GPUs available to accelerate your runs. 

You can also use the Jina API [show code example] to generate embeddings. Which might be a great solution for many of you. If you're using Elasticsearch, it's [show screenshot] available on Elastic Inference Service as well. 

But these are minor points. The key idea is that you now have a brand new set of tools for video search, enabling searches [back to demo] by visual assets [search "presenter with glasses" to surface visual hit], or by what was said [search "elastic inference service" to surface transcript-based hits] - or some combination of those. 

The repo is available [show GH repo & link] here - to use it, clone the repo, and follow the README. The link is below. As I said, I've built this with the open-source version of Elasticsearch, and the open-weight Jina model. Note that for commercial use, you should use the Jina API, or talk to Elastic's sales team if you want to self-host the model.

Now, I'm using this as a part of my toolset for cataloging technical content. But I'd love to hear what you might be thinking of cataloging - is it internal meetings? library of personal videos? Are you a cat video and memes mogul? Let me know in the comments. 

Or, you could just say "hi". Sometimes I wonder if anyone watches this far. Tell you what, if you write "hi" in the comments, I **promise** I'll write back. 

If this video was useful, please give us a like and subscribe to the channel - it helps others discover the content. Thanks and happy video cataloging!


