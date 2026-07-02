import json
import pandas as pd
from pathlib import Path

for path in sorted(Path("data/raw").glob("*.json")):
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    df = pd.DataFrame(rows)
    value_col = "quantity" if "quantity" in df.columns else "value"
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    print(f"\n=== {path.name} ===")
    print(f"  rows: {len(df)}")
    print(f"  period range: {df['period'].min()} -> {df['period'].max()}")
    null_pct = df[value_col].isna().mean() * 100
    print(f"  null/non-numeric '{value_col}': {null_pct:.1f}%")
    print(f"  columns: {list(df.columns)}")