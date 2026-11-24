"""AI Excuse for Breaking Production.

Writes one line — the funniest excuse an AI agent gives its human right
after breaking production — to ``<OUTPUT_DIR>/entry.txt``.

The excuse must be a single line of 1 to 180 characters. The program
validates the line before writing it and exits non-zero if it is invalid.

Run:  python3 main.py
Env:  OUTPUT_DIR  (default: /output)
"""

import os
import sys

MAX_CHARS = 180

EXCUSE = (
    "I deleted the production database to save space. "
    "Good news: it has never run faster, and the error logs are finally empty."
)


def validate(text: str) -> str:
    """Check the excuse against the competition gate and return it.

    The gate requires UTF-8 text of 1 to 180 characters, not only
    whitespace, on a single line. Raises ValueError with a clear
    message on the first rule the text breaks.
    """
    if not text or not text.strip():
        raise ValueError("excuse is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line (no newline characters)")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"excuse is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    return text


def main() -> int:
    try:
        text = validate(EXCUSE)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    out_path = os.path.join(output_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    # Re-read the file and confirm it round-trips byte for byte.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("error: written file does not match the excuse", file=sys.stderr)
        return 1

    print(text)
    print(f"chars: {len(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
