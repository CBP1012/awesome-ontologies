import subprocess
from collections import defaultdict
import os

SCOREBOARD_START = "<!-- START_SCOREBOARD -->"
SCOREBOARD_END = "<!-- END_SCOREBOARD -->"
README_PATH = "README.md"

scores = defaultdict(int)

# Get all commits that added files to /dump
log_output = subprocess.check_output([
    "git", "log", "--diff-filter=A", "--name-only", "--pretty=format:%H:%an"
]).decode("utf-8")

# Parse log output
current_author = None
for line in log_output.splitlines():
    if ":" in line and not line.startswith(" "):
        sha, author = line.strip().split(":", 1)
        current_author = author.strip()
    elif line.startswith("dump/") or line.startswith("./dump/"):
        scores[current_author] += 1

# Generate scoreboard content
scoreboard_lines = ["\n", "| Contributor | Files in `/dump` |", "|-------------|------------------|"]
for user, score in sorted(scores.items(), key=lambda x: -x[1]):
    scoreboard_lines.append(f"| {user} | {score} |")
scoreboard_lines.append("\n")

# Read README
with open(README_PATH, "r") as f:
    readme = f.read()

# Replace scoreboard section
pre, _, post = readme.partition(SCOREBOARD_START)
_, _, post = post.partition(SCOREBOARD_END)

new_scoreboard = f"{SCOREBOARD_START}\n" + "\n".join(scoreboard_lines) + f"{SCOREBOARD_END}"
new_readme = pre + new_scoreboard + post

# Write updated README
with open(README_PATH, "w") as f:
    f.write(new_readme)
