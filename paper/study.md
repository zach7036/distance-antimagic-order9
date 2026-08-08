# Exhaustive Verification of the Distance-Antimagic Open-Neighborhood Conjecture Through Order Nine

## 214,652 independently verified labeling certificates across 288,266 graph isomorphism classes

**Original computational combinatorics study**  
**Completed:** 8 August 2026  
**Status:** Not peer reviewed  
**Evidence standard:** Exhaustive finite enumeration with explicit machine-checkable certificates

## Abstract

A distance-antimagic labeling of a simple graph `G=(V,E)` of order `n` is a bijection `f:V->{1,...,n}` for which the open-neighborhood sums

```text
w_f(v) = sum(f(u) for u in N(v))
```

are pairwise distinct. Identical open neighborhoods are an immediate obstruction, and Kamatchi and Arumugam conjectured that this obstruction is also sufficient. Previous exhaustive work verified the conjecture through order eight. This study extends the exhaustive frontier to order nine.

The complete catalogue of **274,668** unlabeled simple graphs on nine vertices was processed. Exactly **205,914** classes have pairwise-distinct open neighborhoods and **68,754** are obstructed by a repeated open neighborhood. An explicit distance-antimagic labeling was constructed for every eligible class. Two independent verifiers—one using NetworkX's graph6 parser and one using a separately written standard-library-only graph6 decoder—accepted all 205,914 certificates with **zero failures**.

A second construction run with a different seed and a deliberately tiny initial pool independently reconstructed certificates for every eligible graph and exercised the fallback branch on 1,440 cases. Fresh optimized and sanitizer-enabled builds produced a byte-identical primary certificate archive. All `9! = 362,880` labelings were also enumerated for 33 deliberately difficult graphs, totaling **11,975,040** exact graph-labeling tests; the sparsest tested witness set still contained 17,190 valid labelings (4.737103%).

Combining the new order-nine result with a fresh lower-order reproduction gives **214,652 verified positive certificates across all 288,266 unlabeled simple graphs of orders one through nine**. Therefore the conjecture holds for every simple graph of order at most nine, and any counterexample must have at least ten vertices. A result-specific literature search located no earlier exhaustive order-nine verification; the contribution therefore appears to be a previously unreported computational extension, subject to the limitation that unindexed or unpublished work cannot be excluded.

## Completed paper

The report is divided into ordinary Markdown sections so every file remains easy to inspect:

1. [Introduction, literature, novelty, and research question](01_introduction_and_novelty.md)
2. [Data, methods, and analysis](02_data_and_methods.md)
3. [Results](03_results.md)
4. [Robustness, discussion, limitations, contribution, and significance](04_robustness_and_discussion.md)
5. [Reproducibility, conclusion, and references](05_reproducibility_and_references.md)

## Principal theorem

> **Theorem.** For every finite simple graph `G` with at most nine vertices, `G` is distance-antimagic if and only if its open neighborhoods are pairwise distinct.

> **Corollary.** Any counterexample to the Kamatchi–Arumugam conjecture has at least ten vertices.

## Canonical evidence identifiers

```text
839f67ecc73b1f539128694badebe27adf4f0fb1ee6d0663b7ad9868100d5123  graph9.g6
da32bb36f59a8999c735b4d1d585b372d9de665facc1c2ae3e55fb0025516bf1  order9_primary_certificates.tsv
92c3028274ce50ca21694f598536012ad8f4f1bcd2e1145be6aa7f523dcfcd36  order9_replay_seed8675309_pool20_certificates.tsv
```

**Keywords:** graph labeling; distance antimagic; point-determining graph; exhaustive enumeration; graph6; computational proof; certificate verification
