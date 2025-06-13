import csv
import ast
import pandas as pd

input_file = "backend/runs_log.csv"
cleaned_file = "backend/runs_log_cleaned.csv"

# Step 1: Clean quotes and save properly quoted CSV
with open(input_file, "r", encoding="utf-8") as infile, open(cleaned_file, "w", newline='', encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    if "results" not in header:
        header.append("results")
    writer.writerow(header)

    for row in reader:
        # If results exists in this row
        if len(row) > 4:
            joined = ",".join(row[4:])  # join all parts of the JSON-like list
            row = row[:4] + [joined.replace("'", '"')]  # fix quote style
        elif len(row) < 5:
            row += [""]
        writer.writerow(row)

# Step 2: Load cleaned version
df = pd.read_csv(cleaned_file)
df.columns = df.columns.str.strip()

# Step 3: Flatten JSON from 'results' column
flattened_data = []
for _, row in df.iterrows():
    try:
        if pd.notna(row["results"]) and row["results"].strip():
            results = ast.literal_eval(row["results"])
            for block in results:
                flattened_data.append({
                    "timestamp": row["timestamp"],
                    "memory_blocks": row["memory_blocks"],
                    "delay": row["delay"],
                    "memory_type": row["memory_type"],
                    "block_id": block["block_id"],
                    "transfer_time": block["transfer_time"]
                })
    except Exception as e:
        print(f"❌ Error parsing row: {e}")
        continue

# Step 4: Save to final CSV
processed_df = pd.DataFrame(flattened_data)
processed_df.to_csv("processed_runs.csv", index=False)
print("✅ Flattened log saved to 'processed_runs.csv'")
