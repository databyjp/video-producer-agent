/Users/jphwang/code/content/202603-rag-on-a-budget

Title: “Good, local vision RAG on an 8GB device?”
Short title: “Vision RAG on 8GB machine?”
Beats:
	1.	Hook — “Can you run a RAG pipeline that actually reads charts and tables… on an 8GB machine?” Show it answering a question about a Stack Overflow survey chart. Show the RAM usage.
	2.	Problem — PDFs are full of charts, tables, diagrams. Normal RAG is blind to them. You need vision. But vision models are big — or are they?
	3.	The budget — Introduce the models: Qwen 3.5 VLM 0.5B to build a searchable index of visual content, Elastic embedding model at 230M for retrieval. 730M parameters for ingestion.
	4.	Preprocessing — Feed the janky Stack Overflow survey PDF page by page to the 0.5B VLM. Show the descriptions it generates for charts and tables. Audience can verify — they know this data.
	5.	Retrieval — Embed the descriptions, query, show it finding the right pages. Works.
	6.	Generation — first attempt — Pass the retrieved page images + query to the 0.5B VLM for answering. Some queries work. Push it — show where it breaks.
	7.	The fix — Swap in Qwen 3.5 2B for generation. Feed it the actual page images. Still fits on 8GB. Quality jumps.
	8.	The insight — The 0.5B model builds the index, the 2B model does the reasoning. Spend your parameters where it matters.
	9.	Wrap — “You don’t need a giant model. You need the right small models in the right seats.“​​​​​​​​​​​​​​​​