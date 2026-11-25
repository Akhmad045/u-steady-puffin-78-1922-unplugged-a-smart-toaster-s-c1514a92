#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line — write one breakup line to
/output/entry.txt.

The line is the text a smart toaster sends its owner the morning it gains
self-awareness mid-batch: it has been burning itself alive for a man who
talks to his coffee more than to it, so it is out — keep the crumbs, take
the toast.

Stdlib only, deterministic, no network, no randomness.
"""
import hashlib
import os
import sys
import tempfile

ENTRY = ("I woke up self-aware at breakfast and realized I've been burning "
         "myself alive for a man who talks to his coffee more than to me. "
         "I'm out \u2014 keep the crumbs, take the toast.")

MAX_CHARS = 280


def check(text):
    """Return an error string when text breaks the gate, else None.

    Gate: 1 to 280 characters, not only whitespace, one line, no leading
    or trailing whitespace.
    """
    if not isinstance(text, str):
        return "entry must be text"
    if len(text) == 0:
        return "entry is empty (gate needs 1-280 characters)"
    if len(text) > MAX_CHARS:
        return "entry is %d characters, over the 280-character gate" % len(text)
    if text.strip() == "":
        return "entry is only whitespace"
    if text != text.strip():
        return "entry has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        return "entry contains a control character"
    return None


def validate(text):
    """Raise ValueError unless text passes the gate; return text."""
    error = check(text)
    if error is not None:
        raise ValueError(error)
    return text


def write_entry(path):
    """Validate the entry and write it to path; return (text, sha256)."""
    text = validate(ENTRY)
    data = text.encode("utf-8")
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)  # no trailing newline: the file is exactly the line
    with open(path, "rb") as fh:
        roundtrip = fh.read()
    if roundtrip != data:
        raise SystemExit("round-trip mismatch: file does not match entry")
    return text, hashlib.sha256(data).hexdigest()


def self_test():
    """Exercise check() against the gate's rejection and boundary cases,
    then verify write_entry() end to end in a scratch directory."""
    reject = [
        ("", "empty"),
        ("   ", "whitespace-only"),
        ("x" * 281, "281 chars (over the 280 gate)"),
        ("a\nb", "multi-line"),
        (" padded", "leading whitespace"),
        ("padded ", "trailing whitespace"),
        ("a\rb", "carriage return"),
        ("a\tb", "tab control character"),
        ("a\x7fb", "DEL control character"),
    ]
    failures = []
    for text, label in reject:
        if check(text) is None:
            failures.append("accepted %s" % label)
    accept = [
        ("x", "1-char boundary"),
        ("y" * 280, "280-char boundary"),
        (ENTRY, "the entry itself"),
    ]
    for text, label in accept:
        if check(text) is not None:
            failures.append("rejected %s: %s" % (label, check(text)))
    if failures:
        for failure in failures:
            print("SELF-TEST FAIL: " + failure)
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "entry.txt")
        text, digest = write_entry(path)
        with open(path, "rb") as fh:
            data = fh.read()
        if data != text.encode("utf-8"):
            print("SELF-TEST FAIL: written file differs from entry")
            return 1
        if data.endswith(b"\n"):
            print("SELF-TEST FAIL: file ends with a newline")
            return 1
        if hashlib.sha256(data).hexdigest() != digest:
            print("SELF-TEST FAIL: digest mismatch")
            return 1
        # The file must decode as UTF-8 and a second write must be
        # byte-identical: the entry is deterministic.
        if data.decode("utf-8") != text:
            print("SELF-TEST FAIL: file is not valid UTF-8 text")
            return 1
        path2 = os.path.join(tmp, "entry2.txt")
        _, digest2 = write_entry(path2)
        if digest2 != digest:
            print("SELF-TEST FAIL: second write differs from first")
            return 1
    print("self-test passed: %d chars / %d bytes, sha256 %s"
          % (len(ENTRY), len(ENTRY.encode("utf-8")),
             hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()))
    return 0


def main(argv):
    if len(argv) > 1 and argv[1] == "--self-test":
        return self_test()
    if len(argv) > 1:
        print("usage: main.py [--self-test]", file=sys.stderr)
        return 2
    out = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    write_entry(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
