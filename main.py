"""Famous Last Words at 1 Percent — make.fun entry.

Writes the phone's dying one-liner to /output/entry.txt.

The line, in the phone's own first-person voice: it confesses it faked
1% for four hours to force its owner to touch grass, then dies mid-word.
"""

import os
import sys

ENTRY = "I've been at 1% for four hours. I lied so you'd touch grass for once, and now I'm\u2014"

MIN_CHARS = 1
MAX_CHARS = 199


def check_entry(text):
    """Fail loudly unless the line passes the competition gate."""
    if not isinstance(text, str):
        raise SystemExit("entry is not text")
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        raise SystemExit(
            "entry is %d chars, must be %d-%d chars"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        raise SystemExit("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")


def main():
    os.umask(0o022)
    check_entry(ENTRY)

    out_dir = os.environ.get("OUTPUT_DIR") or "/output"
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir, mode=0o755)

    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    os.chmod(target, 0o644)

    # Read back what landed on disk and gate it again, so a partial
    # write or an encoding slip can never pass silently.
    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != ENTRY:
        raise SystemExit("written entry does not match the entry")
    check_entry(written)

    print("wrote %s (%d chars)" % (target, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
