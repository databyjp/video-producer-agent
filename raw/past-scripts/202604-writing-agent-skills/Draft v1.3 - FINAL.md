Let's talk Agent skills. You probably know this, but skills are portable, on-demand extensions for AI agents. It’s the equivalent of Neo from The Matrix downloading Kung Fu directly into the brain, without the inconvenience of plunging a footlong spike into it. 

Skills have been incredibly popular due to their simplicity and their economic token use. 

But, this research on software engineering skills found that four out of five agent skills yielded zero improvement over not using a skill at all. [SWE-Skills-bench "finding 1"]

In fact, some skills are more banana peel than power-up mushroom, making the agent even worse than the baseline. [SWE-skills-bench "finding 4" / SkillBench 4.2.2 table + "while comprehensive Skills actually hurt performance"] It's like if Neo's new skill hadn't improved his fighting, but given him balance problems or caused him to directly punch himself repeatedly in the face.  [stick figure Neo falling over / punching self in face]

Having said that, some skills are incredibly powerful. One paper found that a small model with the right skill can beat a frontier model without one [SkillsBench finding 7], which has pretty big cost implications.

So what separates a skill that actually boosts performance from one that just clutters the context window? We'll talk about exactly that, and how you can write better skills in the video.

[pause/slide/cut]

Let's start by discussing why skills exist, which is to extend generative models. 

Yes, these models know a lot. But even the best ones can’t know everything. Nothing can - it’s just not how knowledge works. 

First of all, models can’t get access to every piece of private information in the world, like my private diary entry from 1999 anointing The Phantom Menace to be the best movie ever. And second, knowledge changes over time, like how we now know The Phantom Menace to be only the second best movie ever, right behind Morbius.

But instead of admitting uncertainty, models still hallucinate with the energy of a random Redditor arguing with a Nobel laureate. [stick figure with Reddit logo? vs another stick figure with Nobel prize in hand]

In agent form, where models are given tools to interact with the world, this means that an agent can happily delete your work or production database, while explaining, in great, excruciating detail, exactly why that was the right call. At least right before they turn around and profusely apologise for their mistake. [screenshot of articles, with models following this sequence]

One obvious solution is to stuff the agent with everything it **might** need - whether it be a long prompt, tools, or MCPs. But unfortunately, more context isn't free. Sure, context windows are getting larger, but every token you add competes with the actual task, and researchers have found that unnecessary context actively degrades performance.

This is why Anthropic built Agent Skills [skills announcement] as an open standard. 

What makes skills different from other solutions is the idea of "**progressive disclosure**". [screenshots from https://agentskills.io/what-are-skills, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://learn.microsoft.com/en-us/agent-framework/agents/skills)

Skills allow you to organise the information that it might or, importantly, might *not* need into packages, which can be then loaded only as needed. 

For an agent, this means a far more efficient, focussed use of its context window. And for the user, faster inference, lower compute and better results.

All these benefits, and the fact that skills are just text files led to rapid, broad adoption, leading to a huge range of public skills to choose from [screenshots of repos like https://github.com/VoltAgent/awesome-agent-skills, https://github.com/anthropics/skills, https://github.com/elastic/agent-skills, https://github.com/heilcheng/awesome-agent-skills]. This also meant researchers were able to dig in and evaluate skills in detail. 

The resulting benchmarks - SkillsBench and SWE-Skills-Bench - converge on these findings. 
One: longer skills generally perform poorly, when compared to focussed, concise skills. [Skillsbench, Table 6, https://agentskills.io/skill-creation/best-practices: Aim for moderate detail] 
Two: narrow, specialised skills that fill real knowledge gaps help the most - like those that relate to concrete procedures, or domain-specific ones [Skillsbench 5 "Skills close procedural gaps", SWE-skillsbench "These results establish that SWE skill utility is highly domain-specific and context-dependent"]. 
Three, a smaller model like Anthropic Haiku, with a well-written skill, can beat a frontier model like Opus with none. [SkillsBench finding 7]

Let's spend a minute on that one, because it's a big deal for your bottom line.

If you don't know, Haiku is the smallest model in Anthropic's product suite. 

Smaller models like Haiku are cheaper and faster, but they’re also less capable. Think of it like a fast-food line cook versus a Michelin-starred chef. [stock images of cook vs chef]

But under the right circumstances, the line cook can provide great value. 

For example, if you give that line cook the exact recipe and the right equipment [same cook in kitchen], they'll outperform a chef cooking blind in a tent [same chef - in empty tent]. That’s exactly what researchers found: Haiku with well-written skills outperformed Opus on some specific tasks. [SkillsBench finding 7]

This is a big finding, given the cost differences between a frontier model and a smaller one, and even the possibility of running local models. It's a reminder that you don't always need the latest, or the biggest model. Size does matter, but you know, it's not everything.

So far, we've talked about the impact of good skills. In other words, the kung-fu kind of useful skill that elevates the agent, not the detrimental kind that might cause the agent to punch itself in the face. [same image of Neo stick figure]

What makes something a good skill? The research gives us good guidance on this. Let's start with the part that might matter the most - triggering.

Remember that skills rely on progressive disclosure. This means that an agent must actively choose to read the skill to make use of it. 

Since an agent can only see the skill description and title to make this choice, a skill with a poorly written description is unlikely to trigger at the right time. You know, much like how you wouldn't have clicked on this video if we had called it "JP stares blankly into the void for an hour". [fake thumbnail]

With a poor description, the skill won't be loaded at the agent's time of need. Worse, it might be loaded for the *wrong* job - like how if you **did** want to watch me stare blankly at the screen for an hour, you'd be very disappointed at this video right now.

The recommendations for skill descriptions are to keep it short but specific, and name concrete trigger scenarios. [https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#writing-effective-descriptions, https://agentskills.io/skill-creation/optimizing-descriptions#should-trigger-queries]

So don't write cryptic descriptions like: "Helps with documents" which could both trigger on everything, or trigger on nothing, depending on what the agent feels like. 

Instead, write something more specific and precise, like: 

> "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). ..." [https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md]

You can read this and concretely tell whether something is in or out. That means the agent can trigger it at the right time, and ONLY at the right time.

Once you've got the skill to trigger, then you can worry about making the contents useful without being excessive. 

Progressive disclosure isn't just limited to the idea of "will this skill trigger". The skill package can have multiple documents [https://agentskills.io/specification#directory-structure], with the body referring to additional references. And this kind of nested structure is helpful, because of the finding that excessive length isn't helpful. The recommendation is to keep main SKILL.md to a max. length of 500 lines or so. [https://agentskills.io/specification#progressive-disclosure, https://learn.microsoft.com/en-us/agent-framework/agents/skills?pivots=programming-language-csharp#skillmd-format]

Note that this doesn't put a limit on the total amount of information, because of the ability to refer to more files. For example, Elastic's own kibana dashboards skill comes with over a dozen additional files, including Javascript code, API references, and example JSON files. [overlay https://github.com/elastic/agent-skills/blob/main/skills/kibana/kibana-dashboards/SKILL.md and other files]

It's just like a choose-your-own-adventure book, if perhaps the adventure was the wonderful journey of vibe-coding. [fake book cover - Alice is vibe-coding?]

In other words, only include the required information for the job. Before writing any line, ask yourself: "Would the agent screw this up without being told?" Don't explain the obvious, like what a database is. Definitely don't write "follow best practices". That's not guidance, that's a fortune cookie.

What you *should* write is the stuff specific to your context that prevents failures. Here are some examples in Anthropic's own skills creator skill:

\[show lines:\]  
"Save this \[timing\] data immediately to \`timing.json\` in the run directory... **This is the only opportunity to capture this data**"  
"The grading.json expectations array must use the fields \`text\`, \`passed\`, and \`evidence\` (not \`name\`/\`met\`/\`details\` or other variants)" 
[https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md]

Look at the specificity here. You can almost **feel** the original errors that inspired these lines when they tried to do the job before they wrote these skills. Write these skills with the energy of Old Biff from Back to the Future, passing on his wisdom to young Biff.

And here’s a surprising one: in one study, skills with executable code examples tripled the pass rates of not having skills [SkillsBench_paper, pass rate to 45.5%]. Even in the age of vibe-coding, the vibes vibe better when they're less vibes and more code. Another reminder that where specificity is available, you should use it.

Speaking of specificity, this applies to versions and software libraries. Version-mismatched skills were a notable failure mode that made agents worse. [SWE_SkillsBench_paper] So, don't write "React project", if you can write "React 18 with TypeScript and Vite" instead.

Quick recap on skill writing - tight descriptions, compact structure, concrete code examples, and exact versioning. Master those, and you'll be closer to a skill that actually triggers and delivers. 

Let me show you what this looks like in practice. I've been using a skill for ES|QL query generation [https://github.com/elastic/agent-skills/blob/main/skills/elasticsearch/elasticsearch-esql/SKILL.md] - that's Elastic's newer query language. It's a textbook case for a skill: ES|QL is new enough that models don't have deep training data on it. 

And the name is similar enough to older Elastic query DSL or SQL that models confidently write the wrong thing. 

Without the skill, this model mixes up ES|QL with other languages - wrong commands, invented functions. With it loaded, the model writes fluent, correct ES|QL. That's the line cook with the recipe, right there, vs the confused chef without proper instructions and tools.
[screen: side-by-side of agent with and without the skill]

So how do you prove that a skill is actually helpful, and not punching your agent in the face? Let's say you've written a skill for logging data into your preferred observability stack, like Elasticsearch.

Step one - compare the outputs: take five or ten real tasks, run them with and without the skill, and compare the outputs. The results are your quality signal, like whether the apps were correctly wired, and whether the outputs were parsed correctly. [sidebar with summaries]

Step two - check if it's even triggering. Throw twenty different prompts at your agent, some logging-related, some not - and record the results. If it's triggering on "research this problem", or "write the README" your description needs work. If it's _not_ triggering on "set up logging for this AI agent", it needs work. [sidebar with summaries]

Now here's something that I found really interesting. Apparently, LLM-generated skills are generally not helpful at all. [SkillsBench Finding 3] 

And if you think about it, it kind of makes intuitive sense. Skills work because they encode expertise the model doesn't have. Asking a model to generate its own skill is like getting a new grad to write their own onboarding. At best, it's going to be a lot of things they already know, and at worst, they'll pass on incorrect info to the next person. 

What you should do instead is to start from real work, and write skills for patterns of errors that you observe. It might even be a good idea to write the evaluation tasks first, with the aim of improving the scores over time with a skill. 

It's also good practice to periodically evaluate these skills over time. Models and harnesses will get better, and your preferences will change. 

And you don't always have to start from scratch, either. There's already a huge ecosystem of skills out there to choose from. [show skills repos once again - maybe with links]

As we mentioned, skills are just text files at the end of the day, so they are relatively easy to build and iterate on. 

I've been writing my own skills, too. I'm working on skills to help me generate visual explainers, or plan tutorials, although I've yet to find a skill for outsourcing my job to an agent so I can go and play video games.

You know, I'd love to hear about **your** favourite skills, whether you wrote them yourself, or if it's a public skill. And also, tell us about your experience creating your own skills - what principles or tips do you find useful, and maybe which ones you don't find so useful. You can chime in in the comments below, which happens to be below the like button!

That's it for me. Links to the resources are in the description. Drop your favourite skills in the comments, and I’ll see you next time.

\----- References (for description) \-----  
\[SkillsBench\_paper\] https://arxiv.org/pdf/2602.12670  
\[SWE\_SkillsBench\_paper\] https://arxiv.org/pdf/2603.15401  
\[Skills\_announcement\] https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard  
\[Anthropic skills guide\] https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf  
\[Skill creation \- best practices\] https://agentskills.io/skill-creation/best-practices  
\[8 tips for writing agent skills\] https://www.philschmid.de/agent-skills-tips
https://learn.microsoft.com/en-us/agent-framework/agents/skills
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices