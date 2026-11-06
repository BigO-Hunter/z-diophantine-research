#!/usr/bin/env python3
"""Inventory a release ZIP (path list only, no extraction) and hash the quartic package files.

Binary-safe: never decodes file bodies. Writes inventory.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--package", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    z = Path(a.zip)
    entry = {}
    with zipfile.ZipFile(z) as zf:
        infos = zf.infolist()
        entry["zip"] = z.name
        entry["zip_bytes"] = z.stat().st_size
        entry["zip_sha256"] = sha256(z)
        entry["file_count"] = len(infos)
        entry["uncompressed_bytes"] = sum(i.file_size for i in infos)
        tops = Counter()
        for i in infos:
            parts = i.filename.split("/")
            tops["/".join(parts[:2]) if len(parts) > 2 else parts[0]] += 1
        entry["top_level"] = dict(sorted(tops.items(), key=lambda kv: -kv[1])[:25])
        entry["largest"] = sorted(
            ({"name": i.filename, "bytes": i.file_size} for i in infos), key=lambda d: -d["bytes"]
        )[:12]

    pkg = Path(a.package)
    files = []
    for p in sorted(pkg.rglob("*")):
        if p.is_file():
            files.append(
                {"path": str(p.relative_to(pkg)), "bytes": p.stat().st_size, "sha256": sha256(p)}
            )
    entry["package_file_count"] = len(files)
    entry["package_bytes"] = sum(f["bytes"] for f in files)
    entry["package_files"] = files
    Path(a.out).write_text(json.dumps(entry, indent=1) + "\n")
    print(
        f"{z.name}: {entry['file_count']} files, {entry['uncompressed_bytes']:,} B uncompressed\n"
        f"package: {entry['package_file_count']} files, {entry['package_bytes']:,} B"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
