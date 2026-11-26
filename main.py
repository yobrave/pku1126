"""Robot pickup line builder: validates the champion line and ships it out."""
from pathlib import Path
import json
import os
import sys

LIMIT = 200
CONTEST = "u-jolly-fox-32-the-robot-pickup-line-championship-3c177b1b"


class LineGuard:
    def __init__(self, root):
        self.source = root / "entry.txt"

    def inspect(self, text):
        if not text.strip():
            return "empty"
        if len(text) > LIMIT:
            return "over-limit"
        return "pass"


def ship(payload, destination):
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "entry.txt"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    return target


def run():
    here = Path(__file__).resolve().parent
    guard = LineGuard(here)
    raw = guard.source.read_text(encoding="utf-8").rstrip("\n")
    state = guard.inspect(raw)
    envelope = {"guard": state, "chars": len(raw), "line": raw, "contest": CONTEST}
    if state != "pass":
        print(json.dumps(envelope))
        sys.exit(1)
    drop = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    shipped = ship(raw + "\n", Path(drop))
    envelope["shipped_to"] = str(shipped)
    print("VERDICT", state, json.dumps(envelope))


if __name__ == "__main__":
    run()
