# Results

## Finite theorem established by the computation

For every simple graph `G` with at most nine vertices, `G` is distance-antimagic **if and only if** its open neighborhoods are pairwise distinct. Therefore any counterexample to the general Kamatchi–Arumugam conjecture has at least 10 vertices.

## Order-nine census

| Class | Count | Result |
|---|---:|---|
| All unlabeled simple graphs | 274,668 | Exhaustively processed |
| Pairwise-distinct open neighborhoods | 205,914 | Every class has a verified distance-antimagic labeling |
| Repeated open neighborhood | 68,754 | Impossible by the equal-weight obstruction |
| Verification failures | 0 | Two independent verifiers agree |

Across orders 1–9, the study covers **288,266** graph isomorphism classes and **214,652** positive labeling certificates.

## Adversarial checks

- independent NetworkX and standard-library graph6 decoders both accepted all 205,914 primary certificates;
- a different seed and 20-permutation initial pool independently solved all eligible graphs and exercised the fallback branch on 1,440 cases;
- warning-clean, fresh, AddressSanitizer, and UndefinedBehaviorSanitizer constructor builds produced the same primary archive hash;
- all `9! = 362,880` labelings were tested for 33 deliberately difficult graphs (11,975,040 graph-labeling tests); the sparsest witness set still contained 17,190 valid labelings (4.737103%).

The full manuscript is in [`paper/study.md`](paper/study.md).
