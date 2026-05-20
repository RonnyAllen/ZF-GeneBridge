import pandas as pd
excel_file = "Latest_ZF_GeneExpression_Gene2Disease_GO_Collated.xlsx"
xl = pd.ExcelFile(excel_file)

# Stage Order sheet
print("--- STAGE ORDER VALUES ---")
df_stage = xl.parse("Stage Order", header=None)
stages_order_list = []
for col in df_stage.columns:
    for val in df_stage[col].dropna():
        stages_order_list.append(str(val).strip())
print("Stage Order List (first 10):", stages_order_list[:10])
print("Stage Order List (total count):", len(stages_order_list))

# Expression sheet start/end stages
print("\n--- EXPRESSION SHEET STAGES ---")
df_exp = xl.parse("20260518_zf_wt_expression")
start_stages = df_exp['Start Stage'].dropna().unique()
end_stages = df_exp['End Stage'].dropna().unique()
print("Unique Start Stages (first 10):", start_stages[:10])
print("Unique End Stages (first 10):", end_stages[:10])

# Check mismatches
print("\n--- CHECK MISMATCHES ---")
mismatch_start = [s for s in start_stages if s not in stages_order_list]
mismatch_end = [e for e in end_stages if e not in stages_order_list]
print("Mismatched Start Stages:", mismatch_start)
print("Mismatched End Stages:", mismatch_end)

# Let's inspect some of the datetime values in columns
print("\n--- DETECT DATETIME CONVERSIONS ---")
date_genes_go = []
df_go = xl.parse("20260519_GeneOntology")
for sym in df_go['Gene Symbol'].dropna().unique():
    if not isinstance(sym, str):
        print("Non-string GO Gene Symbol:", sym, type(sym))
