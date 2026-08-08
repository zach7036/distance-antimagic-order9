# 8. Robustness and falsification tests

The result was treated adversarially after the first successful construction. It survived the following attempts to invalidate it:

1. **Independent graph6 implementation.** A standard-library-only decoder reproduced the same census and accepted all certificates.
2. **Independent library parser.** NetworkX independently decoded all records and accepted all certificates.
3. **Different seed.** Seed `8675309` generated a separate complete archive.
4. **Forced fallback coverage.** Reducing the initial candidate pool to 20 forced fallback execution on 1,440 cases; all were solved.
5. **Lower-order replication.** The previously published frontier through order eight was regenerated before accepting the order-nine extension.
6. **Exact permutation enumeration.** Every possible labeling was checked for 33 difficult graphs.
7. **Independent exact recount.** A separate standard-library implementation reproduced the exact witness counts for representative cases.
8. **Fresh compilation.** A newly compiled optimized build reproduced the exact primary archive hash.
9. **Sanitizer audit.** AddressSanitizer and UndefinedBehaviorSanitizer reported no error and reproduced the exact primary hash.
10. **Catalogue integrity.** The order-nine file contained 274,668 unique graph6 records and matched the published catalogue census.
11. **Result-specific novelty search.** Searches using the discovered counts, terminology, and graph-labeling result found no prior order-nine exhaustive report.

The central result is an exhaustive finite theorem rather than a statistical inference. Its uncertainty is computational: catalogue completeness, parser correctness, implementation correctness, and certificate validity. The independent decoders, cryptographic hashes, replay, lower-order replication, exhaustive subtests, and sanitizer audit directly target those risks.

# 9. Discussion

The result strengthens evidence for the general conjecture and moves its complete computational boundary from eight to nine vertices. The order-nine catalogue is more than twenty times larger than the order-eight catalogue, so the extension represents a substantial increase in the number of exhaustively classified isomorphism classes.

The explicit certificate construction raises the evidentiary standard above an aggregate success count. Every positive claim can be replayed independently from a graph6 record, a nine-entry label permutation, and a nine-entry weight vector. The repository publishes the exact source code, canonical hashes, summary outputs, and sample certificates; the two large complete archives are regenerated transparently rather than hidden in encoded upload payloads.

The low first-success ranks and exact witness counts suggest that valid labelings are often abundant, even among purposively difficult cases. This may help future theoretical work by indicating that the conjecture is not typically sustained by a unique or exceptionally rare permutation. That interpretation remains suggestive rather than proved: a structural lower bound on the number of valid labelings is still open.

Order ten contains 12,005,168 unlabeled graph classes, making a direct extension substantially larger. It remains computationally plausible with parallel processing, symmetry-aware search, or distributed certificate construction, but this study does not claim an order-ten result.

# 10. Limitations

This study does **not** prove the conjecture for arbitrary graph order or for order ten. Its theorem is finite and bounded by nine vertices.

The novelty review cannot exclude inaccessible, private, or unindexed work. The report has not undergone external peer review.

The construction is exhaustive over graph isomorphism classes but uses one fixed vertex order per graph6 representative. That is sufficient because distance-antimagic existence is invariant under graph isomorphism.

Search-rank statistics depend on the selected randomized permutation order. The exact abundance sample is purposive and cannot be generalized statistically to all eligible graphs.

The C++ implementation stores observed weights in a 64-bit bitset. For the supported orders through ten, the maximum possible neighborhood sum is safely below 64. Extending the constructor to larger orders would require changing that representation.

As with any computational proof, implementation and data risks cannot be reduced literally to zero. The independent decoders, byte hashes, replay, lower-order reproduction, exact enumeration, and sanitizer audits substantially reduce those risks.

# 11. Novel contribution

Previous research established the open-neighborhood conjecture exhaustively through order eight. This study determines, apparently for the first time in the available literature, that **all 205,914 point-determining graph classes on nine vertices are distance-antimagic**, provides an explicit certificate construction for every class, and establishes that **any counterexample must have at least ten vertices**.

# 12. Scientific significance

The result is a **meaningful incremental frontier advance**. It does not resolve the general conjecture and should not be described as breakthrough-level. Its value is the complete extension of an established computational boundary, the large increase in classified isomorphism classes, the explicit certificate construction, and the publication of independently reproducible evidence.

The result can be used as:

- a verified finite base for future theoretical induction or structural arguments;
- a benchmark corpus for new graph-labeling algorithms;
- evidence that any counterexample must first occur at order ten or higher;
- a source of hard and easy instances for studying witness abundance;
- a reproducibility benchmark for computational combinatorics workflows.
