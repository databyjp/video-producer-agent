Working Title: Your coding agent is a black box. It doesn't have to be.

In March this year, many Claude Code users began to complain that their agent felt 'dumber' than before.
[insert screenshots here]

Now, this has been a common, timeless, and unprovable complaint - the "they don't make things like they used to" of the AI world. [photo - basically some version of old man yells at cloud / old man on couch with this in speech bubble]

But in early April, a four-and-a-half-thousand word GitHub post changed all that.

Stella Laurenzo, a Senior Director of AI at AMD, came with receipts. She used data from almost 7000 Claude Code sessions to comprehensively demonstrate the agent's regression. Her work was so compelling that it led to an Anthropic investigation and a public report detailing their findings and fixes.

This story is very instructive. So let's follow the data, her conclusions, and then how to build a similar early-warning system for your *own* agents - so that the next time something like this happens, you're not flying blind.

[pause]

We all love a good detective story - whether it's Sherlock Holmes, Nancy Drew, or Detective Pikachu. [flash images of each - including detective pikachu]

My favourite part of Laurenzo's analysis was that she figured all this stuff out from the analysis of local session logs produced by Claude Code.

[Text popup: "Claude Code users: consider increasing the retention time from the default 30 days, like Simon Willison says here" - show screenshot: https://simonwillison.net/2025/Oct/22/claude-code-logs/]

Across three months, the AMD team had logged 68 hundred sessions, 17 thousand thinking blocks, and over 230 thousand tool calls. She broke this data down into periods that she called the "Good", "Transitional" and "Degraded". [The Good, The Bad and The Ugly poster with new captions?]

For simplicity, let's talk about the stats across two of those periods - the "Good" and the "Degraded".

The agent’s read activity to edit activity ratio collapsed overall from 6.6 reads per edit during the Good period to 2 during the Degraded periid. Meaning that on average, the agent was fact-gathering 70% less often before making changes.
[GH stat on screen as overlay]

She had plenty of other stats too - the post also demonstrates that edits without any reading, circular loops, and premature stopping all occurred significantly more often than before.

[GH stat on screen w highlights: edits w/o reading: 6.2% to 33.7%, circular loops from 8.2 to 26.6 per 1000, premature stopping 173 times vs 0]

It wasn't just quantitative stats, either. Qualitative metrics like manual user interrupts rose sharply, and Claude began describing its own in-chat work as "lazy", "rushed" or "sloppy". [stat: manual interrupts rising from 0.9 to 5.9 per 1000]

And to top all of that, as the output quality went down, their token usage went up. Way up, in fact.

Between February and March, she estimates that the daily usage in tokens increased by a factor of *over a hundred* for a similar number of prompts.
[show stat]

To be fair, there *are* mitigating circumstances - it wasn't just the agent using more tokens by itself. She adds some of the token increase was due to very excited engineers spinning up further sub-agents. But the result was pretty bad, since they were now trying to do more, with degraded agents.

She sums up the change from an engineer's perspective, going from, quote: "I can run 50 agents and they all produce excellent work" to quote "every single one of these agents is now an idiot."

In fact, she found that thinking blocks were about 70% shorter in the Degraded period than the Good period. This is important, because as she points out, the model being able to spend tokens to think deeply is key to solving these complex problems.

Although they had no way of knowing why, this was amazing detective work to prove degradation of Claude Code during this period. [text - For clarity, the issues have since been resolved]

Reading her post made me very curious about  my own agents. Would I'd even know if their behaviour ever changed? How will I achieve my dream of delegating my work to agents and spending more time gaming if I can’t even do that?

So I decided to take a look.

=====

One experiment I ran was to build a reverse proxy that sits between my coding agents and the model, parses the traffic, and ships everything to Elasticsearch. [diagram: model ↔ proxy ↔ harness ↔ user, with another arrow from proxy to ES]

I pointed it at a few different harnesses doing the same task, and started poking around.

Within a day, the data turned up something surprising. Two harnesses with similar token usage on the same task had vastly different bills - one was costing almost three times as much as the other. That seemed so odd, that my first thought was that I had messed up - which to be fair, won’t be uncommon.

But an online search led me to this GitHub pull request, flagging a prompt-caching bug in OpenCode. [OpenCode Gh Issue]

The behaviour matched: under certain conditions, OpenCode could miss the cache, which means slower inference and dramatically higher cost - exactly what I was seeing in the data.

Look. You're not always going to find little gems like this; and I was probably quite lucky here to come across a bug in my tiny demo for a video. That's like buying a Lego dinosaur and finding a real fossil inside - it shouldn't really happen, but I'll happily take it.

The point isn’t the bug - bugs are a fact of life, and I still think OpenCode is amazing. But it does make me wonder - what else might you find if you look?.

[back to architecture diagram]

Now, a bespoke proxy isn't great for production. You're running a separate process, adding a network hop, managing certs and auth. The proxy itself needs to be maintained - which isn't trivial, even when vibe coding - in some ways - especially vibe coding - but I digress.

The deeper problem is conceptual. A proxy sits between the harness and the model. It can see the traffic, but it has zero visibility into the harness. Internal state, tool execution details, error handling; all invisible. You're still treating the harness as a black box.

What you actually want is instrumentation inside the harness. And that's where OpenTelemetry comes in. [otel docs?, e.g. https://opentelemetry.io/img/otel-diagram.svg]

OpenTelemetry, or OTel, is a standardised observability framework for emitting traces, metrics, and logs. The major coding agents like Claude Code, OpenAI Codex and Gemini CLI have first-party OTel output built in. And others, like OpenCode and Pi, have plugins or extensions. [Screenshots of otel support/plugins in docs or repo]

The good news is you don't have to be an expert to set this up. I was able to wire up my coding agent's OTel extension, using the docs and Elastic Agent Skills, in less than an hour, so that all usage data is sent to this Elastic instance. [Flash Elastic Agent Skills repo & link] [Show Elastic instance with rows of data]

==========

This is my resulting dashboard. Let’s view it through the lens of which parts of this dashboard might have caught the degradations seen by Laurenzo? [Dashboard screen] [In this section - highlight various parts of the dashboard to match the script]

At the top, I've got the global usage stats - sessions, turns, tool calls, failures. Useful as a baseline. But I think the next parts are even more meaningful.

[Note the symptoms as an overlay?] Symptom: manual interrupts spiking from 0.9 to 5.9 per thousand turns. This panel shows stop reasons over time - did the turn end on a tool call, did the model finish naturally, or did I manually stop it? A spike in that last category is exactly what AMD would have seen as engineers saw the model doing the wrong thing and yanked the chain.

Symptom: the read-to-edit ratio collapsing from 6.6 to 2, and edits-without-reads jumping from 6% to 34%. The read-to-edit ratio reduction was a key stat, and this chart shows exactly that. We also have a chart that breaks down tool calls by type, alongside the read-to-edit ratio over time. If something changes - the model, the harness, a server-side update - I'd expect this ratio to move.

Symptom: tool calls failing more often. Here I've got tool outcomes over time. If something starts breaking tool calls - a model regression, a flaky plugin, a new permissions setup - the failure rate climbs here. I also track tool call patterns, so that if a tool isn't being called when it should, or its data usage patterns change, I'll see here.

And the dashboard doesn't need to be perfect right away. That's the beauty of having the underlying logs and metrics in Elastic - I can build whatever dashboard I need later, and run any in-depth analysis on the raw data when I notice something off.

The point is that this gives you a real-time display. Look, streaming a dashboard isn't going to win a lot of viewers on Twitch - but it's probably more useful than yet another gaming channel.

If a model update shifts behaviour, if a server-side cache bug degrades context, if a harness update changes defaults - I should see it in the trend line.

Before we move on - what do you think about these dashboards? What's good, what's bad, what's missing? I'm also considering videoed on setting up telemetry for major harnesses, like Codex or Claude Code. I’d love to hear from you, which will help us plan these.

And oh, on the way to the comments -give us a like - it’ll help to keep me employed, and help others to find these videos!

=====

Let's come back to where we started, and close the loop on Laurenzo's story.

Just under a month after her post, Anthropic published their report. It turned out multiple things had changed simultaneously.

One: the harness had changed. The default reasoning "effort" parameter went from high to medium, affecting a lot of people.

Two: the new Opus model introduced something called "adaptive thinking", which lets the model decide its own thinking budget. This is a great idea for efficiency, but it had a side effect of sometimes deciding not to think at all.

Three, and probably the most significant, was a server-side bug. Anthropic had introduced a caching efficiency feature that would discard old thinking blocks on resumption, after a month. But the bug meant that once this feature was triggered, it silently dropped all thinking blocks from subsequent message histories - and without the thinking blocks the model just didn’t have enough context while missing the cache, which both degraded performance and increased cost.

From the user perspective, these happened at similar times with little visibility. I can imagine it being a frustrating experience for everyone, with little proof that something was even wrong - except for Stella Laurenzo. The difference between her and everyone else was that she looked into the logs, performed rigorous analysis, and identified what was going on.

==========

Up to this point, I've been telling you how wonderful logs are. But let's talk trade-offs.

One: session logs generate real data, and retention costs money. As always with observability, you should keep an eye on the volume your team is generating, and decide what to log and how long to keep it for.

If Timmy over there in your team is constantly spawning 50 sub-agents for a random side project that runs all week, or using OpenClaw to troll Redditors, maybe that doesn't need as much retention as the data from agents working on your company's main product.

Two: real risk of leakage. These logs can capture confidential information and credentials, and become a yet another potential attack surface and liability. So make sure that you don't create any more risks than you have to. You could exclude message bodies, log metadata or metrics only, or have custom sanitisation logic. None of them are perfect, but you should see what makes sense for you. When building these demos, I saw my agents execute shell commands with credentials right in them, which would not get redacted and end up in the logs.

I should shamelessly plug, though, that that's another reason for going with a proven product like Elastic with great, granular security and access control. [pause, wink and put up deliberately cheesy graphic?]

Three: this gets set up, but never looked at again. Build the habit of looking at it, and set up alerts on the signals that matter to you - so you don't have to.

==========

The lesson for me from all this is that every session generates signal.

Right now, your agent is making decisions you can't see, using a harness that grows more complex all the time, shaped by server-side parameters thousands of kilometres away from you. And unless you're capturing that signal, you're flying blind.

OTel support is built into the major harnesses, or one plugin away. Elastic gives you somewhere secure, and easy to use, to send it, monitor it, and investigate it.

Your coding agent is a black box. It doesn't have to stay that way.

Thanks for watching. I read every comment so please let me know if any questions. Like I said, give us a like if you can - it helps others find our work. If you didn't like it, that's fine too - if you let us know why, that'll help us improve.

See you next time!

Sources: https://github.com/anthropics/claude-code/issues/42796 https://github.com/anomalyco/opencode/pull/14743 https://www.anthropic.com/engineering/april-23-postmortem

https://code.claude.com/docs/en/monitoring-usage https://developers.openai.com/codex/config-advanced#observability-and-telemetry https://geminicli.com/docs/cli/telemetry/ https://github.com/danilofalcao/opencode-observability https://pi.dev/packages/@devkade/pi-opentelemetry?name=otel

