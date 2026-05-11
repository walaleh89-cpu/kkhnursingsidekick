import pandas as pd

# =========================
# LOAD EXCEL FILE
# =========================
df = pd.read_excel("data/compatibility_master.xlsx")

# =========================
# LEGEND
# =========================
legend = {
    "C": "Compatible",
    "Ca": "Compatible if NaCl 0.9% used",
    "X": "Not compatible",
    "NI": "No information"
    "Ca = Compatible if diluent is NaCl 0.9%"
    "Cs = Based on solubility rules in Admixture and Y-site Compatibility of Additives in Intravenous Drips"
}

# =========================
# CONVERT MATRIX TO LONG FORMAT
# =========================
records = []

# Get all column drug names
drug_names = list(df.columns[1:])

# Loop through rows
for index, row in df.iterrows():

    # First column is drug name
    drug1 = row.iloc[0]

    # Loop through compatibility columns
    for drug2 in drug_names:

        value = row[drug2]

        # Skip empty cells
        if pd.isna(value):
            continue

        # Convert symbols into words
        compatibility = legend.get(
            str(value).strip(),
            str(value)
        )

        # Save record
        records.append({
            "Drug1": drug1,
            "Drug2": drug2,
            "Compatibility": compatibility
        })

# =========================
# CREATE DATAFRAME
# =========================
output_df = pd.DataFrame(records)

# =========================
# SAVE CSV
# =========================
output_df.to_csv(
    "data/compatibility.csv",
    index=False
)

print("compatibility.csv created successfully!")