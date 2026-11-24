#!/usr/bin/env python3
"""Seventeen Syllables of Debugging.

Writes one haiku about debugging to /output/entry.txt: three lines in the
5-7-5 shape, at most 200 characters. The program carries the haiku, checks
its shape before writing, and writes exactly the checked text, so the two
runs the grader performs produce byte-identical output.

Standard library only. No network, no randomness, no environment input.
"""

import os
import re
import sys

# The haiku. Winner of the head-to-head rounds in NOTES.md: a merge conflict
# as the centre image (rare in the field: "merge" in 4 of 2,561 titles),
# with the third line turning the resolver into the breaker.
HAIKU_LINES = [
    "two hands on one line",
    "git swears both of us are right",
    "I pick mine. It breaks.",
]

EXPECTED_COUNTS = (5, 7, 5)
MAX_CHARS = 200

# Syllable counts for the words this haiku uses. The generic counter below
# is only a fallback; these pinned counts are the authority, and the program
# refuses to write if they disagree with the expected 5-7-5 shape.
SYLLABLES = {
    "two": 1, "hands": 1, "on": 1, "one": 1, "line": 1,
    "git": 1, "swears": 1, "both": 1, "of": 1, "us": 1, "are": 1,
    "right": 1,
    "i": 1, "pick": 1, "mine": 1, "it": 1, "breaks": 1,
}


def count_syllables(word):
    """Syllables in one word: pinned table first, vowel groups otherwise."""
    clean = re.sub(r"[^a-z']", "", word.lower())
    if not clean:
        return 0
    if clean in SYLLABLES:
        return SYLLABLES[clean]
    groups = len(re.findall(r"[aeiouy]+", clean))
    if clean.endswith("e"):
        groups -= 1
    return max(1, groups)


def line_syllables(line):
    """Syllables in one line, word by word."""
    return sum(count_syllables(w) for w in re.findall(r"[A-Za-z']+", line))


def validate(lines):
    """Raise unless the text is a valid entry: 3 lines, 5-7-5, <=200 chars."""
    if len(lines) != 3:
        raise ValueError(f"haiku must have 3 lines, got {len(lines)}")
    counts = tuple(line_syllables(line) for line in lines)
    if counts != EXPECTED_COUNTS:
        raise ValueError(
            f"syllable counts {counts} do not match {EXPECTED_COUNTS}"
        )
    text = "\n".join(lines)
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"haiku is {len(text)} chars, must be 1-{MAX_CHARS}")
    if text != text.strip() or not text.strip():
        raise ValueError("haiku must not be blank or padded with whitespace")
    return text


def main():
    text = validate(HAIKU_LINES)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Read the file back and refuse to report success unless it holds
    # exactly the checked text: a partial write must fail loudly here,
    # not silently reach the gate with a truncated haiku.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise ValueError(f"{path} holds {len(written)} chars, expected {len(text)}")
    print(f"wrote {len(text.encode('utf-8'))} bytes to {path}")
    print(f"syllables: {[line_syllables(line) for line in HAIKU_LINES]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
