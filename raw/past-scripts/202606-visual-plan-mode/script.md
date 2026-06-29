Title
- Stop Approving AI Plans in the Terminal
- Vibe Coding Broke Me: Here's What I Do Instead
- I Don't Let AI Write Code Without My Visual Approval

Thumbnail:
- Text: "TAKE  / CONTROL / OF AI"
- Visual: Screenshot of Plannotator with notes, with a very large "Send Feedback" button shown; if room exist, show a tiny, cramped terminal window filled with a wall of scrolling markdown text, with a 🚫 sign on top of it

(Plannotator: https://github.com/backnotprop/plannotator)

---

## Hook (45s, on camera, scripted)

I used to let my AI agent just... go. But vibe-coding wasn't for me, and plan mode wasn't perfect either. The agent would write a 2000-word plan in the terminal, I'd skim it, hit approve, and then spend hours untangling the resulting spaghetti code and the broken architecture.

So I stopped doing that. Now, every plan the agent writes gets intercepted — pulled out of the terminal and into a visual review where I can actually read it, annotate it, and send feedback before a single line of code gets written.

Here's the workflow: prompt the agent, intercept the plan visually, review and annotate, execute, then visually review the code. Repeat for each stage.

The tool is called Plannotator — it's open source, and it hooks into your agent automatically. To show you how this works, I'm going to build a RAG app backed by Elasticsearch — in two stages. Let me show you.

---

## The Build (Screencast, bullet-pointed for natural reaction)

### Cycle 1: The Deep Dive (Architecture & Data Layer)

To start, I'm going to install Elastic Agent Skills in this directory for my agent.
```
npx skills add elastic/agent-skills --skill '*' -a pi
```

Here's what I'm going to ask the agent to do. First, I'm going to enable Plannotator by activating this extension, and here's my prompt.

*   **Action:** Paste the initial prompt into the terminal: "I have a catalog of blog articles that I've collected to build a RAG TUI to search the assets in the /blogs directory. I want to be able to perform hybrid searches on them, and also use RAG to ask it questions. Use Elasticsearch serverless for convenience. To start with, please create the elasticsearch instance, ingest the data and verify that hybrid search works."

Here's my prompt. notice how I didn't ask it to build the interface yet. I am forcing it to stop at the data layer.

*   **Action:** The UI pops open.
Great. Here's the agent's plan, in this nice Plannotator window. Instead of reading this in the terminal, it's intercepted. It makes it much easier for me to read it and understand what the agent intends to do. Let's take a look

*   **Action:** Review the UI

**3. The Teachable Moment (The Tech Lead Correction)**
*   **Action:** Look at the plan. Notice the agent is trying to do something outdated (e.g., using some unspecified Jina model or even ELSER).
*   **The Fix:** Highlight that specific line in the Plannotator UI. Leave a comment: *"Use the Jina v5-text-nano model."*
*   **Action:** Click 'Send Feedback'. Let the agent revise the plan, then click 'Approve'.
*   **Commentary:** "By correcting it *here*, I am not only saving myself hours of untangling a messy script. Note also that I can add a global comment, and even attach images."

**4. Execution & Visual Code Review**
*   **Action:** Fast-forward through the agent writing the code.
*   **Action:** Trigger `/plannotator-review`. The Code Review UI opens.
*   **Commentary:** "The code is written. Now we do a visual diff review."
*   **Notes:** [Make changes - e.g. did the AI correctly modularise the code? Are there any odd pieces of implementation?]
*   **Action:** Click 'Approve' and commit the changes.

### Cycle 2: The Speed Run (UI & Execution)

**1. The Next Prompt**
*   **Action:** "Great. Now, write a plan for building the RAG TUI."

**2. The UI Tweak (Plan Review)**
*   **Action:** Plannotator opens with Stage 2.
*   **Commentary:** "And you can see how this is going to go. We do the same plan review for this stage too.  through all the details of this (fast forward through making changes). But let's make a product tweak."
*   **The Fix:** Highlight the UI output step and add: *"Instead of just dumping the text, add an ASCII bar chart visualization of the relevance scores next to the retrieved documents."*
*   **Action:** Approve the plan.

**3. Execution & Finale (Skip the second code review)**
*   **Action:** Fast-forward the agent building the TUI.
*   **Commentary:** "Because I trust the foundation, I'm going to skip the final code review diff and just run the app."
*   **Demo:** Run the final TUI app. Show the fast hybrid search working against Elastic Serverless, complete with the requested ASCII visualization.

"And there you go, we have a working content catalog."

---

## Summary (1 min, on camera)

Plan mode solves a lot of challenges related to AI development. But the tooling around using it had been lacking quite a bit, in my opinion. Visual planning and feedback, like what's provided by Plannotator here, makes it easy to plan, review, and code, in stages, making the AI more of a pair programmer rather than an unwieldy outsourced resource.

For me, this approach puts the human judgment front and centre, right where it has the most leverage: to determine architecture and intent, and to leave the easy stuff to the AI.

---

## CTA + Close

Plannotator is open source — link's in the description, works with Claude Code, Codex, OpenCode, and Pi. If you want an amazing data store to work with AI, check out Elasticsearch - as you saw, it's so easy to get your agent to work with it using Elastic Agent Skills, also linked below.

Are you still reviewing AI plans in the terminal? Let me know your preferences in the comments. See you next time.
