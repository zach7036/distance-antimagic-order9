# Distance-Antimagic Research Suite

**Release:** 1.1.0 (August 13, 2026)  
**Author:** Zach Waddle  
**Status:** research drafts and reproducibility materials; not yet peer reviewed

This repository is the public home for a connected program of research on distance-antimagic graph labelings. It began as the exhaustive order-nine computation and now also documents two proof-based research branches on universal labelings and finite-field constructions.

No GitHub Actions workflows are used.

## Main results

### Paper 1 — Universal labelings

**Universal Distance-Antimagic Labelings: Cyclic Tests, Signed-Sum Intervals, and Complementary Neighborhoods**

Overview: [`paper1_universal/README.md`](paper1_universal/README.md)

The current draft proves, among other results:

1. Every bijection `V(G) -> Z_n` is distance antimagic iff every bijection into every abelian group of order `n` is distance antimagic.
2. The only graphs with that all-group/all-labeling property are `K_n` and, for even `n`, the perfect matching.
3. Universal cyclic subset-sum systems with at least three members are exactly Johnson stars and tops.
4. Signed sums of two disjoint subsets of `[n]` with prescribed cardinalities have an exact support formula, yielding the cancellation/range/parity criterion for ordinary labels.
5. Structural consequences include classifications for cluster graphs and forests, joined clique–matching families, and a connected non-cograph family; order 10 is the first possible non-cograph order.
6. For `F_2^m`, the universal graphs are exactly Seidel switchings of the complete graph or a perfect matching.
7. Complementary-neighborhood, anti-period, and phantom-period phenomena are classified or constructed in the stated settings.

The fixed noncyclic pair problem for general abelian groups of exponent greater than two remains explicitly open.

### Paper 2 — Finite-field constructions

**Nonlinear Group-Distance-Antimagic Labelings from Affine-Line Filters**

Overview: [`paper2_finite_field/README.md`](paper2_finite_field/README.md)

This branch develops algebraic constructions for group-distance-antimagic Cayley graphs over finite fields. The draft contains dimension-three families, higher-dimensional scalar constructions, root-of-unity constructions in odd dimensions, a dimension-two limitation for the full affine-line architecture, and explicit checked finite-field examples.

Together, the constructions give nonlinear distance-antimagic examples in every dimension at least three for infinitely many odd characteristics, even in regimes where additive automorphism labelings are distance magic.

### Paper 3 — Exhaustive order-nine theorem

The original repository materials establish the finite theorem:

> A simple graph on at most nine vertices is distance antimagic iff its open neighborhoods are pairwise distinct.

For order nine, all **274,668** unlabeled simple graph classes were classified. Exactly **205,914** have distinct open neighborhoods and every one received an explicit labeling certificate; the remaining **68,754** fail by the repeated-neighborhood obstruction. Two independent verifiers accepted every positive certificate with zero failures.

See [`ORDER9_README.md`](ORDER9_README.md), [`RESULTS.md`](RESULTS.md), [`paper/`](paper/), [`code/`](code/), [`data/`](data/), and [`results/`](results/) for the original order-nine publication and reproduction layout.

## Reproduction

The original order-nine computation remains reproducible directly from this repository:

```bash
bash reproduce.sh primary
```

or, for the broader original audit:

```bash
bash reproduce.sh full
```

The proof-based branches were also developed with finite regression checks for signed-sum supports, constructive witnesses, small graph cases, elementary abelian two-groups, anti-period examples, and explicit finite-field certificates. Those computations are supporting checks rather than substitutes for the written general arguments.

## Repository map

```text
paper1_universal/       overview of the universal/group/integer branch
paper2_finite_field/    overview of the finite-field construction branch
notes/                  research status notes
paper/                   original order-nine paper materials
code/                    order-nine constructor and verifiers
data/                    order-nine catalogue provenance
results/                 order-nine results and certificate metadata
figures/                 order-nine figures
ORDER9_README.md         preserved original repository README
RELEASE_NOTES.md         current research-suite release notes
CITATION.cff             citation metadata
```

## Scope

These results do **not** solve the Kamatchi–Arumugam conjecture in general. The order-nine theorem moves its computational frontier; the universal-labeling and finite-field branches address different, stronger or group-valued quantifier regimes.

The new mathematical claims are research drafts, not peer-reviewed publications. Priority remains provisional pending specialist and database-level review. The repository deliberately records scope limitations and important proof repairs rather than presenting exploratory claims as settled results.

## AI and computational assistance

Large language models, computer algebra, exhaustive enumeration, SAT/search experiments, and exact verification code were used during exploration, error detection, proof auditing, and drafting. No AI system is an author. The retained mathematical claims are intended to be supported by written arguments, explicit computations, or cited literature; the human author is responsible for release and submission.

## Citation

Citation metadata for the current research suite is in [`CITATION.cff`](CITATION.cff). See [`RELEASE_NOTES.md`](RELEASE_NOTES.md) and [`notes/STATUS.md`](notes/STATUS.md) for the current release scope and status.
