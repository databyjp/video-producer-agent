---
type: Concept
title: Writing for the Ear
description: How to write scripts that sound natural when spoken — sentence-level craft, formatting conventions, and the structure-first pipeline from professional production
tags: [scripting, writing, voice, teleprompter, delivery, writing-for-the-ear]
timestamp: 2026-07-03T00:00:00Z
---

# Writing for the Ear

Scripts written for the eye sound robotic when read aloud. Scripts written for the ear sound like conversation. The gap between the two is called the **Delivery Gap** — the distance between how you write and how you naturally speak. Closing it happens in the writing, before you ever open a teleprompter app or hit record.

This page covers the craft of writing for spoken delivery. For the mechanics of teleprompter use and on-camera rehearsal, see [On-Camera Delivery](howto/on-camera-delivery.md). For JP's personal voice and tone conventions, see [Script Voice and Style](script-voice-and-style.md).

## What Professional Scripts Actually Look Like — Primary Source Analysis

In July 2026, five full *Last Week Tonight* transcripts were studied as primary source material (S12 E23, E27, E30; S13 E1, E2). These are manually cleaned, screenplay-format scripts from a show that runs fully scripted monologue for 20–35 minutes per episode, delivered from a teleprompter to a live audience. The patterns below come from direct observation, not secondhand description. The full source summary is at [LWT Transcripts S12–S13](../sources/lwt-transcripts-s12-s13.md).

Key finding: the craft in LWT writing is not *primarily* about sentence-level mechanics (though those matter). It's about **structural devices** — recurring moves that create architecture, rhythm, and audience orientation across long-form spoken content. These devices are largely absent from developer advocacy scripts, and adding even a few dramatically changes how a piece feels to a viewer.

## The Structure-First Pipeline

The most useful insight from late-night production — where hosts like John Oliver sound natural on a teleprompter despite reading fully scripted copy — is that **writing and performance are treated as two separate problems**.

The *Last Week Tonight* approach:

1. **Structure first** — write the narrative or argument without worrying about jokes, wit, or energy. What is the story? What does the viewer need to understand, and in what order? Get that right before adding any personality.
2. **Inject personality second** — once the structure is solid, go back through and add humor, analogies, emphasis, and voice. Jokes or vivid examples that don't serve the argument are easy to cut because the structure exists independently.

*The Daily Show*'s head writer Zhubin Parang put the editorial principle plainly: *"It's more important for it to be clear and funny than to muddle things up with a bunch of jokes that might not go together well."* Clarity wins. Energy serves clarity, not the other way around.

For developer advocacy video, this maps directly: nail the technical argument and the viewer's journey through it first. Then inject the analogies, the humor, and the relatable moments. A joke that obscures the technical point gets cut — it would have with LWT too.

## Structural Devices (from LWT Primary Source Analysis)

These are higher-order moves — they operate at the paragraph and section level, not the sentence level. They're what makes long-form spoken content feel authored rather than narrated.

### Announce structure out loud (The Bracket Move)

Oliver almost never transitions silently. He explicitly names what's coming next: *"So given that, tonight, let's talk about DHS. And let's start with its origins."* Every major transition is spoken. The equivalent of a slide heading is a sentence.

In practice: *"So that's the model side. Let's look at what happens when you actually store and search those vectors."*

### Callbacks and running threads

Oliver introduces a detail early — often as a throwaway — then returns to it later, at the exact moment the audience has nearly forgotten it. In S13E1, "Detective Harry Hole" (an absurd Netflix show) is introduced in the cold open, then returned to twice more at increasing levels of absurdity. The biathlon storyline is introduced, lovingly described in detail, then theatrically *abandoned* to get to the main segment — the abandonment itself becoming the joke.

Callbacks do something structural: they give the viewer the feeling that an author is in control, that the piece has hidden architecture. Long-form videos that just march linearly through topics feel like lectures. Videos with callbacks feel like essays.

E.g. *"Remember Cora from the intro — the engineer who checked recall and went home happy? This is the moment her choice starts mattering."*

### Reaction narration — naming the processing moment

After presenting a fact, quote, or clip, Oliver routinely narrates the emotional or intellectual response the audience is having: *"Which is a pretty haunting thing to hear."* / *"Okay. Well. Let us know, I guess!"* / *"Yeah, that's not great."* These aren't filler. They serve three functions:

1. They **pace** the information — they give the viewer a beat to absorb what just happened before the next thing arrives.
2. They **model** the correct response — they validate the audience's reaction without forcing it.
3. They **establish judgment** — they signal that the speaker is evaluating, not just reporting.

E.g. *"And that actually surprised me when I first saw it."* / *"That's the part that took me longest to internalize."* / *"Which means Samantha's getting nearly all of Cora's quality at half the storage cost. That's the whole game."*

### Escalating triplets

Oliver's lists of three are never flat parallel structures. The third item is always more absurd, more specific, or more surprising than the first two: *"Anti-ICE sentiment has spread from Pop-Tart the cat, who posted a video with 'Fuck ICE' on it, to the subreddit 'Massive Cock,' where users captioned dick pics... to an AEW match in Vegas."* The escalation in specificity creates rhythm AND delivers a surprise at the position where the audience expects resolution.

E.g. *"You can tune the number of candidates, the quantization level, or — if you're really trying to squeeze performance — the actual dimensionality of the vectors themselves."*

### Conversational navigation markers

*"And look," "I'll say this," "But wait," "The point is," "And I should say," "To be clear," "For the record."*

These are oral GPS signals. They tell the listener that a register shift is coming, that an important claim is next, or that the speaker is about to step back from the argument for a moment. They are not filler — they are pacing and signaling mechanisms. Without them, spoken content feels like a wall of equally-weighted information.

E.g. *"And here's the thing that changes everything," "Now — and this matters — ," "But let's be honest about the tradeoff here," "Which brings us to the part that actually surprised me."*

### Specificity as the punchline

*"Fancy press conference clothes for uncharismatic business Shreks."* The extreme specificity of the description IS the joke. A generic analogy doesn't land. The more precisely ridiculous the comparison, the more memorable.

Oliver's Medicare Advantage analogy shows the pattern: *"It's like buying a flight that leaves at 6 AM to save money. Oh sure, seems like a good idea until you're at the airport at 4 AM... and can't check into your hotel for another five hours. Aren't you glad you saved $35?"* The detail is what makes the comparison land, not the structure of it.

### Concrete comparisons for numbers and abstractions

Oliver almost never lets a large number or an abstraction stand alone: *"If ICE was a military, it would be the 17th richest in the world — worth about the same as Canada's entire armed forces."* Big numbers are meaningless in audio without an anchor. This goes further than rounding — it finds a comparison that itself carries weight.

E.g. *"At 600 million parameters, it's small enough to run on a single GPU — the kind you're already paying for."* / *"Matryoshka lets you cut that storage in half. In a real deployment, that's the difference between a $400/month cluster and an $800 one."*

### Self-interruption as a rhythm device

Oliver frequently interrupts himself to voice his own reaction to something he just said or heard: *"Wait, what?"* / *"Really? Well, first and least importantly: you're standing."* This creates a spoken aside that both delivers a beat and explicitly models the audience's confusion or surprise.

E.g. *"Hold on — let's sit with that for a second."* / *"And I do mean that literally."* / *"Which, if you've been following along, you'll recognize as the opposite of what Ben's doing."*

### Permission and credibility framing

*"And I don't say this lightly."* / *"For the record."* / *"To be clear."* These phrases establish that the speaker has evaluated the claim seriously. They frame extraordinary statements so the audience doesn't experience them as casual or hyperbolic.

E.g. *"And I want to be honest about this tradeoff — it's not obvious which choice is better."* / *"To be clear: this isn't a flaw in the design. It's an intentional choice."*

## Core Rules

**One idea per sentence.** Audio gives the listener one pass. If a sentence holds two ideas — even related ones — one of them lands less clearly. Split it.

> ❌ "The index, which was introduced in ES 8.9 and has since been optimized, is now the default for large-dimensional vectors."
> ✅ "This index type is now the default for large-dimensional vectors. It arrived in ES 8.9 and it's been getting faster ever since."

**Contractions, always.** "Don't" not "do not." "You'll" not "you will." "It's" not "it is." Formal expansions signal "written document" the moment you hear them.

**Short sentences for energy; longer sentences for weight — but vary asymmetrically.** A run of short punchy sentences builds momentum. A longer sentence signals that a point deserves slower processing. Use this deliberately, not accidentally. LWT transcripts reveal the professional pattern is not just "short = energy" — it's *asymmetric*: [short fact] → [even shorter punchline] → [medium context] → [long buildup] → [short payoff]. The asymmetry creates attention peaks by varying speed in a way that flat alternation doesn't.

**Active voice.** "ES ships the feature" not "the feature is shipped by ES." Passive constructions bury the subject and add words — every extra word costs attention in audio.

**Positive constructions.** "Bring your ID" rather than "you're not allowed in without identification." Negative constructions require a mental flip. Cumulative cognitive load across a 10-minute video adds up.

**Cut relative clauses and parentheticals.** "The tool, which was released last year and has since been acquired by..." — each embedded clause makes the sentence harder to deliver naturally and harder to follow aurally. Break them into separate sentences.

**Plain vocabulary.** Use the word you'd say in conversation, not the one you'd write. "Use" not "utilize." "About" not "approximately." "If" not "in the event that."

### Numbers and Names

**Spell out numbers.** Write "three hundred" not "300." Write "two thousand and forty-eight" not "2048." The reader's eye handles numerals fine; the speaker's brain needs the spoken form. (This is also why past JP scripts include phonetic guides inline: "two thousand and forty-eight (2048)".)

**Round large numbers for comprehension.** "Nearly one and a half million" is more useful to a listener than "one million, four hundred and fifty-six thousand, seven hundred and eighty-nine." Unless precision is the point, round.

**Designation before name.** In prose: "Jane Smith, Director of Engineering." In audio: "Engineering Director Jane Smith." The context arrives before the name, so the name lands with meaning already attached.

### Aural Pitfalls

**Homophones.** "Allowed" and "aloud" look different on the page and sound identical in speech. Scan your script for any word where a listener — without visual context — could mishear the intended meaning. Substitute a synonym.

**Alliteration and consonant clusters.** Phrases packed with sibilant "s" sounds or plosive "p" and "b" sounds are tongue-twisters under pressure. If you trip over a phrase at your desk, you will trip over it on camera. Rewrite it.

**Split sentences across page breaks.** A sentence must never be broken at a page turn. Leave white space and carry the full sentence to the top of the next page. A mid-sentence page flip creates a micro-pause at exactly the wrong moment — in the middle of a thought.

## Formatting for Delivery

A professional script is both the words and the performance instructions. The formatting carries the delivery intent so you don't have to remember it in the moment.

**Line breaks are breathing cues.** Add a hard line break wherever you want to pause, slow down, or create emphasis. This is not grammar — it is staging.

**Emphasis markers.** Underline, bold, or CAPITALIZE words you want to stress. Don't trust yourself to find those emphases spontaneously under the pressure of recording — mark them now.

**Delivery cues inline.** `[PAUSE]`, `[READ SLOWLY]`, `[beat]` are standard broadcast practice. Use them anywhere you want a specific performance effect that won't be obvious from the text alone. Past JP scripts already use `[pause]` and `[beat]` — this is the professional convention, not an idiosyncrasy.

**Layout for reading at speed.** Large font (≥ 14pt for paper, ≥ 36pt for teleprompter), 1.5–2× line spacing, wide margins for hand-annotation. The speaker should be able to track lines at pace without hunting.

Before/after example:

> ❌ "The index construction process, which can take anywhere from a few seconds to several hours depending on the size of your dataset and the number of neighbors specified, is a one-time cost that's generally worth paying."

> ✅ "Building the index takes time.\
> A few seconds for small datasets.\
> Hours for large ones.\
> But it's a one-time cost.\
> And it's almost always worth it."

## The Read-Aloud Test

Non-negotiable. Read every draft out loud before you record it.

What reading aloud catches that visual review misses:
- Sentences too long to say in a single breath
- Awkward word combinations the eye skips over but the tongue can't
- Pacing that feels rushed or sluggish without realizing it on the page
- Unnatural stress points — the places where you instinctively want to emphasize something different from what the sentence implies
- The moments where you instinctively say something slightly different from what's written — those rewrites are almost always improvements

**If a phrase trips you up three times in practice, rewrite the phrase.** Familiarity and speed are not fixes for bad phrasing; they're workarounds that cost you on the final take.

**The dictation method.** Some experienced audio writers draft by speaking first — dictating a rough pass, then editing the transcript. The spoken draft is naturally conversational from the start because it was spoken before it was written. Worth trying if you find yourself defaulting to written-language constructions even after revising.

## Comparing to Our Scripts — What's Missing

Comparing the LWT transcripts against past JP scripts (e.g., the vector search personas script, the Plannotator visual review script) reveals what's working and what's not:

**What our scripts do well:**
- Short declarative sentences
- Breaking up information into steps
- Concrete examples (personas, analogies)
- Signaling structure through section headers

**What's absent — the specific gaps:**

| LWT device | How it appears in LWT | What we do instead | Impact of the gap |
|---|---|---|---|
| Bracket Move | Spoken: "So given that, let's talk about X" | Visual slide / section header | Viewer reads ahead; anchor in the speech is missing |
| Callbacks | Planted detail returns unexpectedly | Each example appears once, linearly | Long videos feel like a list, not an essay |
| Reaction narration | "Which is a pretty haunting thing to hear" | Move immediately to the next fact | No processing space; information density feels punishing |
| Escalating triplets | Third item is most absurd/specific | Flat parallel lists | Rhythm flattens; no surprise at the expected resolution |
| Navigation markers | "And look," "The point is," "But wait" | Visual transitions carry the load | Viewer loses orientation when not watching closely |
| Concrete comparisons | "Worth the same as Canada's military" | Round numbers or raw specs | Abstract numbers don't land in audio |
| Self-interruption | "Wait, what?" / "Hold on —" | [PAUSE] markers or nothing | Emphasis relies on delivery not baked into the words |
| Processing asides | Reactions to technical claims | Skip straight to next point | Viewer has no signal that a key insight just landed |

**The most actionable gap:** Reaction narration and navigation markers. These require no comedy, no rewriting of technical content — just adding spoken orientation cues at transitions and a brief processing beat after important claims. They're the smallest change with the largest audible effect.

## Clarity Over Cleverness

The broadcast production principle that survives contact with every show, every era: **a joke that muddles the point gets cut**. The structure and the argument are not sacrificed for a better line. When writing for a technical audience, this applies even more directly — a vivid analogy that confuses the technical claim is worse than no analogy at all.

This is not a constraint on creativity. It's what makes creativity useful. A writer who can be funny *and* clear is more valuable than one who can only do one.

## Sources

- Teleprompter.com — [How to Read a Teleprompter Naturally](https://www.teleprompter.com/blog/how-to-read-a-teleprompter-naturally-and-engage-your-audience) (practitioner-level; commercial but well-sourced)
- Journalism University — [Writing for the Ear: Scriptwriting Tips for Audio Presentation](https://journalism.university/audio-podcast/writing-scriptwriting-tips-audio-presentation/) (broadcast journalism academic resource)
- WGA East — [Zhubin Parang interview](https://www.wgaeast.org/onwriting/zhubin-parang-the-daily-show-with-trevor-noah/) (primary source; Daily Show head writer)
- [Natural Scripted Delivery — Research Report](../sources/natural-scripted-delivery-research.md) — full source summary with all references
- [LWT Transcripts S12–S13](../sources/lwt-transcripts-s12-s13.md) — primary source: five full LWT episodes studied as direct evidence of professional ear-writing craft (July 2026)

See also: [On-Camera Delivery](howto/on-camera-delivery.md) · [Script Voice and Style](script-voice-and-style.md) · [Script Structure Patterns](script-structure-patterns.md)
