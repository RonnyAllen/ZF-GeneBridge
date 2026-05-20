import json
import os
import re

print("=== STARTING INTEGRITY CHECK ===")

# 1. Check database files existence
db_files = ["summary.json", "stage_order.json", "hints.json"]
for dbf in db_files:
    if os.path.exists(dbf):
        print(f"  [OK] {dbf} exists. Size: {os.path.getsize(dbf)} bytes")
        with open(dbf, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"       Successfully loaded {dbf} as JSON.")
            if dbf == "summary.json":
                print(f"       Total genes: {len(data)}")
                # Check casing
                bad_cases = [k for k in data.keys() if k != k.lower()]
                if bad_cases:
                    print(f"       [ERROR] Non-lowercase keys in summary.json: {bad_cases[:5]}")
                else:
                    print(f"       [OK] All keys in summary.json are lowercase.")
    else:
        print(f"  [ERROR] {dbf} is missing!")

# 2. Check stage_order.json integrity
with open("stage_order.json", "r", encoding="utf-8") as f:
    stages = json.load(f)
print(f"  [OK] Loaded stage_order.json with {len(stages)} stages.")

# Check key genes
with open("summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

for test_gene in ["march1", "pparg", "tp53", "sox10"]:
    if test_gene in summary:
        g = summary[test_gene]
        print(f"  [OK] Found test gene '{test_gene}':")
        print(f"       ID: {g['id']}")
        print(f"       Name: {g['name']}")
        print(f"       Stages Count: {len(g['stages'])}")
        print(f"       Tissues (first 3): {g['tissues'][:3]}")
    else:
        print(f"  [WARNING] Test gene '{test_gene}' not found in summary.json")

# 3. Check split databases
split_dir = "data"
files = os.listdir(split_dir)
print(f"  [OK] Found {len(files)} files in split folder 'data/'")

# Check lowercase of all keys in a sample split file
go_p_path = "data/go_p.json"
if os.path.exists(go_p_path):
    with open(go_p_path, "r", encoding="utf-8") as f:
        go_p = json.load(f)
    bad_keys = [k for k in go_p.keys() if k != k.lower()]
    if bad_keys:
        print(f"  [ERROR] Non-lowercase keys in go_p.json: {bad_keys[:5]}")
    else:
        print(f"  [OK] All keys in go_p.json are lowercase.")
else:
    print(f"  [WARNING] {go_p_path} is missing!")

print("=== INTEGRITY CHECK COMPLETE ===")
