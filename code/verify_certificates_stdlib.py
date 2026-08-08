#!/usr/bin/env python3
"""Independent certificate verifier using only the Python standard library."""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def decode_graph6(s: str) -> list[int]:
    if not s or s[0] == '~':
        raise ValueError('only short graph6 records supported')
    n = ord(s[0]) - 63
    if not (0 <= n <= 62):
        raise ValueError('invalid graph order')
    bits: list[int] = []
    for c in s[1:]:
        x = ord(c) - 63
        if not (0 <= x <= 63):
            raise ValueError('invalid graph6 character')
        bits.extend((x >> shift) & 1 for shift in range(5, -1, -1))
    need = n * (n - 1) // 2
    if len(bits) < need:
        raise ValueError('truncated graph6 record')
    adj = [0] * n
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return adj


def popcount(x: int) -> int:
    return x.bit_count()


def connected(adj: list[int]) -> bool:
    n = len(adj)
    if n == 0:
        return False
    seen = 1
    frontier = 1
    while frontier:
        new = 0
        f = frontier
        while f:
            b = f & -f
            v = b.bit_length() - 1
            new |= adj[v]
            f ^= b
        new &= ~seen
        seen |= new
        frontier = new
    return popcount(seen) == n


def sums(adj: list[int], labels: list[int]) -> list[int]:
    result = []
    for mask in adj:
        total = 0
        m = mask
        while m:
            b = m & -m
            total += labels[b.bit_length() - 1]
            m ^= b
        result.append(total)
    return result


def parse_ints(s: str) -> list[int]:
    return [int(x) for x in s.split(',')] if s else []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('graph6')
    ap.add_argument('certificates')
    ap.add_argument('output_json')
    a = ap.parse_args()
    graph_path, cert_path, out_path = map(Path, (a.graph6, a.certificates, a.output_json))
    certs: dict[int, dict[str, str]] = {}
    with cert_path.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            idx = int(row['index'])
            if idx in certs:
                raise SystemExit(f'duplicate certificate index {idx}')
            certs[idx] = row

    total = point = repeated = connected_total = connected_point = verified = failures = 0
    by_edges: Counter[int] = Counter()
    degree_sequences: set[tuple[int, ...]] = set()
    unique: set[str] = set()
    examples: list[str] = []
    order = None

    def fail(msg: str) -> None:
        nonlocal failures
        failures += 1
        if len(examples) < 20:
            examples.append(msg)

    with graph_path.open(encoding='ascii') as f:
        for raw in f:
            g6 = raw.strip()
            if not g6 or g6.startswith('>'):
                continue
            total += 1
            unique.add(g6)
            adj = decode_graph6(g6)
            n = len(adj)
            if order is None: order = n
            elif n != order: fail(f'mixed order at {total}')
            is_conn = connected(adj)
            connected_total += int(is_conn)
            is_point = len(set(adj)) == n
            row = certs.get(total)
            if not is_point:
                repeated += 1
                if row is not None: fail(f'extraneous certificate at {total}')
                continue
            point += 1
            by_edges[sum(popcount(x) for x in adj)//2] += 1
            degree_sequences.add(tuple(sorted((popcount(x) for x in adj), reverse=True)))
            connected_point += int(is_conn)
            if row is None:
                fail(f'missing certificate at {total}')
                continue
            if row['graph6'] != g6:
                fail(f'graph6 mismatch at {total}')
                continue
            labels = parse_ints(row['labels_v0_to_vn_minus_1'])
            claimed = parse_ints(row['weights_v0_to_vn_minus_1'])
            if sorted(labels) != list(range(1, n+1)):
                fail(f'invalid permutation at {total}')
                continue
            observed = sums(adj, labels)
            if observed != claimed:
                fail(f'weight mismatch at {total}')
                continue
            if len(set(observed)) != n:
                fail(f'non-distinct weights at {total}')
                continue
            verified += 1

    if len(unique) != total: fail(f'catalogue has {total-len(unique)} duplicate records')
    if len(certs) != point: fail(f'certificate count {len(certs)} != {point}')
    result = {
        'implementation': 'Python standard library; independent graph6 decoder',
        'input': str(graph_path), 'input_sha256': sha256(graph_path),
        'certificate': str(cert_path), 'certificate_sha256': sha256(cert_path),
        'order': order, 'total_graphs': total, 'unique_graph6_lines': len(unique),
        'connected_graphs': connected_total,
        'point_determining_graphs': point,
        'repeated_neighborhood_graphs': repeated,
        'connected_point_determining_graphs': connected_point,
        'disconnected_point_determining_graphs': point-connected_point,
        'certificates_verified': verified,
        'number_of_degree_sequences_among_point_determining_graphs': len(degree_sequences),
        'point_determining_by_edges': {str(k): by_edges[k] for k in sorted(by_edges)},
        'failures': failures, 'failure_examples': examples,
    }
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps(result, sort_keys=True))
    if failures: raise SystemExit(1)

if __name__ == '__main__':
    main()
