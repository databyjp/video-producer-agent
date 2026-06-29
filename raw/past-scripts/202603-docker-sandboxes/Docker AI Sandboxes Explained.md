### Intro

Should you let an AI agent run loose on your machine? 

That’s the question developers everywhere are grappling with. 

The thing is, AI agents are powerful - in all senses of that word. They can get a lot done for you, but they've also been known to get things very wrong. 

[show headlines of things going wrong]
There have been instances of coding agents mistakenly deleting users' files, or exposing user credentials to a malicious actor. 

https://www.ndtv.com/offbeat/i-nearly-had-a-heart-attack-venture-capitalist-after-claude-ai-wipes-15-years-of-family-memories-10969659

https://www.theregister.com/2025/12/01/google_antigravity_wipes_d_drive/

https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/

https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys

And if you have to babysit it like an overeager intern, you're losing half the point of having an agent in the first place.

Docker is tackling this problem with a new product called Docker Sandbox. 
[webpage]

So let's take a look at what it is, how it aims to solve these problems, and the tradeoffs involved in using it.

### Problems being addressed

If you've used coding agents, you've probably seen this problem:
[b-roll - agent asking for permission to do XYZ]
The constant need for attention and permission. 

Agents were supposed to offload work from us. But instead, it's asking us for permission to do anything and everything - from running shell commands, Internet searches or even just reading the contents of a text file. 

So why is it set up to be so tedious? The answer is that you are the circuit breaker from the risks of your agents going rogue. 

In order for agents to be more than just token-spitting LLMs, 
[agent = llm + tools ]

they need to be able to interact with a runtime. And that means agents can typically run arbitrary commands through the shell. But this is a very dangerous game.  

We've seen cases where an agent decides to "start from scratch". 
[ai runs 'rm -rf']
So it runs `rm -rf` on your project, or worse, your root directory.


One small stumble for the agent, one giant heap of pain for the user. 


Second, your agent needs credentials. That means API keys, GitHub tokens, environment variables. A malicious dependency or a prompt injection, and those keys are gone. 

And this isn't hypothetical. In February 2026, researchers found vulnerabilities in Claude Code that could exfiltrate API keys and execute arbitrary code, and OpenClaw's marketplace has hundreds of malicious packages.

All these risks are why permission prompts exist. And also why running AI agents with auto-accept is called: “YOLO” mode. 

All this is also why Docker is building “Sandboxes” specifically for AI agents. 
### What is Docker Sandbox

The main job of a sandbox is to be a protective layer between your agent, and the host machine.

A Docker Sandbox does this by wrapping your AI agent in a virtual machine that is isolated from your host device, and putting together quality of life improvements for using these coding agents.

Now, you might be thinking - wait, Docker already has containers. Why not just run the agent in a container?

It’s a fair question, and it’s actually where Docker Sandbox started. But there are a few reasons why they moved away from this in Docker Desktop four dot fiftyeight onwards.

The first is the kernel. Containers share the host kernel; they just isolate the filesystem and processes on top of it. 

That means any kernel-level exploit inside the container hits your host OS directly. For a web server, that’s an acceptable tradeoff. For an AI agent running arbitrary code? Less so.

The second problem is Docker itself. Coding agents need to do things like docker build, run tests in containers, spin up services with docker compose. 

But if your agent is already inside a container, how does it run Docker commands?

You’ve got two bad options. 

The first is Docker-in-Docker, which runs the container in privileged mode. This unfortunately tears down the isolation you were trying to create in the first place. 

The second option is to mount the Docker socket from the host. This gives the agent direct access to every container and volume on your machine. That’s arguably worse.

As a result, Docker went with virtual machines, or VMs. 

A VM gives you deeper levels of isolation than containers, by owning its own entire operating system on virtualised hardware.

Think Parallels or VMware running Windows on your Mac. A piece of software called a hypervisor acts as the middleman between the guest OS and the real hardware. 

Your host OS and everything on it is fully insulated from anything that happens inside the guest. That's why Docker chose VMs for the Sandbox. 

Of course, that isolation isn't free. A VM requires a full OS - hardware resources, networking, package managers, all of it. 

Even Docker's "microVM" requires gigabytes of RAM. Which is ironic. VMs being resource-hungry is exactly why Docker containers became so popular in the first place. 

In the age of AI, everything old is new again.

That's the core architecture of the Docker Sandbox. Now, what's it like to use Docker Sandbox? Let's take a look at the practical side, through the developer experience and the tooling. 
### What Docker Sandbox Does: The Differentiators

Let's start with what the VM architecture means for your for coding agents. 

Inside each Docker Sandbox, is a completely private Docker daemon. Your agent can build, run, and delete Docker containers completely separate from your host Docker environment. 

That means your agent can run code for validation, debugging or testing, or even spin up its own tooling as needed, without any risk to your host device. 

Now, the agentic tooling. Two things stand out here. 

First, file sync. Docker uses bidirectional file sync for files in your working directory, preserving your absolute paths. 

That means everything matches your host, whether it comes to relationships between files; or outputs like stack traces or error messages. No mental translation needed.

Second, credential injection. Remember how we talked about API keys and credentials being a risk? 

Docker Sandbox uses a proxy to inject your credentials into outbound API requests on the fly. 

The agent never sees the actual tokens. So even if the sandbox is compromised, your credentials can't be stolen, because they were never in the sandbox. 

Another cool thing about the architecture is that the VM is built from a Dockerfile.

You can customize the agent's tooling by creating your own Dockerfile. And if the agent doesn't know use those tools, extend their knowledge through frameworks like Agent Skills.

For example, you could add Playwright CLI to the Dockerfile as a headless browser, then add Microsoft's official `playwright-cli` skill in the project directory to teach the agent how to actually drive it.

You can also set network policies to let you control exactly which domains the agent can reach. I could for example only include my Serverless Elastic project domain to the allowlist, and not let my agent touch any other part of the Internet. 

### Docker Sandbox: Quick Demo

Let me show you what the user experience looks like in practice.

[Pause video, record scratch noise & popup a new instance of me]
Hey - future JP here. Since we recorded this video last week in late March, Docker's released Docker Sandbox as a standalone CLI tool called `sbx`. 

What you'll see past JP [point to side] use here is the Sandbox tool that comes with Docker Desktop. 

Slightly different syntax, but basically the same tool, so all the key concepts still apply. 

Both tools are available, so anywhere you see me type `docker sandbox`, you could use `sbx` as an alternative.

Okay then - back to you, past JP.
[End of insert]

Running Docker Sandbox is just one command like this: `docker sandbox run claude ~/my-project`

And you'll see that we've booted directly into the agent's interface - in this case Claude Code. This is now running in the VM, not on your host machine. 

[screen recording — docker sandbox run claude ~/my-project]

Let's get it to run a task - [some task; tbd]

[Create a simple app in Python to download an RSS feed into Markdown. Include tests & make sure it runs.]

You can see the agent's working here; let's leave it to do its thing.

Meanwhile, if I open a new terminal tab and run `docker ps` on my host nothing. The sandbox doesn't show up. But `docker sandbox ls` -> there it is. Completely separate management plane.

And if I want to see what the agent's been doing on the network, `docker sandbox network log` gives me a full breakdown of every request; what was allowed, what was blocked. 

When we go back, we see it's done a bunch of things - installed dependencies, built the project, and even run some tests. 

I've been using Docker Sandbox quite a bit in my personal workflow for a few weeks now. 

And I've really enjoyed the fact that I can trust it to work away, without it running around and smashing up parts of my computer. 

The lack of unnecessary context switching has helped me focus a lot more on my other work. 
### The Honest Tradeoffs

So far, I've talked about how great Docker Sandbox is - but it's not without its drawbacks. 

The biggest one is just the resource overhead. While a lightweight container would use tens of megabytes of disk, I've found that even a fresh Sandbox would use five to six gigabytes. 

Also, each Sandbox is assigned four gigabytes of memory, with about one gigabyte being used by the sandbox itself. 

So if you're one of *those* people - and you know who I mean - running a gaggle of agents in parallel, it's going to eat through your system resources pretty quickly. 

You should consider which agents need the extra guardrails and only run those in the sandbox.

The memory limit is a tough one. Currently, as of March 2026, the four gigabyte limit is hardcoded. If you need more than that, it's just not possible at the moment. 

[add screenshot(s)]
But there are a number of GitHub issues requesting for this to be changed, so hopefully this would be changed. 

Platform support is another potential sticking point. Me, I'm happy because macOS on Apple Silicon gets the full microVM experience. 

But if you're on Windows - support is labelled experimental; in other words - use at your own risk. And Linux users still get container-based sandboxes, which, as we talked about, means weaker isolation.

There are also some side effects of using a separate VM. Adding a persistent environment variable requires you to stop the sandbox, delete it, and recreate it from scratch. 

This means losing your entire agent conversation unless you somehow manually back it up and restore it. 

The Arcade.dev team called this "a steep penalty for a small configuration mistake" in their blog and they probably have a point. 

Also, I've talked a lot about isolation and protection here - but you **need** to know that Docker Sandbox doesn't protect your project files. Your workspace is still fully writable inside the sandbox. It has to be, otherwise the agent couldn't do its job. 

It means the agent can still delete your codebase, and eat your work. The sandbox protects your system, but your project is still vulnerable to the agent. So keep committing your work, and keep pushing it to a safe place.

### Bigger Picture & Wrap-up

Docker Sandbox isn't the only game in town. A cursory search will show other providers building sandboxes, on the cloud, or building them as a part of agents and frameworks. As with all things AI, the space is moving fast.

But Docker does have a few key advantages. 

It's local, and it gives you a full Docker daemon inside the sandbox. Plus, it comes with Docker Desktop - so if you have access to that, like millions of developers, you already have access to it. 

And they seem to be investing in the agent ecosystem pretty seriously. They are also building out an MCP catalog and toolkit, and partnering with others for cloud sandboxes. It seems like they're building a platform, not just a feature.

I think sandbox infrastructure for AI agents is becoming as essential as container orchestration was a decade ago. 

The question isn't "should we sandbox our agents". It's "how quickly can we sandbox everything?", and "what's the right sandbox architecture for this agent"? 

Docker Sandbox is a very accessible on-ramp, with serious isolation. It's free if you have Docker Desktop, it's easy to set up and use and customisable. 

The main concerns are the resource use - both how heavy it is, and the current lack of ability to assign more RAM to it. 

But these are minor, and in the case of memory, probably temporary. 

Look, I've only been using Docker Sandbox for a short while, and I'm very excited. 

I'm actually going to be playing in the sandbox a lot more in the near future. 

One thing that I'm really excited to do is to use it with Elastic's new Agent Skills. This tooling is going to help me push automation of Elastic’s workflow to see what is possible. 

I might do a video later on about how these experiments turn out. 

I'd also love to hear about **your** preferred isolation strategy for your coding agent. Are you like me, and find Docker Sandbox a good solution for your use case? If not, why, and what else do you use? Let me know in the comments.

That's it for me. Thanks for watching; remember to like, subscribe, and tell your friends and pets! See you next time.



(source: https://www.arcade.dev/blog/using-docker-sandboxes-with-claude-code/) 