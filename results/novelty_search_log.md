# Novelty search log

**Search date:** 8 August 2026  
**Target result:** exhaustive verification of the Kamatchi-Arumugam distance-antimagic open-neighborhood conjecture for all simple unlabeled graphs of order 9.

## Terminology used

The search deliberately included synonymous or adjacent terminology:

- distance antimagic; distance-antimagic; `{1}`-antimagic; `D={1}` antimagic
- identical open neighborhoods; identical neighborhoods; neighborhood twins; `{1}`-twins
- point-determining graph; mating graph
- order 9; order nine; 9 vertices; nine vertices
- exhaustive; computationally verified; all non-isomorphic graphs; nauty; graph6

## Candidate screening

1. **Order-9 extension of the distance-antimagic conjecture (selected).** The 2021 paper *Another Antimagic Conjecture* explicitly reports exhaustive agreement only through order 8. A 2025 preprint on oriented linear forests still states that the conjecture had been computationally verified through order 8. Exact and synonym-expanded searches found no order-9 exhaustive result or certificate archive.
2. **New construction for a familiar graph family (rejected).** Product graphs, circulants, Mycielskian graphs, splitting graphs, shadow graphs, and several other standard families have recent dedicated papers (2022-2026). A family result would therefore require a delicate new construction and was less likely to be both novel and conclusively finishable in the available computation window.
3. **Exact witness-count distribution for every eligible order-9 graph (rejected as primary question).** This appears unreported, but a direct complete calculation would test 205,914 x 9! = 74,722,072,320 labelings. It was retained as a robustness sub-study on a deliberately difficult 33-graph sample rather than the central objective.
4. **Exhaustive order-10 extension (deferred).** The official catalogue contains 12,005,168 unlabeled order-10 graphs, over 43 times the order-9 catalogue. The search itself may be feasible, but generating, independently replaying, auditing, and packaging millions of explicit certificates would exceed the intended scope of a carefully validated single-session study.

## Result-specific searches

Representative exact searches included:

- `"distance antimagic" graph order 9 exhaustive`
- `"distance antimagic" "order nine" graph`
- `"all graphs of order 9" "distance antimagic"`
- `"computationally verified" "distance antimagic" "order 9"`
- `"205914" "distance antimagic"`
- `"274668" "distance antimagic"`
- `"point-determining" "distance antimagic" order 9`
- `"mating graph" "distance antimagic"`
- graph6 strings for the two hardest replay cases, together with `distance antimagic`

Sources checked included the original JCMCC article, the 2021 Symmetry article and repository copy, publisher pages for 2022-2026 family results, arXiv, AIMS Mathematics, IJETT, the Australian National University/Brendan McKay graph catalogue, OEIS entries A004110 and A004108, and the Gessel-Li point-determining graph paper.

## Closest prior work

- Kamatchi and Arumugam (2013) introduced distance-antimagic graphs and stated the open-neighborhood conjecture.
- Simanjuntak et al. (2021) performed an exhaustive search through order 8: 8,047 of 12,346 order-8 graphs had distinct open neighborhoods, and all 8,047 were distance-antimagic.
- Later work through 2026 continues to present evidence for special graph families; a 2025 paper explicitly describes the computational frontier as order 8.
- The number 205,914 was already known independently as the number of unlabeled order-9 point-determining (mating) graphs. Thus, that count is not claimed as new. What was not found in prior work was an existence certificate for a distance-antimagic labeling for every one of those 205,914 classes.

## Qualified novelty conclusion

As of 8 August 2026, the literature and result-specific searches located no prior exhaustive order-9 verification, no archive of 205,914 order-9 distance-antimagic certificates, and no published corollary excluding counterexamples below 10 vertices. The result therefore **appears to be a previously unreported computational extension from order 8 to order 9**. This is necessarily a qualified novelty claim: unindexed, unpublished, or inaccessible work cannot be ruled out by web and literature searches alone.
