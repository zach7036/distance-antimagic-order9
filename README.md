# Distance-Antimagic Research Suite

**Release:** 1.1.0 (August 13, 2026)  
**Author:** Zach Waddle  
**Status:** publication drafts and reproducibility materials; not yet peer reviewed

This repository is the public home for a connected program of research on distance-antimagic graph labelings. It began as the exhaustive order-nine computation and now also contains two proof-based manuscripts on universal labelings and nonlinear finite-field constructions.

No GitHub Actions workflows are used. Verification is intended to be run explicitly and locally.

## Main results

### Paper 1 — Universal labelings

**Universal Distance-Antimagic Labelings: Cyclic Tests, Signed-Sum Intervals, and Complementary Neighborhoods**

Source: [`paper1_universal/main.tex`](paper1_universal/main.tex)

Among the results proved in the manuscript:

1. Every bijection `V(G) -> Z_n` is distance antimagic iff every bijection into every abelian group of order `n` is distance antimagic.
2. The only graphs with that all-group/all-labeling property are `K_n` and, for even `n`, the perfect matching.
3. Universal cyclic subset-sum systems with at least three members are exactly Johnson stars and tops.
4. The signed sums of two disjoint subsets of `[n]` with prescribed cardinalities are determined exactly, yielding the cancellation/range/parity criterion for pairs separated under every ordinary integer labeling.
5. Structural consequences include exact classifications for cluster graphs and forests, joined clique–matching families, and an infinite connected non-cograph family; order 10 is the first possible non-cograph order.
6. For `F_2^m`, a pair is separated under every labeling exactly at neighborhood-row Hamming distance `2` or `2^m-2`; the universal graphs are exactly Seidel switchings of `K_(2^m)` or a perfect matching.
7. Inverse-closed Cayley anti-periods and a connected twin-free phantom-period obstruction family are classified/constructed.

The cyclic additive step uses Zoltan Lorant Nagy's classification of zero permutational sums. The fixed noncyclic pair problem for general groups of exponent greater than two remains explicitly open.

### Paper 2 — Nonlinear finite-field constructions

**Nonlinear Group-Distance-Antimagic Labelings from Affine-Line Filters**

Source: [`paper2_finite_field/main.tex`](paper2_finite_field/main.tex)

The manuscript develops translation-sum/Hasse-derivative filters that send nonlinear permutation monomials to permutation weight maps. Results include:

1. a general paired affine-line norm criterion;
2. a connected `4p`-regular dimension-three family on `F_(p^3)` for `p != 4 (mod 7)`;
3. scalar-weight constructions in every admissible even dimension at least four;
4. root-of-unity balancing in every fixed odd dimension at least five for infinitely many primes;
5. therefore nonlinear escapes in every dimension `m >= 3` for infinitely many odd characteristics;
6. a dimension-two impossibility theorem for the full affine-line architecture;
7. explicit checked certificates over `F_27`, `F_(7^4)`, and an `F_(11^5)` example.

The finite-field identities themselves are classical in character; the proposed contribution is their systematic graph-labeling application.

### Paper 3 — Exhaustive order-nine theorem

The original repository materials establish the finite theorem:

> A simple graph on at most nine vertices is distance antimagic iff its open neighborhoods are pairwise distinct.

For order nine, all **274,668** unlabeled simple graph classes were classified. Exactly **205,914** have distinct open neighborhoods and every one received an explicit labeling certificate; the remaining **68,754** fail by the repeated-neighborhood obstruction. Two independent verifiers accepted every positive certificate with zero failures.

See [`ORDER9_README.md`](ORDER9_README.md), [`RESULTS.md`](RESULTS.md), [`paper/`](paper/), [`code/`](code/), [`data/`](data/), and [`results/`](results/) for the original order-nine publication and reproduction layout.

## Verification

Proof-regression and construction checks for Papers 1–2 are in [`verification/`](verification/). The archived test suite covers, among other things:

- exact signed-sum supports and constructive witnesses;
- universal cyclic and integer labeling tests on every atlas graph through order seven;
- structural integer families and the non-cograph frontier;
- elementary-abelian-2 pair and switching theory;
- anti-period and phantom-period families;
- exponent/gcd reductions and root-of-unity scalar constructions;
- explicit finite-field certificates.

The order-nine computation retains its original deterministic reproduction workflow:

```bash
bash reproduce.sh primary
```

For Papers 1–2, install the small Python dependency set with:

```bash
python3 -m pip install -r verification/requirements.txt
```

and run the individual `verification/verify_*.py` programs.

## Repository map

```text
paper1_universal/       universal/group/integer theorem manuscript
paper2_finite_field/    nonlinear finite-field construction manuscript
verification/           theorem and construction regression checks
notes/                  publication, literature, and proof-audit records
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

These results do **not** solve the Kamatchi–Arumugam conjecture in general. The order-nine theorem moves its computational frontier; the universal-labeling and finite-field papers address different, stronger or group-valued quantifier regimes.

The manuscripts are rigorous research drafts, not peer-reviewed publications. Priority remains provisional pending specialist/database review. The repository records known corrections, failed intermediate claims, proof repairs, and computational checks rather than hiding them.

## AI/computational assistance

Large language models, computer algebra, exhaustive enumeration, SAT/search experiments, and exact verification code were used during exploration, error detection, proof auditing, and drafting. No AI system is an author. Every retained mathematical claim is supported by a written proof, explicit computation, or cited literature; the human author is responsible for release and submission.

## Citation and licensing

See [`CITATION.cff`](CITATION.cff), [`LICENSE-CODE.txt`](LICENSE-CODE.txt), [`LICENSE-DOCUMENTATION.txt`](LICENSE-DOCUMENTATION.txt), and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
