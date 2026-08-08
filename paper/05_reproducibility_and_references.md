# 13. Reproducibility

The repository contains:

- the C++20 certificate constructor;
- two independent certificate verifiers;
- a hash-checked order-eight and order-nine catalogue downloader;
- deterministic lower-order catalogue generation from NetworkX's Graph Atlas;
- exact result tables and verification JSON;
- a human-readable certificate sample;
- SHA-256 identifiers for both complete 205,914-row archives;
- local reproduction commands.

The central replay is:

```bash
python3 -m pip install -r requirements.txt
bash reproduce.sh primary
```

This command:

1. downloads `graph9.g6` from Brendan McKay's ANU catalogue;
2. rejects it unless its SHA-256 is exactly `839f67ecc73b1f539128694badebe27adf4f0fb1ee6d0663b7ad9868100d5123`;
3. compiles the C++20 constructor with warning flags;
4. regenerates the canonical 205,914-row certificate archive using seed `20260807` and pool size `20000`;
5. rejects the archive unless its SHA-256 is exactly `da32bb36f59a8999c735b4d1d585b372d9de665facc1c2ae3e55fb0025516bf1`;
6. replays every certificate using the independent standard-library verifier;
7. also runs the NetworkX verifier when NetworkX is installed;
8. asserts the complete census and zero-failure totals.

The expanded replay is:

```bash
bash reproduce.sh full
```

It additionally regenerates the different-seed/tiny-pool archive, verifies its canonical digest, recreates the lower-order catalogues, and repeats orders one through eight.

No GitHub Actions workflow is required or included. Reproduction runs only when a researcher explicitly executes the local script.

## Certificate format

Every certificate row has the form:

```text
index  graph6  edges  search_rank  labels_v0_to_vn_minus_1  weights_v0_to_vn_minus_1
```

To check a row, decode the graph6 record, assign the listed labels to vertices in graph6 order, recompute each vertex's open-neighborhood sum, and verify that the listed weights agree and are pairwise distinct. The standard-library verifier implements this procedure without relying on the constructor or NetworkX.

## Canonical checksums

```text
839f67ecc73b1f539128694badebe27adf4f0fb1ee6d0663b7ad9868100d5123  graph9.g6
546a249902101c97d3aa590f93e53366854bd0a6f405aa59bdb32d25c57f845a  graph8.g6
da32bb36f59a8999c735b4d1d585b372d9de665facc1c2ae3e55fb0025516bf1  order9_primary_certificates.tsv
92c3028274ce50ca21694f598536012ad8f4f1bcd2e1145be6aa7f523dcfcd36  order9_replay_seed8675309_pool20_certificates.tsv
67ea1f465fa67cd4c7726829b6b977c5766100ab14eb4796d3be630a87b988d9  order8_replication_certificates.tsv
```

# 14. Conclusion

Previous exhaustive work verified the distance-antimagic open-neighborhood conjecture through order eight, while order nine remained unresolved. This study processed every one of the 274,668 unlabeled simple graph classes on nine vertices, classified 68,754 as necessarily obstructed, and constructed and independently verified certificates for all 205,914 eligible classes. Multiple independent and adversarial checks produced zero failures.

It is therefore now established computationally that a simple graph of order at most nine is distance-antimagic exactly when its open neighborhoods are pairwise distinct. Any counterexample to the general conjecture must have at least ten vertices.

# References

1. N. Kamatchi and S. Arumugam, “Distance Antimagic Graphs,” *Journal of Combinatorial Mathematics and Combinatorial Computing* **84** (2013), 61–67.
2. R. Simanjuntak, T. Nadeak, F. Yasin, K. Wijaya, N. Hinding, and K. A. Sugeng, “Another Antimagic Conjecture,” *Symmetry* **13**(11) (2021), 2071. DOI: 10.3390/sym13112071.
3. R. Simanjuntak and A. Tritama, “Distance Antimagic Product Graphs,” *Symmetry* **14**(7) (2022), 1411. DOI: 10.3390/sym14071411.
4. R. Y. Wulandari and R. Simanjuntak, “Distance Antimagic Labelings of Product Graphs,” *Electronic Journal of Graph Theory and Applications* **11**(1) (2023), 111–123. DOI: 10.5614/ejgta.2023.11.1.9.
5. S. Sy, R. Simanjuntak, T. Nadeak, K. A. Sugeng, and T. Tulus, “Distance Antimagic Labeling of Circulant Graphs,” *AIMS Mathematics* **9**(8) (2024), 21177–21188. DOI: 10.3934/math.20241028.
6. I. M. Gessel and J. Li, “Enumeration of Point-Determining Graphs,” *Journal of Combinatorial Theory, Series A* **118**(2) (2011), 591–612. DOI: 10.1016/j.jcta.2010.03.009.
7. OEIS Foundation, entries A004110, “Number of unlabeled mating graphs,” and A004108, “Number of connected unlabeled mating graphs,” accessed 8 August 2026.
8. B. D. McKay, “Combinatorial Data: Simple Graphs,” Australian National University, https://users.cecs.anu.edu.au/~bdm/data/graphs.html.
9. B. D. McKay and A. Piperno, “Practical Graph Isomorphism, II,” *Journal of Symbolic Computation* **60** (2014), 94–112. DOI: 10.1016/j.jsc.2013.09.003.
10. A. A. Hagberg, D. A. Schult, and P. J. Swart, “Exploring Network Structure, Dynamics, and Function Using NetworkX,” in *Proceedings of the 7th Python in Science Conference* (2008), 11–15.
