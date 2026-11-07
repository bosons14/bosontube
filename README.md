# BosonTube

A calm, hand-picked home for the best free **AI, ML and Gen AI courses and talks on YouTube**, with ordered **learning paths**. Inspired by Andrej Karpathy's [HackerTube](https://hackertube.org).

No algorithm, no account, no tracking. It's one static page: videos open on YouTube, and your "done" ticks stay in your own browser.

## What's inside

- **34 courses and talks**: Stanford (CS229, CS224N, CS231n, CS336, CS236, CS25, CME295…), MIT (6.S191, 18.06), Karpathy (Zero to Hero, Let's build GPT, GPT-2 reproduction), fast.ai, 3Blue1Brown, StatQuest, DeepMind × UCL, David Silver's RL, Berkeley CS285 and the LLM Agents MOOC, and more
- **5 learning paths**: Math for ML · Classic ML to deep learning · Build an LLM from scratch · Generative AI in depth · RL & AI agents
- **Browse** by topic, course vs. talk and "must-watch", plus search (press `/`)
- **Progress**: tick off steps in a path. This is saved in your browser's localStorage.

## Run it

It's a single HTML file, so you can just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Add or edit courses

All content lives in `courses.json`. After editing it, rebuild:

```bash
python3 build.py   # checks the data and writes index.html
```

Each item looks like this:

```json
{
  "id": "cs336", "code": "CS336",
  "title": "Stanford CS336: Language Modeling from Scratch",
  "by": "Percy Liang & Tatsunori Hashimoto", "org": "Stanford Online",
  "kind": "course",            // "course" (playlist) or "talk" (single video)
  "topic": "llm",              // one of the keys in "topics"
  "level": "Advanced",         // Beginner | Intermediate | Advanced
  "year": 2025,
  "url": "https://www.youtube.com/playlist?list=...",
  "vid": "optional YouTube video id, used for the thumbnail",
  "pick": true,                // optional: show the "Must-watch" badge
  "blurb": "One or two sentences in your own words."
}
```

A learning path is just an ordered list of item ids under `"paths"`.

## Deploy

It's static, so any static host works:

- **GitHub Pages**: push to a repo, then Settings → Pages → deploy from `main` / root.
- **Netlify / Cloudflare Pages / Vercel**: drag and drop the folder. There's no build step, because `index.html` is already built.
- **Your own server**: copy `index.html` anywhere nginx or Caddy can serve it.

When it runs on a normal host, cards with a `vid` show the real YouTube thumbnail. Elsewhere they fall back to a coloured title card.

## Notes

- The "Must-watch" badge is my own curation. It is not pulled from HackerTube's or Hacker News' data.
- Links point to the public YouTube playlists or videos. If a course is re-uploaded, update its `url` in `courses.json`.

## Ideas for later

- Import Karpathy's HackerTube data export and add every AI/ML video it lists
- A small script with the YouTube Data API to pull lecture counts, durations and new course editions
- Embedded player and per-lecture progress inside playlists

MIT licensed. All videos belong to their creators.
