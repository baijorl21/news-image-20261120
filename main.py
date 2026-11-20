#!/usr/bin/env python3
"""Entry for make.fun news-image-20261120: "Sum up 20 November's world news in one image".

The picture itself is entry.png beside this file, drawn from scratch with
make_image.py (Python + PIL, no photos or copyrighted assets). This program
copies it to /output/entry.png. It is deterministic: every run writes the
exact same bytes. Standard library only, no network.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: entry image not found: {source}", file=sys.stderr)
        raise SystemExit(1)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / "entry.png")


if __name__ == "__main__":
    main()
