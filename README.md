# BosonTube

A calm, hand-picked home for the best free **AI, ML and Gen AI courses and talks on YouTube**, with ordered **learning paths**. Inspired by Andrej Karpathy's [HackerTube](https://hackertube.org).

No algorithm, no account, no tracking. It works as a static web page and as a Claude Code plugin. On the page, videos open on YouTube, and your "done" ticks stay in your own browser.

## What's inside

- **34 courses and talks**: Stanford (CS229, CS224N, CS231n, CS336, CS236, CS25, CME295…), MIT (6.S191, 18.06), Karpathy (Zero to Hero, Let's build GPT, GPT-2 reproduction), fast.ai, 3Blue1Brown, StatQuest, DeepMind × UCL, David Silver's RL, Berkeley CS285 and the LLM Agents MOOC, and more
- **5 learning paths**: Math for ML · Classic ML to deep learning · Build an LLM from scratch · Generative AI in depth · RL & AI agents
- **Browse** by topic, course vs. talk and "must-watch", plus search (press `/`)
- **Progress**: tick off steps in a path. This is saved in your browser's localStorage.

## Claude Code plugin

BosonTube is also a Claude Code plugin, so you can ask Claude what to learn next without leaving your terminal.

**Install** (Claude Code 2.1.275 or later):

```
/plugin install bosontube --marketplace bosons14/bosontube
```

On older versions:

```
/plugin marketplace add bosons14/bosontube
/plugin install bosontube@bosontube
```

**Skills**

| Command | What it does |
| :- | :- |
| `/bosontube:learn [goal]` | Recommends courses and talks from the catalog for your goal and level, in watch order |
| `/bosontube:path [id]` | Shows a learning path, your progress and the next lecture. `done <id>` / `undo <id>` track progress |
| `/bosontube:add-course <YouTube URL>` | Looks up a course or talk, classifies it and adds it to your personal catalog |
| `/bosontube:open [file]` | Builds your personal BosonTube page (catalog plus your additions) and opens it |

You don't always need the slash command: asking "what should I watch to learn diffusion models?" or "I finished Zero to Hero" brings the right skill in on its own.

Your progress and your own courses are stored in the plugin's data folder (`~/.claude/plugins/data/…`), so they survive plugin updates. The same CLI also works on its own:

```bash
python3 scripts/bt.py search "transformer" --level Beginner
python3 scripts/bt.py path llm-scratch
python3 scripts/bt.py done build-gpt
python3 scripts/bt.py build --out bosontube.html
```

Without the plugin, data goes to `~/.bosontube` (or `--data-dir`).

## Run the website

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
