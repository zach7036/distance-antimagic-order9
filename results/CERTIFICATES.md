# Complete certificate archives

The completed computation produced two complete order-nine TSV archives, each containing one certificate for every one of the **205,914** eligible graph isomorphism classes. They are deliberately not embedded in this repository as opaque encoded upload chunks. Instead, `./reproduce.sh primary` regenerates the canonical archive deterministically from the published C++ source and authoritative graph catalogue.

Expected SHA-256 values:

```text
da32bb36f59a8999c735b4d1d585b372d9de665facc1c2ae3e55fb0025516bf1  generated/order9_primary_certificates.tsv
92c3028274ce50ca21694f598536012ad8f4f1bcd2e1145be6aa7f523dcfcd36  generated/order9_replay_seed8675309_pool20_certificates.tsv
```

The first archive was generated with seed `20260807` and initial pool size `20000`. The independent replay used seed `8675309` and pool size `20`, deliberately forcing the fallback branch on 1,440 graphs.

`order9_certificate_sample.tsv` contains a small human-readable sample, including the hardest primary search-rank case.
