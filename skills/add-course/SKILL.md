---
name: add-course
description: Add a YouTube course, playlist or talk on AI, ML or Gen AI to the user's personal BosonTube catalog. Use when the user shares a YouTube link and asks to add or save it to BosonTube, or runs /bosontube:add-course.
argument-hint: "<YouTube URL> [notes]"
allowed-tools: Bash(python3 *), WebFetch, WebSearch
---

# BosonTube: add a course

Request: $ARGUMENTS

## Steps

1. **Get the URL.** It must be a `youtube.com` or `youtu.be` link: a playlist (`list=`) means `--kind course`, a single video means `--kind talk`. If there's no URL, ask for one.
2. **Look up the facts.** Use WebFetch on the URL, or WebSearch with the URL or title if fetching fails, to find the title, the teacher or speaker, the channel or institution, and the year. Never invent these. If something can't be confirmed, ask the user.
3. **Classify it** using these values:
   - `--topic`: one of `math ml dl cv llm genai rl agents`
   - `--level`: `Beginner`, `Intermediate` or `Advanced`
   - `--blurb`: one or two sentences in your own words on what it covers and who it's for. Don't copy the video description.
   - optional `--code`: a short label for the card, such as `CS336`, `GPT` or `RL`
4. **Check for duplicates:** run `search` with a key word from the title.
5. **Add it:**

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" add \
  --url "<url>" --title "<title>" --by "<teacher>" --org "<channel or institution>" \
  --kind course|talk --topic <topic> --level <level> --year <yyyy> \
  --blurb "<your one-line summary>" [--code <label>]
```

6. Confirm in one or two lines what was added and how you classified it. Mention that `/bosontube:open` rebuilds the web page with it included.

To remove one of the user's own additions: `... remove <id>`. Built-in catalog entries can't be removed this way.

**Working inside the bosontube repo itself?** If the current project is the BosonTube repository (it has `courses.json` and `build.py` at its root) and the user wants the course in the **public** catalog, edit `courses.json` directly in the same item format, then run `python3 build.py` to validate it and rebuild `index.html`.
