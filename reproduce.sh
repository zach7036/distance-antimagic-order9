#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
MODE="${1:-primary}"
OUT="generated"
mkdir -p "$OUT"
EXPECTED_GRAPH9="839f67ecc73b1f539128694badebe27adf4f0fb1ee6d0663b7ad9868100d5123"
EXPECTED_PRIMARY="da32bb36f59a8999c735b4d1d585b372d9de665facc1c2ae3e55fb0025516bf1"
EXPECTED_REPLAY="92c3028274ce50ca21694f598536012ad8f4f1bcd2e1145be6aa7f523dcfcd36"

hash_of() {
  python3 - "$1" <<'PY_HASH'
import hashlib, sys
h = hashlib.sha256()
with open(sys.argv[1], "rb") as f:
    for block in iter(lambda: f.read(1 << 20), b""):
        h.update(block)
print(h.hexdigest())
PY_HASH
}

require_hash() {
  local file="$1" expected="$2" actual
  actual="$(hash_of "$file")"
  if [[ "$actual" != "$expected" ]]; then
    echo "HASH MISMATCH: $file" >&2
    echo "expected: $expected" >&2
    echo "actual:   $actual" >&2
    exit 1
  fi
  echo "OK $actual  $file"
}

python3 code/download_catalogues.py 9
require_hash data/graph9.g6 "$EXPECTED_GRAPH9"
CXX="${CXX:-g++}"
"$CXX" -std=c++20 -O3 -Wall -Wextra -Wpedantic code/distance_antimagic_search.cpp -o "$OUT/distance_antimagic_search"

echo "== Deterministic primary reconstruction =="
"$OUT/distance_antimagic_search" data/graph9.g6 "$OUT/order9_primary" 20260807 20000
require_hash "$OUT/order9_primary_certificates.tsv" "$EXPECTED_PRIMARY"
python3 code/verify_certificates_stdlib.py data/graph9.g6 "$OUT/order9_primary_certificates.tsv" "$OUT/order9_primary_verification_stdlib.json"

if python3 - <<'PY_NX' >/dev/null 2>&1
import networkx
PY_NX
then
  python3 code/verify_certificates.py data/graph9.g6 "$OUT/order9_primary_certificates.tsv" "$OUT/order9_primary_verification_networkx.json"
else
  echo "NetworkX not installed; the standard-library verifier completed. Install requirements.txt to run the second verifier."
fi

python3 - "$OUT/order9_primary_verification_stdlib.json" <<'PY_ASSERT'
import json, sys
x = json.load(open(sys.argv[1], encoding="utf-8"))
assert x["total_graphs"] == 274668
assert x["point_determining_graphs"] == 205914
assert x["repeated_neighborhood_graphs"] == 68754
assert x["certificates_verified"] == 205914
assert x["failures"] == 0
print("PASS: 274,668 classes classified; 205,914 certificates verified; 0 failures.")
PY_ASSERT

if [[ "$MODE" == "primary" ]]; then
  exit 0
fi
if [[ "$MODE" != "full" ]]; then
  echo "Usage: bash reproduce.sh [primary|full]" >&2
  exit 2
fi

echo "== Different-seed/tiny-pool replay =="
"$OUT/distance_antimagic_search" data/graph9.g6 "$OUT/order9_replay_seed8675309_pool20" 8675309 20
require_hash "$OUT/order9_replay_seed8675309_pool20_certificates.tsv" "$EXPECTED_REPLAY"
python3 code/verify_certificates_stdlib.py data/graph9.g6 "$OUT/order9_replay_seed8675309_pool20_certificates.tsv" "$OUT/order9_replay_verification_stdlib.json"

echo "== Lower-order reproduction =="
python3 code/generate_lower_catalogues.py
python3 code/download_catalogues.py 8
for n in 1 2 3 4 5 6 7 8; do
  "$OUT/distance_antimagic_search" "data/graph${n}.g6" "$OUT/order${n}_replication" 20260807 20000
  python3 code/verify_certificates_stdlib.py "data/graph${n}.g6" "$OUT/order${n}_replication_certificates.tsv" "$OUT/order${n}_verification_stdlib.json"
done

echo "== Exact hard-case witness counts =="
python3 code/count_exact_labelings_sample.py
if [[ "${RUN_SLOW_RECOUNT:-0}" == "1" ]]; then
  DISTANCE_ANTIMAGIC_RECOUNT_PROCESSES="${DISTANCE_ANTIMAGIC_RECOUNT_PROCESSES:-1}" python3 code/recount_exact_labelings_stdlib.py
else
  echo "Skipping the slower pure-Python independent recount. Run RUN_SLOW_RECOUNT=1 bash reproduce.sh full to include it."
fi

echo "Full computational replay complete. Outputs are under generated/."
