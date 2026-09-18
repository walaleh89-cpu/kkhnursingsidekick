import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# DATABASE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR / "data" / "medication_database_v2.csv"
)


def load_database():

    if not DATA_FILE.exists():
        st.error("Medication database not found.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(
            DATA_FILE,
            dtype=str,
            keep_default_na=False
        )

        required = [
            "medication",
            "indication",
            "route",
            "min_dose_mg_per_kg",
            "max_dose_mg_per_kg",
            "dose_basis",
            "frequency_options",
            "remarks",
            "source",
            "version",
        ]

        missing = [
            col for col in required
            if col not in df.columns
        ]

        if missing:
            st.error(
                "Missing database columns: "
                + ", ".join(missing)
            )
            return pd.DataFrame()

        return df[
            df["medication"].str.strip() != ""
        ].copy()

    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


# ==========================================
# MAIN PAGE
# ==========================================

def run_medication_order_page():

    st.header(
        "💊 Paediatric Medication Order Assistant"
    )

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.warning(
        "DEMONSTRATION ONLY — Medication information "
        "has not been clinically validated. "
        "Do not use for prescribing."
    )

    df = load_database()

    if df.empty:
        st.info("No medications available.")
        return

    # ======================================
    # PATIENT INFORMATION
    # ======================================

    st.subheader("1. Patient Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        years = st.number_input(
            "Age (years)",
            min_value=0,
            max_value=18,
            value=3,
            step=1
        )

    with col2:
        months = st.number_input(
            "Additional months",
            min_value=0,
            max_value=11,
            value=0,
            step=1
        )

    with col3:
        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=300.0,
            value=0.0,
            step=0.1,
            format="%.2f"
        )

    st.caption(
        f"Age: {years} years {months} months | "
        f"Weight: {weight:.2f} kg"
    )

    st.divider()

    # ======================================
    # MEDICATION SELECTION
    # ======================================

    st.subheader("2. Medication Selection")

    medication = st.selectbox(
        "Medication",
        sorted(df["medication"].unique()),
        index=None,
        placeholder="Select medication"
    )

    if medication is None:
        return

    med_df = df[
        df["medication"] == medication
    ]

    indication = st.selectbox(
        "Indication",
        sorted(med_df["indication"].unique()),
        index=None,
        placeholder="Select indication"
    )

    if indication is None:
        return

    indication_df = med_df[
        med_df["indication"] == indication
    ]

    route = st.selectbox(
        "Route",
        sorted(indication_df["route"].unique()),
        index=None,
        placeholder="Select route"
    )

    if route is None:
        return

    selected = indication_df[
        indication_df["route"] == route
    ]

    if len(selected) != 1:
        st.error(
            "Multiple medication records found. "
            "Please review the database."
        )
        return

    row = selected.iloc[0]

    st.divider()

    # ======================================
    # GUIDELINE INFORMATION
    # ======================================

    st.subheader("3. Medication Reference")

    st.write(
        f"**Medication:** {row['medication']}"
    )

    st.write(
        f"**Indication:** {row['indication']}"
    )

    st.write(
        f"**Route:** {row['route']}"
    )

    st.write(
        "**Reference dose range:** "
        f"{row['min_dose_mg_per_kg']}–"
        f"{row['max_dose_mg_per_kg']} "
        f"{row['dose_basis']}"
    )

    st.write(
        "**Reference frequency options:** "
        + row["frequency_options"].replace("|", " or ")
        + " hours"
    )

    st.write(
        f"**Formulation:** {row['formulation']}"
    )

    st.write(
        f"**Remarks:** {row['remarks']}"
    )

    st.caption(
        f"Source: {row['source']} | "
        f"Version: {row['version']}"
    )

    st.divider()

    # ======================================
    # CALCULATION STATUS
    # ======================================

    st.subheader("4. Dose Calculation")

    st.info(
        "Patient-specific dose calculation and "
        "suggested medication orders are not enabled "
        "for this unverified medication dataset."
    )

    st.warning(
        "Before enabling calculations, confirm "
        "age restrictions, dose ranges, maximum "
        "single and daily doses, formulation "
        "selection and rounding rules."
    )

    st.divider()

    st.subheader("5. Safety Reminders")

    st.warning(
        "Independently verify patient identity, "
        "current weight, allergies, indication, "
        "contraindications, interactions and "
        "renal/hepatic suitability where applicable."
    )