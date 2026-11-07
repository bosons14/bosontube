#!/usr/bin/env python3
"""Build index.html from template.html + courses.json.

Usage:  python3 build.py
Edit courses.json to add or change courses, then rebuild.
"""
import json
from pathlib import Path

root = Path(__file__).parent
data = json.loads((root / "courses.json").read_text(encoding="utf-8"))

ids = {i["id"] for i in data["items"]}
assert len(ids) == len(data["items"]), "duplicate item id in courses.json"
for item in data["items"]:
    assert item["topic"] in data["topics"], f"{item['id']}: unknown topic {item['topic']}"
    assert item["kind"] in ("course", "talk"), f"{item['id']}: kind must be course or talk"
for path in data["paths"]:
    missing = [s for s in path["steps"] if s not in ids]
    assert not missing, f"path {path['id']} refers to unknown items: {missing}"

blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = (root / "template.html").read_text(encoding="utf-8").replace("/*__DATA__*/null", blob)
(root / "index.html").write_text(html, encoding="utf-8")
print(f"index.html built: {len(data['items'])} items, {len(data['paths'])} paths")
