# 7. Results

## 7.1 Exhaustive order-nine classification

| Classification | Number of graph classes | Outcome |
|---|---:|---|
| Pairwise-distinct open neighborhoods | 205,914 | Every class received a verified distance-antimagic certificate |
| At least one repeated open neighborhood | 68,754 | Necessarily not distance-antimagic |
| **All order-nine classes** | **274,668** | **Completely classified** |

Both independent verifiers accepted all **205,914** positive certificates and reported **zero failures**.

The primary certificate archive has SHA-256:

```text
da32bb36f59a8999c735b4d1d585b372d9de665facc1c2ae3e55fb0025516bf1
```

The different-seed replay archive has SHA-256:

```text
92c3028274ce50ca21694f598536012ad8f4f1bcd2e1145be6aa7f523dcfcd36
```

## 7.2 Finite theorem

> **Theorem.** For every finite simple graph `G` with at most nine vertices, `G` is distance-antimagic if and only if its open neighborhoods are pairwise distinct.

The reverse implication follows from the exhaustive positive certificates through order nine. The forward implication is immediate: equal open neighborhoods force equal weights under every labeling.

> **Corollary.** Any counterexample to the Kamatchi–Arumugam conjecture has at least ten vertices.

Across orders one through nine, the study classifies **288,266** graph isomorphism classes and supplies **214,652** positive certificates.

## 7.3 Complete census through order nine

| Order | All graph classes | Point-determining | Repeated neighborhood | Certificates verified | Failures |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 1 | 0 |
| 2 | 2 | 1 | 1 | 1 | 0 |
| 3 | 4 | 2 | 2 | 2 | 0 |
| 4 | 11 | 5 | 6 | 5 | 0 |
| 5 | 34 | 16 | 18 | 16 | 0 |
| 6 | 156 | 78 | 78 | 78 | 0 |
| 7 | 1,044 | 588 | 456 | 588 | 0 |
| 8 | 12,346 | 8,047 | 4,299 | 8,047 | 0 |
| 9 | 274,668 | 205,914 | 68,754 | 205,914 | 0 |

## 7.4 Search-rank behavior

Under the fixed primary permutation order:

- mean first-success rank: **4.274736**;
- median rank: **3**;
- 90th percentile: **9**;
- 95th percentile: **12**;
- 99th percentile: **20**;
- maximum rank: **98**;
- 47,687 graphs (23.158697%) succeeded at rank 1;
- 191,540 graphs (93.019416%) succeeded by rank 10;
- 203,892 graphs (99.018037%) succeeded by rank 20.

The maximum-rank primary case was graph6 record:

```text
HCQe`pk
```

One explicit certificate is:

```text
labels  = 1,4,3,7,9,2,8,5,6
weights = 17,23,13,14,15,10,12,19,18
```

The labels are a permutation of `1,...,9`, and the weights are pairwise distinct.

## 7.5 Exact witness abundance in difficult cases

All `9!` labelings were tested for 33 deliberately difficult graphs, for a total of **11,975,040 exact graph-labeling evaluations**. Every sampled graph had thousands of valid certificates. The smallest exact witness set contained **17,190** labelings:

```text
17,190 / 362,880 = 4.737103%
```

The complete graph `K9` had all 362,880 labelings valid, as expected. Because the 33 graphs were selected adversarially rather than randomly, their witness fractions must not be interpreted as estimates for all eligible order-nine graphs.

## 7.6 Connected and disconnected classes

Among the 205,914 eligible order-nine classes:

- **197,772** are connected;
- **8,142** are disconnected;
- **3,199** distinct degree sequences occur.

Both connected and disconnected eligible classes were fully certified.

## 7.7 Edge-density distribution

Eligible graphs occur from 4 edges through 36 edges, with the largest counts concentrated near the middle densities. The exact edge-stratified census is published in `results/order9_primary_by_edges.csv`. The primary maximum search rank of 98 occurred in the 14-edge stratum. No eligible graph required the primary fallback beyond its 20,000 precomputed candidate pool.
