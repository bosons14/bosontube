#!/usr/bin/env python3
"""BosonTube CLI: search the catalog, follow learning paths, track progress,
add your own courses and build your personal BosonTube page.

Used by the BosonTube Claude Code plugin, but works on its own too:

  python3 scripts/bt.py search "transformers" --level Beginner
  python3 scripts/bt.py paths
  python3 scripts/bt.py path llm-scratch
  python3 scripts/bt.py done build-gpt
  python3 scripts/bt.py add --url URL --title T --by B --org O --kind course \
                            --topic llm --level Intermediate --year 2025 --blurb "..."
  python3 scripts/bt.py build --out ./bosontube.html

The built-in catalog is courses.json next to this repo's root. Your progress
and personal additions are kept in a data directory (--data-dir, the
BOSONTUBE_DATA environment variable, or ~/.bosontube), never in the catalog.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEVELS = ["Beginner", "Intermediate", "Advanced"]


def data_dir(args):
    d = Path(args.data_dir or os.environ.get("BOSONTUBE_DATA") or Path.home() / ".bosontube")
    d.mkdir(parents=True, exist_ok=True)
    return d


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def write_json(path, obj):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def catalog(args):
    """Built-in catalog merged with the user's own additions."""
    base = read_json(ROOT / "courses.json", None)
    if base is None:
        sys.exit(f"catalog not found at {ROOT / 'courses.json'}")
    mine = read_json(data_dir(args) / "my-courses.json", {"items": []})
    ids = {i["id"] for i in base["items"]}
    for it in mine.get("items", []):
        if it["id"] not in ids:
            base["items"].append(dict(it, mine=True))
    return base


def progress(args):
    return read_json(data_dir(args) / "progress.json", {"done": []})


def line(it, done=False, topics=None):
    tick = "[x]" if done else "[ ]"
    topic = topics[it["topic"]]["label"] if topics else it["topic"]
    star = " ★" if it.get("pick") else ""
    mine = " (yours)" if it.get("mine") else ""
    return (f"{tick} {it['id']}: {it['title']}{star}{mine}\n"
            f"    {it['by']} · {it['org']} · {topic} · {it['level']} · {it['kind']} · {it['year']}\n"
            f"    {it['url']}\n    {it['blurb']}")


def cmd_search(args):
    cat, done = catalog(args), set(progress(args)["done"])
    q = (args.query or "").lower()
    hits = []
    for it in cat["items"]:
        hay = " ".join([it["title"], it["by"], it["org"], it["code"], it["blurb"],
                        cat["topics"][it["topic"]]["label"], it["topic"]]).lower()
        if q and not all(w in hay for w in q.split()):
            continue
        if args.topic and it["topic"] != args.topic:
            continue
        if args.level and it["level"].lower() != args.level.lower():
            continue
        if args.kind and it["kind"] != args.kind:
            continue
        hits.append(it)
    hits.sort(key=lambda i: (not i.get("pick"), LEVELS.index(i["level"]), -i["year"]))
    print(f"{len(hits)} match(es)")
    for it in hits[: args.limit]:
        print(line(it, it["id"] in done, cat["topics"]))


def cmd_topics(args):
    cat = catalog(args)
    for k, t in cat["topics"].items():
        n = sum(1 for i in cat["items"] if i["topic"] == k)
        print(f"{k}: {t['label']} ({n})")


def cmd_paths(args):
    cat, done = catalog(args), set(progress(args)["done"])
    for p in cat["paths"]:
        n = sum(1 for s in p["steps"] if s in done)
        print(f"{p['id']}: {p['title']} [{p['level']}] {n}/{len(p['steps'])} done\n    {p['desc']}")


def cmd_path(args):
    cat, done = catalog(args), set(progress(args)["done"])
    p = next((p for p in cat["paths"] if p["id"] == args.id), None)
    if not p:
        sys.exit(f"no path '{args.id}'. Known: {', '.join(x['id'] for x in cat['paths'])}")
    by = {i["id"]: i for i in cat["items"]}
    n = sum(1 for s in p["steps"] if s in done)
    print(f"{p['title']} [{p['level']}]: {n}/{len(p['steps'])} done\n{p['desc']}\n")
    nxt = next((s for s in p["steps"] if s not in done), None)
    for i, s in enumerate(p["steps"], 1):
        first, rest = line(by[s], s in done, cat["topics"]).split("\n", 1)
        mark = "   <- next" if s == nxt else ""
        print(f"{i}. {first}{mark}\n{rest}")
    if nxt is None:
        print("\nPath complete.")


def set_done(args, value):
    cat = catalog(args)
    ids = {i["id"] for i in cat["items"]}
    prog = progress(args)
    done = set(prog["done"])
    for i in args.ids:
        if i not in ids:
            sys.exit(f"unknown id '{i}'")
        (done.add if value else done.discard)(i)
    prog["done"] = sorted(done)
    write_json(data_dir(args) / "progress.json", prog)
    print(("marked done: " if value else "unmarked: ") + ", ".join(args.ids))


def cmd_progress(args):
    cat, done = catalog(args), set(progress(args)["done"])
    by = {i["id"]: i for i in cat["items"]}
    print(f"{len(done)} of {len(cat['items'])} finished")
    for i in sorted(done):
        if i in by:
            print(f"  [x] {i}: {by[i]['title']}")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


def cmd_add(args):
    cat = catalog(args)
    if args.topic not in cat["topics"]:
        sys.exit(f"topic must be one of: {', '.join(cat['topics'])}")
    if args.level not in LEVELS:
        sys.exit(f"level must be one of: {', '.join(LEVELS)}")
    if not re.match(r"^https://(www\.)?(youtube\.com|youtu\.be)/", args.url):
        sys.exit("url must be a YouTube link (https://www.youtube.com/... or https://youtu.be/...)")
    vid = args.vid
    if not vid:
        m = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", args.url)
        vid = m.group(1) if m else None
    item = {
        "id": args.id or slug(args.title), "code": args.code or slug(args.title)[:8].upper(),
        "title": args.title, "by": args.by, "org": args.org or args.by, "kind": args.kind,
        "topic": args.topic, "level": args.level, "year": args.year, "url": args.url,
        "blurb": args.blurb,
    }
    if vid:
        item["vid"] = vid
    if any(i["id"] == item["id"] for i in cat["items"]):
        sys.exit(f"id '{item['id']}' already exists; pass --id to choose another")
    if any(i["url"] == item["url"] for i in cat["items"]):
        sys.exit("that URL is already in the catalog")
    path = data_dir(args) / "my-courses.json"
    mine = read_json(path, {"items": []})
    mine["items"].append(item)
    write_json(path, mine)
    print(f"added '{item['id']}' to {path}")


def cmd_remove(args):
    path = data_dir(args) / "my-courses.json"
    mine = read_json(path, {"items": []})
    before = len(mine["items"])
    mine["items"] = [i for i in mine["items"] if i["id"] != args.id]
    if len(mine["items"]) == before:
        sys.exit(f"'{args.id}' is not one of your additions (built-in courses can't be removed here)")
    write_json(path, mine)
    print(f"removed '{args.id}'")


def cmd_build(args):
    cat = catalog(args)
    for it in cat["items"]:
        it.pop("mine", None)
    blob = json.dumps(cat, ensure_ascii=False).replace("</", "<\\/")
    html = (ROOT / "template.html").read_text(encoding="utf-8").replace("/*__DATA__*/null", blob)
    out = Path(args.out).expanduser().resolve()
    out.write_text(html, encoding="utf-8")
    print(f"built {out} ({len(cat['items'])} items, {len(cat['paths'])} paths)")


def main():
    ap = argparse.ArgumentParser(description="BosonTube CLI")
    ap.add_argument("--data-dir", help="where progress and your own courses are stored")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search"); s.add_argument("query", nargs="?")
    s.add_argument("--topic"); s.add_argument("--level"); s.add_argument("--kind", choices=["course", "talk"])
    s.add_argument("--limit", type=int, default=12); s.set_defaults(f=cmd_search)
    sub.add_parser("topics").set_defaults(f=cmd_topics)
    sub.add_parser("paths").set_defaults(f=cmd_paths)
    s = sub.add_parser("path"); s.add_argument("id"); s.set_defaults(f=cmd_path)
    s = sub.add_parser("done"); s.add_argument("ids", nargs="+"); s.set_defaults(f=lambda a: set_done(a, True))
    s = sub.add_parser("undo"); s.add_argument("ids", nargs="+"); s.set_defaults(f=lambda a: set_done(a, False))
    sub.add_parser("progress").set_defaults(f=cmd_progress)
    s = sub.add_parser("add")
    for k in ["url", "title", "by", "blurb"]:
        s.add_argument("--" + k, required=True)
    s.add_argument("--kind", choices=["course", "talk"], required=True)
    s.add_argument("--topic", required=True); s.add_argument("--level", required=True)
    s.add_argument("--year", type=int, required=True)
    s.add_argument("--org"); s.add_argument("--id"); s.add_argument("--code"); s.add_argument("--vid")
    s.set_defaults(f=cmd_add)
    s = sub.add_parser("remove"); s.add_argument("id"); s.set_defaults(f=cmd_remove)
    s = sub.add_parser("build"); s.add_argument("--out", default="bosontube.html"); s.set_defaults(f=cmd_build)

    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
