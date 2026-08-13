# Distance-antimagic conjecture through order nine

**Canonical theory/research repository:** https://github.com/zach7036/distance-antimagic-research

This repository is the dedicated computational archive for the exhaustive order-nine distance-antimagic study.

## Finite theorem

Every simple graph on at most nine vertices is distance antimagic if and only if its open neighborhoods are pairwise distinct.

At order nine, all 274,668 unlabeled simple graph classes were processed. Exactly 205,914 have distinct open neighborhoods and every one received an explicit distance-antimagic labeling certificate. The remaining 68,754 contain a repeated open neighborhood and fail necessarily. Two independent verifiers accepted all positive certificates with zero failures.

## Reproduction

```bash
python3 -m pip install -r requirements.txt
bash reproduce.sh primary
bash reproduce.sh full
```

See `paper/`, `RESULTS.md`, `code/`, `data/`, `results/`, and `figures/` for the complete study and reproducibility materials.

The broader universal-labeling, group-valued, and finite-field results are intentionally kept in the canonical research repository linked above. This finite result does not solve the Kamatchi-Arumugam conjecture in general.
