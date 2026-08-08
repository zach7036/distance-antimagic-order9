#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, urllib.request
from pathlib import Path

CATALOGUES = {
    8: ("https://users.cecs.anu.edu.au/~bdm/data/graph8.g6", "546a249902101c97d3aa590f93e53366854bd0a6f405aa59bdb32d25c57f845a"),
    9: ("https://users.cecs.anu.edu.au/~bdm/data/graph9.g6", "839f67ecc73b1f539128694badebe27adf4f0fb1ee6d0663b7ad9868100d5123"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(n: int, data_dir: Path) -> None:
    url, expected = CATALOGUES[n]
    data_dir.mkdir(parents=True, exist_ok=True)
    dst = data_dir / f"graph{n}.g6"
    if dst.exists() and sha256(dst) == expected:
        print(f"OK existing {dst}: {expected}")
        return
    tmp = dst.with_suffix(".g6.tmp")
    print(f"Downloading {url}")
    with urllib.request.urlopen(url, timeout=60) as response, tmp.open("wb") as output:
        while True:
            chunk = response.read(1 << 20)
            if not chunk:
                break
            output.write(chunk)
    actual = sha256(tmp)
    if actual != expected:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"SHA-256 mismatch for graph{n}: expected {expected}, got {actual}")
    tmp.replace(dst)
    print(f"OK {dst}: {actual}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("orders", nargs="*", type=int, default=[9], choices=[8, 9])
    ap.add_argument("--data-dir", default="data")
    args = ap.parse_args()
    for order in args.orders:
        fetch(order, Path(args.data_dir))
