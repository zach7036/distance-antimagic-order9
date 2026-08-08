#!/usr/bin/env python3
"""Regenerate exact order-1 through order-7 graph6 catalogues from NetworkX's Graph Atlas."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
import networkx as nx

EXPECTED = {
    1: "ecf5de1a2ecc66a1876a832804c64f6b5125784e94c82285d9720621c613ab46",
    2: "b7cd2a004ade86133158ffa94292f1d79a1fa154874706bf33b9e841cd3fa4cb",
    3: "ad734c7f1aa188ac62d0ba1b2c514d019e1e2602e846f9bcc471f5850e392ab8",
    4: "204bfcb4c55a445224ed77b69b8bc648eb6bfd6b71fe29bb77ba31ef75067673",
    5: "6d2822f724f5b5213bcef73d91963e9510c4159e9cae15951d3d699d40c1659e",
    6: "f85812bc936feefd5972b1c3cddc7b138a31c1224256883b541146d780a68b12",
    7: "811b507699101ae6adeddd595c4d5643b0b6f3188b5738c374b4874df06ab97d",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    args = ap.parse_args()
    out = Path(args.data_dir)
    out.mkdir(parents=True, exist_ok=True)
    atlas = nx.graph_atlas_g()
    for n in range(1, 8):
        graphs = [g for g in atlas if g.number_of_nodes() == n]
        path = out / f"graph{n}.g6"
        with path.open("wb") as f:
            for graph in graphs:
                f.write(nx.to_graph6_bytes(graph, header=False))
        actual = digest(path)
        if actual != EXPECTED[n]:
            raise SystemExit(f"graph{n}.g6 hash mismatch: expected {EXPECTED[n]}, got {actual}")
        print(f"OK graph{n}.g6: {len(graphs)} records, {actual}")


if __name__ == "__main__":
    main()
