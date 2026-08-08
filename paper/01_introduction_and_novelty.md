# 1. Introduction

For a finite simple graph `G=(V,E)` with `|V|=n`, a vertex labeling is a bijection

```text
f: V -> {1,2,...,n}.
```

The open-neighborhood weight at a vertex `v` is

```text
w_f(v) = sum(f(u) for u in N_G(v)).
```

The labeling is **distance-antimagic** when `w_f(x) != w_f(y)` for every two distinct vertices `x` and `y`.

If two vertices have the same open neighborhood, then their weights are equal under every labeling. Pairwise-distinct open neighborhoods are therefore necessary. Kamatchi and Arumugam conjectured that this necessary condition is sufficient. In graph-enumeration terminology, graphs with pairwise-distinct open neighborhoods are also called **point-determining** or **mating** graphs.

The conjecture is nontrivial because its hypothesis is a local structural condition while its conclusion requires a global permutation satisfying all pairwise weight inequalities. Earlier exhaustive computation established the conjecture through order eight. Order nine is the next complete isomorphism catalogue and is large enough to constitute a substantial extension while remaining feasible for exhaustive construction, independent verification, and adversarial replay.

# 2. Literature and novelty review

Kamatchi and Arumugam introduced distance-antimagic graphs and stated the open-neighborhood conjecture in 2013. Simanjuntak and collaborators subsequently reported exhaustive agreement through order eight: among the 12,346 unlabeled simple graphs of order eight, all 8,047 graphs without repeated open neighborhoods were distance-antimagic. Later work established the property for particular graph families, including product graphs and circulants, but did not report a complete order-nine census.

Before selecting this problem, candidate questions were screened for computational tractability, scientific value, and whether a definitive result could be obtained using public data and available computation. The order-nine extension was selected because:

1. the prior exhaustive boundary was explicitly order eight;
2. the complete order-nine catalogue is public and finite;
3. every positive instance can be accompanied by a compact, independently checkable certificate;
4. a negative instance, if found, would be an explicit counterexample to the conjecture;
5. all classes could be processed and independently replayed rather than sampled.

After the computation, a second novelty search used combinations of:

- distance antimagic; distance-antimagic; `{1}`-antimagic; `D={1}` antimagic;
- identical open neighborhoods; identical neighborhoods; neighborhood twins; `{1}`-twins;
- point-determining graph; mating graph;
- order 9; order nine; 9 vertices; nine vertices;
- exhaustive; computationally verified; all non-isomorphic graphs; nauty; graph6;
- the exact values 205,914 and 274,668;
- the maximum-rank graph6 identifiers and result-specific terminology suggested by the computation.

No earlier exhaustive order-nine verification or complete order-nine certificate construction was located. The novelty claim is therefore deliberately phrased as **appears previously unreported**, not as an absolute guarantee. Unindexed, private, or unpublished work cannot be excluded, and the manuscript has not yet undergone external peer review.

# 3. Research question and hypothesis

## Research question

Does every simple graph on nine vertices with pairwise-distinct open neighborhoods admit a distance-antimagic labeling?

## Falsifiable hypothesis

For every one of the 205,914 order-nine point-determining graph isomorphism classes, there exists a permutation of `1,...,9` whose nine open-neighborhood sums are pairwise distinct.

A single eligible graph for which all `9! = 362,880` permutations failed would falsify the hypothesis and the general conjecture.

## What was known and what remained unknown

Previous research established the following:

- equal open neighborhoods are a necessary obstruction;
- the conjecture holds exhaustively for every simple graph through order eight;
- many specific graph families satisfy the conjectured behavior;
- there are 274,668 unlabeled simple graphs of order nine;
- 205,914 of those classes are point-determining.

What remained unknown was whether every one of those 205,914 order-nine classes admitted a distance-antimagic labeling. This study determines that finite question completely.
