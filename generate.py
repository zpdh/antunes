"""
Regenerate posts/posts.json from the .md files in posts/.
"""

import json
import re
from pathlib import Path

posts_dir = Path(__file__).parent / "posts"


def front_matter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    data = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
    return data


entries = []
for f in posts_dir.glob("*.md"):
    meta = front_matter(f.read_text(encoding="utf-8"))
    if meta.get("draft", "").lower() == "true":
        continue  # add `draft: true` to hide a post
    entries.append((meta.get("date", ""), f.name))

entries.sort(reverse=True)  # newest first
names = [name for _, name in entries]
(posts_dir / "posts.json").write_text(
    json.dumps(names, indent=2) + "\n", encoding="utf-8"
)
print(f"Wrote posts.json with {len(names)} post(s)")
