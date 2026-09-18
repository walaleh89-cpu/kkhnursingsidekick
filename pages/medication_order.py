import streamlit as st
import pandas as pd

from pathlib import Path
from decimal import Decimal, InvalidOperation


# ==========================================
# DATABASE LOCATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR / "data" / "medication_database_v2.csv"
)


# ==========================================
# LOAD MEDICATION DATABASE
# ==========================================

def load_database():

    if not DATA_FILE.exists():

        st.error(
            "Medication database not found. "
            "Please check data/medication_database_v2.csv"
        )

        return pd.DataFrame()

    try:

        df = pd.read_csv(
            DATA_FILE,
            dtype=str,
            keep_default_na=False
        )

        required_columns = [
            "medication",
            "indication",
            "route",
            "min_age_months",
            "max_age_months",
            "min_dose_mg_per_kg",
            "max_dose_mg_per_kg",
            "dose_basis",
            "frequency_options",
            "max_single_dose_mg",
            "max_daily_dose_mg",
            "max_daily_dose_mg_per_kg",
            "formulation",
            "remarks",
            "source",
            "version",
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:

            st.error(
                "Missing database columns: "
                + ", ".join(missing)
            )

            return pd.DataFrame()

        df = df[
            df["medication"].str.strip() != ""
        ].copy()

        return df

    except Exception as e:

        st.error(
            f"Unable to load medication database: {e}"
        )

        return pd.DataFrame()


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def to_decimal(value):

    try:

        number = Decimal(str(value).strip())

        if not number.is_finite():
            return None

        return number

    except (InvalidOperation, ValueError, TypeError):

        return None


def format_mg(value):

    return f"{value:,.2f}"


def check_age(row, age_months):

    min_age = to_decimal(
        row["min_age_months"]
    )

    max_age = to_decimal(
        row["max_age_months"]
    )

    if min_age is not None:

        if age_months < min_age:

            st.error(
                "Patient is below the minimum age "
                "specified in the medication database."
            )

            return False

    if max_age is not None:

        if age_months > max_age:

            st.error(
                "Patient exceeds the maximum age "
                "specified in the medication database."
            )

            return False

    if min_age is None or max_age is None:

        st.warning(
            "Age eligibility is not fully specified "
            "in the database. The calculated range "
            "does not establish suitability for this age."
        )

    return True


# ==========================================
# MAIN CALCULATOR
# ==========================================

def run_medication_order_page():

    st.header(
        "💊 Paediatric Medication Dosage Calculator"
    )

    # Back button

    if st.button(
        "🏠 Back to Home",
        key="medication_back_home"
    ):

        st.session_state.page = "home"

        st.rerun()

    # Safety warning

    st.warning(
        "DEMONSTRATION ONLY — Medication reference "
        "data have not been clinically validated. "
        "Do not use these calculations for prescribing "
        "or medication administration."
    )

    # Load database

    df = load_database()

    if df.empty:

        st.info(
            "No medication records are available."
        )

        return

    # ======================================
    # 1. PATIENT INFORMATION
    # ======================================

    st.subheader(
        "1. Patient Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        years = st.number_input(
            "Age (years)",
            min_value=0,
            max_value=18,
            value=3,
            step=1,
            key="med_age_years"
        )

    with col2:

        months = st.number_input(
            "Months",
            min_value=0,
            max_value=11,
            value=0,
            step=1,
            key="med_age_months"
        )

    with col3:

        weight_input = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=150.0,
            value=0.0,
            step=0.1,
            format="%.2f",
            key="med_weight"
        )

    age_months = years * 12 + months

    if weight_input <= 0:

        st.info(
            "Please enter the patient's weight."
        )

        return

    weight = Decimal(
        str(weight_input)
    )

    st.divider()

    # ======================================
    # 2. MEDICATION SELECTION
    # ======================================

    st.subheader(
        "2. Medication Selection"
    )

    medication = st.selectbox(
        "Medication",
        sorted(df["medication"].unique()),
        index=None,
        placeholder="Select medication",
        key="medication_selection"
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
            "Medication selection does not match "
            "exactly one database record."
        )

        return

    row = selected_df.iloc[0]

    # ======================================
    # 3. REFERENCE INFORMATION
    # ======================================

    st.divider()

    st.subheader(
        "3. Medication Reference"
    )

    minimum = to_decimal(
        row["min_dose_mg_per_kg"]
    )

    maximum = to_decimal(
        row["max_dose_mg_per_kg"]
    )

    if (
        minimum is None
        or maximum is None
        or minimum <= 0
        or maximum < minimum
    ):

        st.error(
            "The reference dose range is missing "
            "or invalid. Calculation cannot proceed."
        )

        return

    dose_basis = row["dose_basis"].strip()

    if dose_basis not in [
        "mg/kg/dose",
        "mg/kg/day"
    ]:

        st.error(
            "Unsupported dose basis."
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

    # Age check

    if not check_age(
        row,
        age_months
    ):

        return

    # ======================================
    # 4. AUTOMATIC DOSE RANGE
    # ======================================

    st.divider()

    st.subheader(
        "4. Weight-Based Dose Range"
    )

    minimum_mg = weight * minimum

    maximum_mg = weight * maximum

    # Apply an available maximum single-dose
    # ceiling only for per-dose calculations.
    # Do not silently cap the displayed range.

    max_single = to_decimal(
        row["max_single_dose_mg"]
    )

    if dose_basis == "mg/kg/dose":

        st.success(
            f"Calculated reference range: "
            f"{format_mg(minimum_mg)} – "
            f"{format_mg(maximum_mg)} mg/dose"
        )

        st.caption(
            f"Calculation: {weight} kg × "
            f"{minimum}–{maximum} mg/kg/dose"
        )

        if max_single is not None:

            st.info(
                f"Maximum single dose recorded: "
                f"{format_mg(max_single)} mg"
            )

            if minimum_mg > max_single:

                st.error(
                    "The entire weight-calculated "
                    "range exceeds the recorded "
                    "maximum single dose. "
                    "Dose selection is blocked."
                )

                return

            if maximum_mg > max_single:

                st.warning(
                    "The upper end of the calculated "
                    "range exceeds the recorded "
                    "maximum single dose. "
                    "The reference range above is "
                    "not a safe-dose recommendation."
                )

    else:

        st.success(
            f"Calculated daily reference range: "
            f"{format_mg(minimum_mg)} – "
            f"{format_mg(maximum_mg)} mg/day"
        )

        st.caption(
            f"Calculation: {weight} kg × "
            f"{minimum}–{maximum} mg/kg/day"
        )

        st.warning(
            "This is a DAILY dose range, "
            "not a single-dose range."
        )

    # ======================================
    # 5. SELECT SPECIFIC DOSE
    # ======================================

    st.divider()

    st.subheader(
        "5. Select Dose"
    )

    st.info(
        "Optional: Select a dose within the "
        "reference range to calculate the "
        "corresponding amount in mg."
    )

    selected_input = st.number_input(
        f"Selected dose ({dose_basis})",
        min_value=float(minimum),
        max_value=float(maximum),
        value=None,
        step=0.1,
        format="%.2f",
        placeholder="Enter dose",
        key=(
            f"selected_{medication}_"
            f"{indication}_{route}"
        )
    )

    if selected_input is None:

        st.caption(
            "The calculated dose range is shown "
            "above. Select a specific dose only "
            "if you wish to calculate one."
        )

        return

    selected_dose = Decimal(
        str(selected_input)
    )

    if not minimum <= selected_dose <= maximum:

        st.error(
            "Selected dose is outside "
            "the reference range."
        )

        return

    # ======================================
    # 6. CALCULATED SELECTED DOSE
    # ======================================

    st.divider()

    st.subheader(
        "6. Calculated Selected Dose"
    )

    calculated_dose = (
        weight * selected_dose
    )

    if dose_basis == "mg/kg/dose":

        st.metric(
            "Calculated dose",
            f"{format_mg(calculated_dose)} mg/dose"
        )

        st.caption(
            f"{weight} kg × "
            f"{selected_dose} mg/kg/dose"
        )

    else:

        st.metric(
            "Calculated daily amount",
            f"{format_mg(calculated_dose)} mg/day"
        )

        st.caption(
            f"{weight} kg × "
            f"{selected_dose} mg/kg/day"
        )

        st.warning(
            "This is the total daily amount. "
            "It has not been divided into "
            "individual doses."
        )

    # ======================================
    # 7. AVAILABLE LIMIT CHECKS
    # ======================================

    st.divider()

    st.subheader(
        "7. Available Maximum-Dose Checks"
    )

    exceeded = False

    # Single-dose maximum

    if dose_basis == "mg/kg/dose":

        if max_single is not None:

            if calculated_dose > max_single:

                st.error(
                    "Maximum single dose exceeded: "
                    f"{format_mg(calculated_dose)} mg "
                    f"> {format_mg(max_single)} mg"
                )

                exceeded = True

            else:

                st.write(
                    "Calculated dose does not exceed "
                    "the recorded maximum single dose "
                    f"of {format_mg(max_single)} mg."
                )

        else:

            st.warning(
                "Maximum single dose is not "
                "specified in the database."
            )

    # Daily-dose limits:
    # These are displayed but not treated as
    # fully checked without a validated schedule.

    max_daily = to_decimal(
        row["max_daily_dose_mg"]
    )

    max_daily_per_kg = to_decimal(
        row["max_daily_dose_mg_per_kg"]
    )

    if max_daily is not None:

        st.write(
            f"**Recorded maximum daily dose:** "
            f"{format_mg(max_daily)} mg/day"
        )

        if (
            dose_basis == "mg/kg/day"
            and calculated_dose > max_daily
        ):

            st.error(
                "Calculated daily amount exceeds "
                "the recorded maximum daily dose."
            )

            exceeded = True

    if max_daily_per_kg is not None:

        st.write(
            "**Recorded maximum daily "
            "weight-based dose:** "
            f"{format_mg(max_daily_per_kg)} "
            "mg/kg/day"
        )

        if (
            dose_basis == "mg/kg/day"
            and selected_dose > max_daily_per_kg
        ):

            st.error(
                "Selected daily dose exceeds "
                "the recorded maximum daily "
                "weight-based dose."
            )

            exceeded = True

    if exceeded:

        st.error(
            "A configured maximum-dose limit "
            "has been exceeded. "
            "Do not use this result."
        )

    else:

        st.warning(
            "This calculator does not confirm "
            "that the dose is safe. Daily exposure, "
            "frequency, formulation rounding and "
            "patient-specific contraindications "
            "have not been fully checked."
        )

    # ======================================
    # END
    # ======================================

    st.divider()

    st.caption(
        "Weight-based calculation preview only. "
        "No medication order is generated."
    )