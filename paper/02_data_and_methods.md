# 4. Data and materials

The order-nine input was Brendan McKay's complete catalogue of all **274,668 unlabeled simple graphs on nine vertices**, represented in graph6 format. The canonical catalogue SHA-256 is:

```text
839f67ecc73b1f539128694badebe27adf4f0fb1ee6d0663b7ad9868100d5123
```

The order-eight catalogue was obtained from the same source. Orders one through seven were exported deterministically from NetworkX's Graph Atlas. The repository includes scripts that regenerate or download these catalogues and reject them if their hashes disagree with the completed study.

Software used in the completed study included:

- a C++20 constructor;
- an independent Python verifier using NetworkX;
- a second Python verifier using only the standard library and a separately written graph6 decoder;
- exact-labeling enumeration scripts;
- Python analysis and figure-generation scripts;
- warning-clean optimized and sanitizer-enabled compiler builds.

# 5. Methods

## 5.1 Eligibility classification

Each graph6 record was decoded into open-neighborhood bitmasks. A graph was classified as eligible precisely when all `n` masks were distinct. If two masks were equal, the graph was placed in the obstructed class because those two vertices necessarily receive equal neighborhood sums under every labeling.

This obstruction is exact in one direction: if `N(x)=N(y)`, then for every labeling `f`,

```text
w_f(x) = sum(f(u) for u in N(x))
       = sum(f(u) for u in N(y))
       = w_f(y).
```

## 5.2 Certificate construction

For `n=9`, all `9! = 362,880` permutations of labels `1,...,9` were generated once. Their order was shuffled using the fixed seed `20260807`. For each permutation in an initial pool of 20,000 candidates, all subset sums of labels were precomputed. Since each open neighborhood is represented by a 9-bit mask, the weight of every vertex can then be retrieved by a table lookup.

For every eligible graph, candidate permutations were tested in the fixed order until all nine weights were distinct. If the initial pool failed, the remaining permutations were tested directly. Every accepted candidate was rechecked by a separate direct calculation before it was written to the certificate archive.

The canonical certificate archive stores:

- catalogue index;
- graph6 representation;
- edge count;
- first-success search rank;
- nine labels in graph6 vertex order;
- the corresponding nine open-neighborhood weights.

## 5.3 Independent verification

The constructor's success reports were not treated as proof. Two independently implemented verifiers loaded the graph catalogue and certificate archive and checked, for every record, that:

1. the catalogue record decodes correctly;
2. the graph's open neighborhoods are classified correctly;
3. obstructed graphs have no supplied certificate;
4. every eligible graph has exactly one certificate;
5. the labels are exactly a permutation of `1,...,9`;
6. the graph6 identifier agrees with the catalogue record;
7. all nine weights recomputed from adjacency agree with the listed weights;
8. the nine recomputed weights are pairwise distinct.

One verifier delegated graph6 parsing to NetworkX. The other used only the Python standard library and a separately written graph6 decoder.

## 5.4 Different-seed replay

A second constructor run used seed `8675309` and an initial pool of only 20 permutations. This intentionally forced the fallback branch on **1,440** graphs and generated a separate 205,914-row archive. The replay archive was independently verified in the same way as the primary archive.

## 5.5 Lower-order replication

Before accepting the new order-nine result, the same constructor and independent verifier were run over orders one through eight. This reproduced the previously published order-eight frontier and confirmed that the pipeline recovered all known eligible counts without a failure.

## 5.6 Exact witness-abundance tests

A purposive adversarial sample selected the maximum primary search-rank graph in each represented edge stratum and added the replay's global maximum when distinct. For each of the resulting 33 graphs, every one of the 362,880 possible labelings was enumerated exactly. This produced 11,975,040 graph-labeling evaluations.

A separate standard-library implementation independently recounted representative cases, including the least-abundant sampled graph, the primary global maximum-rank graph, the replay global maximum-rank graph, and the complete graph.

## 5.7 Software audit

Optimized, freshly recompiled, and sanitizer-enabled constructor builds were compared at the byte level. AddressSanitizer and UndefinedBehaviorSanitizer were run with halt-on-error settings. The canonical primary archive was accepted only after these builds generated the same SHA-256 digest.

# 6. Analysis

The primary endpoint was exhaustive existence: whether each eligible graph had at least one verified certificate. Because every isomorphism class in the finite population was processed, the main result has no sampling uncertainty, confidence interval, or p-value. Computational uncertainty was instead addressed through catalogue hashes, exact record counts, independent parsers, independent verifiers, replay runs, lower-order replication, exact enumeration on adversarial cases, and sanitizer audits.

Secondary analyses measured first-success rank under the fixed primary permutation order and exact witness abundance in the adversarial sample. These quantities describe the behavior of the construction and selected hard cases; they are not population estimates from random samples.
