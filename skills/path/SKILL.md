---
name: path
description: Follow a BosonTube learning path step by step and track progress - show the next lecture, mark courses or talks done, or undo. Use when the user asks about their AI/ML learning path or progress, says they finished a BosonTube course or talk, or runs /bosontube:path.
argument-hint: "[path id] | done <item id> | undo <item id>"
allowed-tools: Bash(python3 *)
---

# BosonTube: follow a learning path

Request: $ARGUMENTS

Use the bundled CLI, always with the plugin data directory so progress persists between sessions:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" paths                 # all paths with done counts
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" path <path-id>        # steps, [x] for done, "<- next" on the next one
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" done <item-id> [...]  # mark finished
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" undo <item-id> [...]  # unmark
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bt.py" --data-dir "${CLAUDE_PLUGIN_DATA}" progress              # everything finished so far
```

The built-in paths are `math-first`, `ml-to-dl`, `llm-scratch`, `genai` and `agents`.

## What to do

- **No arguments:** run `paths`. Show each path with its progress, and suggest continuing the one with the most progress that isn't complete. If none are started, ask which goal fits best.
- **A path id (or a name such as "LLM from scratch"):** map it to the id, run `path <id>`, then show:
  - a one-line progress summary (e.g. "3 of 8 done")
  - the next step: title linked to YouTube, teacher, level, and the blurb
  - the remaining steps as a short numbered list
- **"done X" / "I finished X":** find the item id (use `search` if they gave a title), run `done`, then show what's next on the path or paths it belongs to. Confirm briefly.
- **"undo X":** run `undo` and confirm.

Progress is kept in the plugin's data directory on this machine. It is separate from the "Mark done" ticks on the BosonTube web page, which live in the browser.
