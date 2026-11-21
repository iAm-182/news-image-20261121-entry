#!/usr/bin/env python3
"""news-image-20261121 — entrypoint.

Copies the pre-drawn entry.png (produced by draw.py at build time) into the
grader's output directory. Standard library only, no network, deterministic:
two runs write identical bytes. The image itself is drawn at build time;
this entrypoint only places the finished file where the grader reads it.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
