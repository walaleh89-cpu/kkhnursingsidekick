import streamlit as st
import pandas as pd
from pathlib import Path
from decimal import Decimal, InvalidOperation


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "medication_database_v2.csv"


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
            "min_age_months",
            "max_age_months",
            "min_dose_mg_per_kg",
            "max_dose_mg_per_kg",
            "dose_basis",
            "frequency_options",
            "max_doses_per_day",
            "max_single_dose_mg",
            "max_daily_dose_mg",
            "max_daily_dose_mg_per_kg",
            "formulation",
            "concentration_mg_per_ml",
            "remarks",
            "source",
            "version",
        ]

        missing = [
            column for column in required
            if column not in df.columns
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


def parse_decimal(value):
    try:
        number = Decimal(str(value).strip())
        if not number.is_finite():
            return None
        return number
    except (InvalidOperation, ValueError, TypeError):
        return None


def display_number(value):
    return f"{value:,.2f}"


def run_medication_order_page():

    st.header("💊 Paediatric Medication Dose Calculator")

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.warning(
        "DEMONSTRATION ONLY — Medication reference data "
        "have not been clinically validated. Calculations "
        "must not be used for prescribing or administration."
    )

    df = load_database()

    if df.empty:
        st.info("No medications available.")
        return

    # =====================================
    # 1. PATIENT INFORMATION
    # =====================================

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
        weight_input = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=150.0,
            value=0.0,
            step=0.1,
            format="%.2f"
        )

    age_months = years * 12 + months

    if weight_input <= 0:
        st.info("Enter the patient's weight to continue.")
        return

    weight = Decimal(str(weight_input))

    st.divider()

    # =====================================
    # 2. MEDICATION SELECTION
    # =====================================

    st.subheader("2. Medication Selection")

    medication = st.selectbox(
        "Medication",
        sorted(df["medication"].unique()),
        index=None,
        placeholder="Select medication",
        key="medication_choice"
    )

    if medication is None:
        return

    med_df = df[df["medication"] == medication]

    indication = st.selectbox(
        "Indication",
        sorted(med_df["indication"].unique()),
        index=None,
        placeholder="Select indication",
        key=f"indication_{medication}"
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
        placeholder="Select route",
        key=f"route_{medication}_{indication}"
    )

    if route is None:
        return

    selected_df = indication_df[
        indication_df["route"] == route
    ]

    if len(selected_df) != 1:
        st.error(
            "Medication selection does not correspond "
            "to exactly one database record."
        )
        return

    row = selected_df.iloc[0]

    st.divider()

    # =====================================
    # 3. REFERENCE INFORMATION
    # =====================================

    st.subheader("3. Reference Information")

    minimum = parse_decimal(
        row["min_dose_mg_per_kg"]
    )

    maximum = parse_decimal(
        row["max_dose_mg_per_kg"]
    )

    if (
        minimum is None
        or maximum is None
        or minimum <= 0
        or maximum < minimum
    ):
        st.error(
            "Dose range is missing or invalid. "
            "Calculation is unavailable."
        )
        return

    dose_basis = row["dose_basis"].strip()

    if dose_basis not in (
        "mg/kg/dose",
        "mg/kg/day"
    ):
        st.error(
            "Unsupported dose basis. "
            "Calculation is unavailable."
        )
        return

    st.write(
        f"**Reference dose:** "
        f"{minimum}–{maximum} {dose_basis}"
    )

    st.write(
        f"**Route:** {row['route']}"
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

    # Age eligibility:
    # A missing limit means age eligibility
    # cannot be confirmed.

    min_age = parse_decimal(
        row["min_age_months"]
    )

    max_age = parse_decimal(
        row["max_age_months"]
    )

    if min_age is None or max_age is None:
        st.warning(
            "Age eligibility is incomplete in the "
            "reference data. This calculation does "
            "not establish suitability for this age."
        )

    elif not min_age <= age_months <= max_age:
        st.error(
            "Patient age is outside the configured "
            "age range. Calculation is blocked."
        )
        return

    st.divider()

    # =====================================
    # 4. CLINICIAN-SELECTED DOSE
    # =====================================

    st.subheader("4. Select Dose")

    st.info(
        "Select a dose within the displayed reference "
        "range. The calculator will not automatically "
        "choose a dose."
    )

    selected_input = st.number_input(
        f"Selected dose ({dose_basis})",
        min_value=float(minimum),
        max_value=float(maximum),
        value=None,
        step=0.1,
        format="%.2f",
        placeholder="Enter selected dose",
        key=(
            f"dose_{medication}_"
            f"{indication}_{route}"
        )
    )

    if selected_input is None:
        return

    selected_dose = Decimal(
        str(selected_input)
    )

    # Independently validate the selected value.

    if not minimum <= selected_dose <= maximum:
        st.error(
            "Selected dose is outside the "
            "reference range."
        )
        return

    st.divider()

    # =====================================
    # 5. DOSE CALCULATION
    # =====================================

    st.subheader("5. Calculated Dose")

    calculated_mg = weight * selected_dose

    if dose_basis == "mg/kg/dose":

        st.metric(
            "Calculated dose",
            f"{display_number(calculated_mg)} mg/dose"
        )

        st.write(
            "**Calculation:** "
            f"{weight} kg × "
            f"{selected_dose} mg/kg/dose"
        )

    else:

        st.metric(
            "Calculated daily amount",
            f"{display_number(calculated_mg)} mg/day"
        )

        st.write(
            "**Calculation:** "
            f"{weight} kg × "
            f"{selected_dose} mg/kg/day"
        )

        st.warning(
            "This is a daily amount, NOT a single dose. "
            "The app does not divide it into individual "
            "doses or generate a dosing schedule."
        )

    # =====================================
    # 6. AVAILABLE SAFETY LIMITS
    # =====================================

    st.divider()

    st.subheader("6. Reference Limit Checks")

    if dose_basis == "mg/kg/day":
        st.info(
            "Per-dose and frequency checks are not "
            "supported for daily-dose records."
        )
        return

    limits = {
        "Maximum single dose": (
            "max_single_dose_mg",
            calculated_mg,
            "mg"
        ),
    }

    any_limit = False
    exceeded = False

    for label, (field, amount, unit) in limits.items():

        limit = parse_decimal(row[field])

        if limit is None:
            st.caption(
                f"{label}: not specified in database."
            )
            continue

        any_limit = True

        if amount > limit:
            exceeded = True
            st.error(
                f"{label} exceeded: "
                f"{display_number(amount)} mg "
                f"> {display_number(limit)} mg"
            )
        else:
            st.write(
                f"{label}: calculated amount does "
                f"not exceed {display_number(limit)} mg."
            )

    if not any_limit:
        st.warning(
            "No maximum single-dose limit is configured. "
            "The calculated dose has not been established "
            "as safe."
        )

    if exceeded:
        st.error(
            "The selected dose exceeds a configured "
            "reference limit. Do not use this result."
        )

    st.warning(
        "Daily exposure has NOT been checked. "
        "Frequency, maximum daily dose, formulation "
        "rounding, contraindications and interactions "
        "require independent verification."
    )

    st.divider()

    st.caption(
        "Calculation preview only. "
        "No medication order is generated."
    )