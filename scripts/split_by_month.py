import pandas as pd
import os

INPUT_FILE = "data/stores_sales_forecasting.csv"
OUTPUT_DIR = "output"
DATE_COLUMN = "Order Date"

df = pd.read_csv(INPUT_FILE, encoding="latin1")

df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")

df = df.dropna(subset=[DATE_COLUMN])

df["year"] = df[DATE_COLUMN].dt.year
df["month"] = df[DATE_COLUMN].dt.month

for (year, month), group in df.groupby(["year", "month"]):
    folder_path = os.path.join(
        OUTPUT_DIR,
        f"year={year}",
        f"month={month:02d}"
    )

    os.makedirs(folder_path, exist_ok=True)

    output_file = os.path.join(folder_path, "sales.csv")
    group.drop(columns=["year", "month"]).to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

print("Done.")
