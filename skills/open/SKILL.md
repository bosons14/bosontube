---
name: open
description: Build the user's personal BosonTube web page - the full AI/ML/Gen AI course catalog plus their own additions, with learning paths, topics and search - as a single HTML file. Use when the user wants to browse BosonTube, see all courses, or runs /bosontube:open.
argument-hint: "[output file]"
allowed-tools: Bash(python3 *)
---

# BosonTube: open the catalog as a web page

Output file requested: $ARGUMENTS (default `bosontube.html` in the current directory)

1. Build the page, which includes the user's own additions:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" build --out "<output file>"
```

2. Try to open it in the user's browser, and ignore any failure: `open` on macOS, `xdg-open` on Linux, `start ""` on Windows.
3. Tell the user where the file is, in one line. It's a single self-contained page that works offline. Videos open on YouTube, and "Mark done" ticks on the page are saved in that browser.

The public version lives at https://github.com/bosons14/bosontube.
