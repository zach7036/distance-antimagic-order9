#!/usr/bin/env python3
"""Exact 9! labeling counts for a purposive hard-case sample."""
from __future__ import annotations
import argparse, csv, itertools, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def decode_graph6(s: str) -> list[int]:
    n = ord(s[0]) - 63
    bits: list[int] = []
    for c in s[1:]:
        x = ord(c) - 63
        bits += [(x >> k) & 1 for k in range(5, -1, -1)]
    adj = [0] * n
    p = 0
    for j in range(1, n):
        for i in range(j):
            if bits[p]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            p += 1
    return adj


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primary", type=Path, default=ROOT / "generated/order9_primary_certificates.tsv")
    ap.add_argument("--replay", type=Path, default=ROOT / "generated/order9_replay_seed8675309_pool20_certificates.tsv")
    ap.add_argument("--out-csv", type=Path, default=ROOT / "generated/order9_exact_label_counts_sample.csv")
    ap.add_argument("--out-json", type=Path, default=ROOT / "generated/order9_exact_label_counts_sample.json")
    args = ap.parse_args()

    primary = read_rows(args.primary)
    chosen: list[tuple[dict[str, str], str, int]] = []
    for edges in sorted({int(r["edges"]) for r in primary}):
        rows = [r for r in primary if int(r["edges"]) == edges]
        maxrank = max(int(r["search_rank"]) for r in rows)
        row = next(r for r in rows if int(r["search_rank"]) == maxrank)
        chosen.append((row, "primary_edgewise_max", maxrank))

    replay = read_rows(args.replay)
    maxrank = max(int(r["search_rank"]) for r in replay)
    row = next(r for r in replay if int(r["search_rank"]) == maxrank)
    if all(x[0]["graph6"] != row["graph6"] for x in chosen):
        item = (row, "replay_global_max", maxrank)
        pos = next((i + 1 for i, x in enumerate(chosen) if int(x[0]["edges"]) == int(row["edges"])), len(chosen))
        chosen.insert(pos, item)

    permutations = np.asarray(list(itertools.permutations(range(1, 10))), dtype=np.uint8)
    rows_out: list[dict[str, object]] = []
    for position, (row, source, rank) in enumerate(chosen, 1):
        adj = decode_graph6(row["graph6"])
        weights = np.empty((len(permutations), 9), dtype=np.uint8)
        for v, mask in enumerate(adj):
            idx = [i for i in range(9) if (mask >> i) & 1]
            weights[:, v] = permutations[:, idx].sum(axis=1, dtype=np.uint16) if idx else 0
        weights.sort(axis=1)
        valid = np.all(weights[:, 1:] != weights[:, :-1], axis=1)
        count = int(valid.sum())
        rows_out.append({
            "sample_position": position,
            "catalogue_index": int(row["index"]),
            "graph6": row["graph6"],
            "edges": int(row["edges"]),
            "selection_source": source,
            "primary_or_replay_search_rank": rank,
            "exact_distance_antimagic_labelings": count,
            "total_labelings": len(permutations),
            "witness_fraction": count / len(permutations),
        })
        print(position, row["graph6"], count)

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows_out[0].keys())
        writer.writeheader()
        writer.writerows(rows_out)
    args.out_json.write_text(json.dumps(rows_out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out_csv} ({len(rows_out)} graphs; {len(rows_out) * len(permutations):,} labelings)")


if __name__ == "__main__":
    main()
