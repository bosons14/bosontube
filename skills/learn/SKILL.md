---
name: learn
description: Recommend free AI, ML, deep learning, LLM and Gen AI courses and talks on YouTube from the BosonTube catalog, or a learning path for a goal. Use when the user asks what to learn or watch next, for a course, lecture series or roadmap on an AI/ML topic, or runs /bosontube:learn.
argument-hint: "[goal, topic or level]"
allowed-tools: Bash(python3 *)
---

# BosonTube: recommend what to learn

The user wants course or talk recommendations. Their request: $ARGUMENTS

The catalog is a curated set of free YouTube courses and talks (Stanford, MIT, Karpathy, fast.ai, 3Blue1Brown, DeepMind, Berkeley…) with ordered learning paths. Query it with the bundled CLI. Always pass the data directory so the user's own additions and progress are included:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" topics                         # topic keys: math ml dl cv llm genai rl agents
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" paths                          # learning paths with progress
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" search "transformer" --level Beginner --kind course --topic llm
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" path llm-scratch               # one path, step by step, with the next step marked
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" progress                       # what the user has finished
```

## How to answer

1. Work out the goal and the user's level from the request and the conversation. If the request is empty, run `paths` and `progress` and suggest where to go next.
2. Run one or two searches, or open the path that matches the goal. Search terms are ANDed, so prefer short queries or `--topic`.
3. Recommend **from the catalog only**. Give two to five picks, in the order to watch them, each with:
   - the title as a link to its YouTube URL
   - who teaches it, its level, and whether it's a course (playlist) or a single talk
   - one line on why it fits this user's goal, in your own words
4. If a learning path matches, name it and say which step to start at, skipping steps the user has already done (`[x]`).
5. Skip anything already marked done unless the user asks to revisit it.
6. If nothing in the catalog fits, say so plainly. You may suggest a well-known course from your own knowledge, clearly labelled as outside the catalog, and offer to add it with `/bosontube:add-course`.

Keep it short and practical. Mention `/bosontube:path <id>` to follow a path and `/bosontube:open` to browse everything as a web page.
