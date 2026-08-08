#!/usr/bin/env python3
"""Pure-standard-library independent recount for four exact-labeling cases."""
from __future__ import annotations
import argparse, csv, itertools, json, multiprocessing as mp, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("H?bB@_W", "HCQe`pk", "HCQe`pg", "H~~~~~~")


def decode_graph6(text: str) -> tuple[tuple[int, ...], ...]:
    n = ord(text[0]) - 63
    bits: list[int] = []
    for char in text[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency: list[list[int]] = [[] for _ in range(n)]
    position = 0
    for j in range(1, n):
        for i in range(j):
            if bits[position]:
                adjacency[i].append(j)
                adjacency[j].append(i)
            position += 1
    return tuple(tuple(neighbors) for neighbors in adjacency)


ADJACENCIES = tuple(decode_graph6(graph6) for graph6 in TARGETS)


def count_prefix(first_label: int) -> tuple[int, tuple[int, ...]]:
    remaining = tuple(label for label in range(1, 10) if label != first_label)
    counts = [0] * len(ADJACENCIES)
    for tail in itertools.permutations(remaining):
        labels = (first_label,) + tail
        for graph_index, adjacency in enumerate(ADJACENCIES):
            seen: set[int] = set()
            valid = True
            for neighbors in adjacency:
                weight = sum(labels[vertex] for vertex in neighbors)
                if weight in seen:
                    valid = False
                    break
                seen.add(weight)
            if valid:
                counts[graph_index] += 1
    return first_label, tuple(counts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=Path, default=ROOT / "results/order9_exact_label_counts_sample.csv")
    ap.add_argument("--output", type=Path, default=ROOT / "generated/order9_exact_label_counts_independent_recount.json")
    args = ap.parse_args()
    with args.sample.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected = {row["graph6"]: int(row["exact_distance_antimagic_labelings"]) for row in rows}

    requested = int(os.environ.get("DISTANCE_ANTIMAGIC_RECOUNT_PROCESSES", "1"))
    processes = min(9, max(1, requested))
    if processes == 1:
        partials = [count_prefix(label) for label in range(1, 10)]
    else:
        try:
            context = mp.get_context("fork")
        except ValueError:
            context = mp.get_context()
        with context.Pool(processes=processes) as pool:
            partials = pool.map(count_prefix, range(1, 10))

    totals = [0] * len(TARGETS)
    for _, counts in partials:
        for index, count in enumerate(counts):
            totals[index] += count

    output_rows = []
    for graph6, observed in zip(TARGETS, totals, strict=True):
        expected_count = expected[graph6]
        agreement = observed == expected_count
        output_rows.append({
            "graph6": graph6,
            "observed_count": observed,
            "expected_vectorized_count": expected_count,
            "agreement": agreement,
        })
        print(graph6, observed, expected_count, agreement, flush=True)

    result = {
        "implementation": "Python standard library only; independent graph6 decoder; direct exhaustive permutation loop partitioned by vertex-0 label",
        "processes": processes,
        "permutations_enumerated": 362880,
        "graph_labeling_pairs_checked": 4 * 362880,
        "all_agree": all(row["agreement"] for row in output_rows),
        "rows": output_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if not result["all_agree"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
