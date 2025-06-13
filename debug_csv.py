import pandas as pd

df = pd.read_csv("backend/runs_log.csv")
print("🧩 Columns in CSV:", df.columns.tolist())
print("🔍 First row:")
print(df.head(1).to_string())
