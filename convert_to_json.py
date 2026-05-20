import pandas as pd
import json
import os
import datetime

excel_file = "Latest_ZF_GeneExpression_Gene2Disease_GO_Collated.xlsx"
print("Starting Excel conversion to optimized JSON...")

def clean_dataframe(df):
    # Convert any datetime columns to string
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Convert dataframe to records
    records = df.to_dict(orient='records')
    
    # Deep clean cells: convert any remaining timestamp/datetime or float NaN to serializable equivalents
    clean_records = []
    for r in records:
        clean_row = {}
        for k, v in r.items():
            if pd.isna(v):
                clean_row[k] = None
            elif isinstance(v, (datetime.datetime, datetime.date, pd.Timestamp)):
                clean_row[k] = v.isoformat()
            else:
                clean_row[k] = v
        clean_records.append(clean_row)
    return clean_records

# 1. Stage Order
print("Loading Stage Order...")
df_stage = pd.read_excel(excel_file, sheet_name="Stage Order", header=None)
stage_order = []
for col in df_stage.columns:
    for val in df_stage[col].dropna():
        v = str(val).strip()
        if v:
            name = v.split(':')[0].strip() if ':' in v else v.strip()
            if name and name not in stage_order:
                stage_order.append(name)
with open("stage_order.json", "w", encoding="utf-8") as f:
    json.dump(stage_order, f, ensure_ascii=False)
print("Saved stage_order.json")

# 2. Summary
print("Loading 20260518_wtexpression_Summary...")
df_sum = pd.read_excel(excel_file, sheet_name="20260518_wtexpression_Summary")
sum_cols = {
    'Gene Symbol': 'geneSymbol',
    'Super Structure Name': 'superStructure',
    'Start Stage': 'startStage',
    'End Stage': 'endStage',
    'Assay': 'assay'
}
df_sum = df_sum[list(sum_cols.keys())].rename(columns=sum_cols)
df_sum = df_sum.dropna(subset=['geneSymbol'])
summary_data = clean_dataframe(df_sum)
with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary_data, f, ensure_ascii=False)
print("Saved summary.json")

# 3. Disease
print("Loading 20260519_gene2DiseaseOrthology...")
df_dis = pd.read_excel(excel_file, sheet_name="20260519_gene2DiseaseOrthology")
dis_cols = {
    'Zebrafish Gene ID': 'zebrafishGeneId',
    'Zebrafish Gene Symbol': 'geneSymbol',
    'Human Ortholog Entrez Gene Id': 'humanGeneId',
    'Human Ortholog Symbol': 'humanGeneSymbol',
    'DO Term Name': 'doName',
    'DO Term ID': 'doId',
    'OMIM Term Name': 'omimName',
    'OMIM ID': 'omimId',
    'Evidence Code': 'evidenceCode',
    'Publication': 'publication'
}
dis_cols_present = {k: v for k, v in dis_cols.items() if k in df_dis.columns}
df_dis = df_dis[list(dis_cols_present.keys())].rename(columns=dis_cols_present)
df_dis = df_dis.dropna(subset=['geneSymbol'])
disease_data = clean_dataframe(df_dis)
with open("disease.json", "w", encoding="utf-8") as f:
    json.dump(disease_data, f, ensure_ascii=False)
print("Saved disease.json")

# 4. GO
print("Loading 20260519_GeneOntology...")
df_go = pd.read_excel(excel_file, sheet_name="20260519_GeneOntology")
go_cols = {
    'Gene Symbol': 'geneSymbol',
    'GO Term ID': 'goId',
    'GO Evidence Code': 'evidence',
    'Reference ID': 'refId',
    'Ontology: P=Biological Process; F=Molecular Function; C=Cellular Component': 'ontology',
    'Marker Name': 'markerName'
}
go_cols_present = {k: v for k, v in go_cols.items() if k in df_go.columns}
df_go = df_go[list(go_cols_present.keys())].rename(columns=go_cols_present)
df_go = df_go.dropna(subset=['geneSymbol'])
go_data = clean_dataframe(df_go)
with open("go.json", "w", encoding="utf-8") as f:
    json.dump(go_data, f, ensure_ascii=False)
print("Saved go.json")

# 5. Detailed Expression
print("Loading 20260518_zf_wt_expression...")
df_exp = pd.read_excel(excel_file, sheet_name="20260518_zf_wt_expression")
exp_cols = {
    'Gene ID': 'geneId',
    'Gene Symbol': 'geneSymbol',
    'Fish Name': 'fishName',
    'Super Structure Name': 'superStructure',
    'Sub Structure Name': 'subStructure',
    'Start Stage': 'startStage',
    'End Stage': 'endStage',
    'Assay': 'assay',
    'Assay MMO ID': 'assayMmoId',
    'Publication ID': 'publicationId',
    'Probe ID': 'probeId',
    'Antibody ID': 'antibodyId',
    'Fish ID': 'fishId'
}
exp_cols_present = {k: v for k, v in exp_cols.items() if k in df_exp.columns}
df_exp = df_exp[list(exp_cols_present.keys())].rename(columns=exp_cols_present)
df_exp = df_exp.dropna(subset=['geneSymbol'])
expression_data = clean_dataframe(df_exp)
with open("expression.json", "w", encoding="utf-8") as f:
    json.dump(expression_data, f, ensure_ascii=False)
print("Saved expression.json")

print("All Excel sheets successfully converted to optimized JSON!")
