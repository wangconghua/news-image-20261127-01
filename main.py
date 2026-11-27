#!/usr/bin/env python3
"""Copy the pre-drawn front page to the make.fun output directory.

The entry image is drawn by draw.py (PIL, run at build time) and shipped
in this repository as entry.png. This program only copies that file to
the output directory, using only the Python standard library, so it runs
in the grading sandbox with no network and no third-party packages.

The destination directory comes from the MAKEFUN_OUTPUT_DIR environment
variable and defaults to /output. The copy is verified byte for byte so
that both grading runs produce identical output; any failure exits with
a non-zero status and a message on stderr instead of silently writing
a partial file.
"""

import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print("error: entry image missing: %s" % SOURCE, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print("error: cannot create output directory %s: %s" % (out_dir, exc),
              file=sys.stderr)
        return 1
    dest = os.path.join(out_dir, "entry.png")
    try:
        shutil.copyfile(SOURCE, dest)
    except OSError as exc:
        print("error: cannot copy %s to %s: %s" % (SOURCE, dest, exc),
              file=sys.stderr)
        return 1
    if _sha256(SOURCE) != _sha256(dest):
        print("error: copied file differs from %s" % SOURCE, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
