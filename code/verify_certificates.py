#!/usr/bin/env python3
"""Independent certificate verifier using NetworkX's graph6 parser."""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import Counter
from pathlib import Path
import networkx as nx


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def parse_csv_ints(s: str) -> list[int]:
    return [int(x) for x in s.split(',')] if s else []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('graph6')
    ap.add_argument('certificates')
    ap.add_argument('output_json')
    args = ap.parse_args()
    graph_path = Path(args.graph6)
    cert_path = Path(args.certificates)
    out_path = Path(args.output_json)

    certs: dict[int, dict[str, str]] = {}
    with cert_path.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            idx = int(row['index'])
            if idx in certs:
                raise SystemExit(f'duplicate certificate index {idx}')
            certs[idx] = row

    total = point = repeated = connected = connected_point = verified = failures = 0
    by_edges: Counter[int] = Counter()
    degree_sequences: set[tuple[int, ...]] = set()
    failure_examples: list[str] = []
    seen_g6: set[str] = set()
    order = None

    def fail(msg: str) -> None:
        nonlocal failures
        failures += 1
        if len(failure_examples) < 20:
            failure_examples.append(msg)

    with graph_path.open(encoding='ascii') as f:
        for raw in f:
            g6 = raw.strip()
            if not g6 or g6.startswith('>'):
                continue
            total += 1
            if g6 in seen_g6:
                fail(f'duplicate graph6 line at {total}: {g6}')
            seen_g6.add(g6)
            G = nx.from_graph6_bytes(g6.encode('ascii'))
            n = G.number_of_nodes()
            if order is None:
                order = n
            elif order != n:
                fail(f'mixed order at {total}: {n}')
            if nx.is_connected(G):
                connected += 1
            neighborhoods = [frozenset(G.neighbors(v)) for v in range(n)]
            is_point = len(set(neighborhoods)) == n
            row = certs.get(total)
            if not is_point:
                repeated += 1
                if row is not None:
                    fail(f'certificate supplied for repeated-neighborhood graph {total}')
                continue
            point += 1
            m = G.number_of_edges()
            by_edges[m] += 1
            degree_sequences.add(tuple(sorted((d for _, d in G.degree()), reverse=True)))
            if nx.is_connected(G):
                connected_point += 1
            if row is None:
                fail(f'missing certificate at graph {total}')
                continue
            if row['graph6'] != g6:
                fail(f'graph6 mismatch at graph {total}')
                continue
            labels = parse_csv_ints(row['labels_v0_to_vn_minus_1'])
            claimed = parse_csv_ints(row['weights_v0_to_vn_minus_1'])
            if sorted(labels) != list(range(1, n + 1)):
                fail(f'labels are not a permutation at graph {total}')
                continue
            weights = [sum(labels[u] for u in G.neighbors(v)) for v in range(n)]
            if weights != claimed:
                fail(f'weight mismatch at graph {total}: {weights} != {claimed}')
                continue
            if len(set(weights)) != n:
                fail(f'non-distinct weights at graph {total}: {weights}')
                continue
            verified += 1

    extra = sorted(set(certs) - set(range(1, total + 1)))
    if extra:
        fail(f'certificate indices beyond catalogue: {extra[:10]}')
    if len(certs) != point:
        fail(f'certificate count {len(certs)} != point-determining count {point}')

    result = {
        'input': str(graph_path), 'input_sha256': sha256(graph_path),
        'certificate': str(cert_path), 'certificate_sha256': sha256(cert_path),
        'order': order, 'total_graphs': total, 'unique_graph6_lines': len(seen_g6),
        'connected_graphs': connected,
        'point_determining_graphs': point,
        'repeated_neighborhood_graphs': repeated,
        'connected_point_determining_graphs': connected_point,
        'disconnected_point_determining_graphs': point - connected_point,
        'certificates_verified': verified,
        'number_of_degree_sequences_among_point_determining_graphs': len(degree_sequences),
        'point_determining_by_edges': {str(k): by_edges[k] for k in sorted(by_edges)},
        'failures': failures, 'failure_examples': failure_examples,
    }
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(result, sort_keys=True))
    if failures:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
