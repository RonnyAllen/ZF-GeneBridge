import pandas as pd
import json
import os
import datetime

excel_file = "Latest_ZF_GeneExpression_Gene2Disease_GO_Collated.xlsx"
print("Starting optimized Excel conversion with split files...")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def clean_val(val):
    if pd.isna(val):
        return ""
    if isinstance(val, (datetime.datetime, datetime.date, pd.Timestamp)):
        return val.isoformat()
    return str(val).strip()

def get_prefix(sym):
    if not sym:
        return "other"
    c = sym[0].lower()
    if c.isalnum():
        return c
    return "other"

# 1. Stage Order
print("Processing Stage Order...")
df_stage = pd.read_excel(excel_file, sheet_name="Stage Order", header=None)
stage_order = []
stage_index = {}
for col in df_stage.columns:
    for val in df_stage[col].dropna():
        v = str(val).strip()
        if v:
            name = v.split(':')[0].strip() if ':' in v else v.strip()
            if name and name not in stage_order:
                stage_index[name] = len(stage_order)
                stage_order.append(name)

with open("stage_order.json", "w", encoding="utf-8") as f:
    json.dump(stage_order, f, ensure_ascii=False)
print(f"Saved stage_order.json ({len(stage_order)} stages)")

# 2. Load Gene Ontology (for marker names and hasGo)
print("Loading 20260519_GeneOntology...")
df_go = pd.read_excel(excel_file, sheet_name="20260519_GeneOntology")
go_grouped = {}
marker_names = {} # geneSymbol -> full name

for _, row in df_go.iterrows():
    sym = clean_val(row.get('Gene Symbol'))
    if not sym:
        continue
    
    go_id = clean_val(row.get('GO Term ID'))
    ontology = clean_val(row.get('Ontology: P=Biological Process; F=Molecular Function; C=Cellular Component'))
    marker_name = clean_val(row.get('Marker Name'))
    
    if marker_name:
        marker_names[sym] = marker_name
        
    if sym not in go_grouped:
        go_grouped[sym] = {
            "name": marker_name,
            "go": []
        }
    elif marker_name and not go_grouped[sym]["name"]:
        go_grouped[sym]["name"] = marker_name
        
    if go_id:
        aspect = "Biological Process"
        if "Molecular Function" in ontology:
            aspect = "Molecular Function"
        elif "Cellular Component" in ontology:
            aspect = "Cellular Component"
            
        if not any(x['id'] == go_id for x in go_grouped[sym]["go"]):
            go_grouped[sym]["go"].append({
                "id": go_id,
                "o": aspect
            })

# Split go.json into go_{char}.json
go_split = {}
for sym, val in go_grouped.items():
    prefix = get_prefix(sym)
    if prefix not in go_split:
        go_split[prefix] = {}
    go_split[prefix][sym] = val

for prefix, data in go_split.items():
    with open(f"data/go_{prefix}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
print(f"Saved split go_{{char}}.json files ({len(go_split)} prefixes)")

# 3. Load Disease Orthology (for human orthologs and diseases)
print("Loading 20260519_gene2DiseaseOrthology...")
df_dis = pd.read_excel(excel_file, sheet_name="20260519_gene2DiseaseOrthology")
disease_grouped = {}

for _, row in df_dis.iterrows():
    sym = clean_val(row.get('Zebrafish Gene Symbol'))
    if not sym:
        continue
        
    human_sym = clean_val(row.get('Human Ortholog Symbol'))
    do_name = clean_val(row.get('DO Term Name'))
    omim_name = clean_val(row.get('OMIM Term Name'))
    
    if sym not in disease_grouped:
        disease_grouped[sym] = {
            "orth": [],
            "dis": []
        }
        
    if human_sym and human_sym not in disease_grouped[sym]["orth"]:
        disease_grouped[sym]["orth"].append(human_sym)
        
    dis_label = do_name
    if omim_name:
        dis_label = f"{do_name} ({omim_name})" if do_name else omim_name
    
    if dis_label and dis_label not in disease_grouped[sym]["dis"]:
        disease_grouped[sym]["dis"].append(dis_label)

# Split disease.json into disease_{char}.json
disease_split = {}
for sym, val in disease_grouped.items():
    prefix = get_prefix(sym)
    if prefix not in disease_split:
        disease_split[prefix] = {}
    disease_split[prefix][sym] = val

for prefix, data in disease_split.items():
    with open(f"data/disease_{prefix}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
print(f"Saved split disease_{{char}}.json files ({len(disease_split)} prefixes)")

# 4. Load Detailed Expression
print("Loading 20260518_zf_wt_expression...")
df_exp = pd.read_excel(excel_file, sheet_name="20260518_zf_wt_expression")
expr_grouped = {}
expr_stages = {} # geneSymbol -> set of stage indices

for _, row in df_exp.iterrows():
    sym = clean_val(row.get('Gene Symbol'))
    if not sym:
        continue
        
    gene_id = clean_val(row.get('Gene ID'))
    fish_name = clean_val(row.get('Fish Name'))
    super_struct = clean_val(row.get('Super Structure Name'))
    sub_struct = clean_val(row.get('Sub Structure Name'))
    start_stage = clean_val(row.get('Start Stage'))
    end_stage = clean_val(row.get('End Stage'))
    assay = clean_val(row.get('Assay'))
    publication = clean_val(row.get('Publication ID'))
    
    if sym not in expr_grouped:
        expr_grouped[sym] = []
        
    expr_grouped[sym].append({
        "s": start_stage,
        "e": end_stage,
        "t": super_struct,
        "sub": sub_struct,
        "a": assay,
        "f": fish_name,
        "p": publication,
        "id": gene_id
    })
    
    if sym not in expr_stages:
        expr_stages[sym] = set()
        
    idx_s = stage_index.get(start_stage)
    idx_e = stage_index.get(end_stage)
    if idx_s is not None and idx_e is not None:
        for i in range(idx_s, idx_e + 1):
            expr_stages[sym].add(i)

# Split expression.json into expression_{char}.json
expr_split = {}
for sym, val in expr_grouped.items():
    prefix = get_prefix(sym)
    if prefix not in expr_split:
        expr_split[prefix] = {}
    expr_split[prefix][sym] = val

for prefix, data in expr_split.items():
    with open(f"data/expression_{prefix}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
print(f"Saved split expression_{{char}}.json files ({len(expr_split)} prefixes)")

# 5. Compile summary.json (The compact gene catalog for filtering & results)
print("Building catalog summary.json...")
summary_catalog = {}

all_genes = set(expr_grouped.keys()).union(go_grouped.keys()).union(disease_grouped.keys())

for sym in all_genes:
    gene_id = ""
    if sym in expr_grouped and len(expr_grouped[sym]) > 0:
        gene_id = expr_grouped[sym][0]["id"]
    
    name = marker_names.get(sym, "")
    if not name and sym in go_grouped:
        name = go_grouped[sym]["name"]
        
    tissues = set()
    fish_lines = set()
    assays = set()
    pubs = set()
    
    if sym in expr_grouped:
        for r in expr_grouped[sym]:
            if r["t"]: tissues.add(r["t"])
            if r["f"]: fish_lines.add(r["f"])
            if r["a"]: assays.add(r["a"])
            if r["p"]: pubs.add(r["p"])
            
    start_idx = None
    end_idx = None
    indices = expr_stages.get(sym, set())
    if indices:
        start_idx = min(indices)
        end_idx = max(indices)
        
    start_stage = stage_order[start_idx] if start_idx is not None and start_idx < len(stage_order) else ""
    end_stage = stage_order[end_idx] if end_idx is not None and end_idx < len(stage_order) else ""
    
    summary_catalog[sym] = {
        "symbol": sym,
        "id": gene_id,
        "name": name,
        "fish": list(fish_lines),
        "tissues": list(tissues),
        "startStage": start_stage,
        "endStage": end_stage,
        "stages": list(indices),
        "assays": list(assays),
        "pubs": list(pubs),
        "hasDisease": sym in disease_grouped,
        "hasGo": sym in go_grouped
    }

with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary_catalog, f, ensure_ascii=False)
print(f"Saved summary.json ({len(summary_catalog)} genes in catalog)")

# 6. Preload vocabulary hints.json
print("Building preloaded vocabulary hints.json...")
vocab_symbols = set()
vocab_tissues = set()
name_to_symbol = {}

for sym, data in summary_catalog.items():
    vocab_symbols.add(sym)
    if data["name"]:
        name_to_symbol[data["name"].lower()] = sym
        
    for t in data["tissues"]:
        vocab_tissues.add(t)

for sym, data in disease_grouped.items():
    for orth in data["orth"]:
        vocab_symbols.add(orth)
        name_to_symbol[orth.lower()] = sym

hints_data = {
    "geneSymbols": sorted(list(vocab_symbols)),
    "tissues": sorted(list(vocab_tissues)),
    "nameToSymbol": name_to_symbol
}

with open("hints.json", "w", encoding="utf-8") as f:
    json.dump(hints_data, f, ensure_ascii=False)
print(f"Saved hints.json ({len(hints_data['geneSymbols'])} symbols, {len(hints_data['tissues'])} tissues)")

# Clean up large files that we replaced
for large_file in ["go.json", "disease.json", "expression.json"]:
    if os.path.exists(large_file):
        os.remove(large_file)
        print(f"Removed redundant global file: {large_file}")

print("All optimized, split JSON databases pre-compiled successfully!")
