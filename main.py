"""Write the one-line office joke to the make.fun output directory.

Reads entry.txt next to this script and writes it verbatim to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt), then
verifies the copy by size and SHA-256.
"""

import hashlib
import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.txt"
    data = source.read_bytes()
    text = data.decode("utf-8")
    if not text.strip():
        print("entry.txt is empty", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(data)
    # Verify the copy byte-for-byte before reporting success.
    written = target.read_bytes()
    if written != data:
        print("verification failed: bytes differ", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {target} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
