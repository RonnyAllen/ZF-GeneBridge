import pandas as pd
import json
import os

excel_file = "Latest_ZF_GeneExpression_Gene2Disease_GO_Collated.xlsx"
print("File size:", os.path.getsize(excel_file), "bytes")

xl = pd.ExcelFile(excel_file)
print("Sheets in workbook:", xl.sheet_names)

for sheet in xl.sheet_names:
    df = xl.parse(sheet)
    print(f"Sheet: {sheet}, Shape: {df.shape}, Columns: {df.columns.tolist()[:10]}")
