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

## The Structure-First Pipeline

The most useful insight from late-night production — where hosts like John Oliver sound natural on a teleprompter despite reading fully scripted copy — is that **writing and performance are treated as two separate problems**.

The *Last Week Tonight* approach:

1. **Structure first** — write the narrative or argument without worrying about jokes, wit, or energy. What is the story? What does the viewer need to understand, and in what order? Get that right before adding any personality.
2. **Inject personality second** — once the structure is solid, go back through and add humor, analogies, emphasis, and voice. Jokes or vivid examples that don't serve the argument are easy to cut because the structure exists independently.

*The Daily Show*'s head writer Zhubin Parang put the editorial principle plainly: *"It's more important for it to be clear and funny than to muddle things up with a bunch of jokes that don't go together well."* Clarity wins. Energy serves clarity, not the other way around.

For developer advocacy video, this maps directly: nail the technical argument and the viewer's journey through it first. Then inject the analogies, the humor, and the relatable moments. A joke that obscures the technical point gets cut — it would have with LWT too.

## Core Rules

### At the Sentence Level

**One idea per sentence.** Audio gives the listener one pass. If a sentence holds two ideas — even related ones — one of them lands less clearly. Split it.

> ❌ "The index, which was introduced in ES 8.9 and has since been optimized, is now the default for large-dimensional vectors."
> ✅ "This index type is now the default for large-dimensional vectors. It arrived in ES 8.9 and it's been getting faster ever since."

**Contractions, always.** "Don't" not "do not." "You'll" not "you will." "It's" not "it is." Formal expansions signal "written document" the moment you hear them.

**Short sentences for energy; longer sentences for weight.** A run of short punchy sentences builds momentum. A longer sentence signals to the listener that this point deserves slower processing. Use this deliberately, not accidentally.

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

## Clarity Over Cleverness

The broadcast production principle that survives contact with every show, every era: **a joke that muddles the point gets cut**. The structure and the argument are not sacrificed for a better line. When writing for a technical audience, this applies even more directly — a vivid analogy that confuses the technical claim is worse than no analogy at all.

This is not a constraint on creativity. It's what makes creativity useful. A writer who can be funny *and* clear is more valuable than one who can only do one.

## Sources

- Teleprompter.com — [How to Read a Teleprompter Naturally](https://www.teleprompter.com/blog/how-to-read-a-teleprompter-naturally-and-engage-your-audience) (practitioner-level; commercial but well-sourced)
- Journalism University — [Writing for the Ear: Scriptwriting Tips for Audio Presentation](https://journalism.university/audio-podcast/writing-scriptwriting-tips-audio-presentation/) (broadcast journalism academic resource)
- WGA East — [Zhubin Parang interview](https://www.wgaeast.org/onwriting/zhubin-parang-the-daily-show-with-trevor-noah/) (primary source; Daily Show head writer)
- [Natural Scripted Delivery — Research Report](../sources/natural-scripted-delivery-research.md) — full source summary with all references

See also: [On-Camera Delivery](howto/on-camera-delivery.md) · [Script Voice and Style](script-voice-and-style.md) · [Script Structure Patterns](script-structure-patterns.md)
