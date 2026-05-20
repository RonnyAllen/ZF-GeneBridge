import pandas as pd
excel_file = "Latest_ZF_GeneExpression_Gene2Disease_GO_Collated.xlsx"
xl = pd.ExcelFile(excel_file)

for sheet in xl.sheet_names:
    print(f"\nChecking sheet: {sheet}")
    df = xl.parse(sheet)
    for col in df.columns:
        # Find datetime-like types
        dt_rows = df[df[col].apply(lambda x: isinstance(x, (pd.Timestamp, type(pd.NaT)) ) or 'datetime' in str(type(x)))]
        if not dt_rows.empty:
            unique_vals = dt_rows[col].dropna().unique()
            if len(unique_vals) > 0:
                print(f"  Col '{col}' contains datetime objects:")
                for uv in unique_vals:
                    print(f"    Val: {uv} (type: {type(uv)})")
