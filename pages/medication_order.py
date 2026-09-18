import streamlit as st
import pandas as pd
from pathlib import Path
from decimal import Decimal, InvalidOperation

# ==========================================
# MEDICATION DATABASE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "medication_database.csv"

REQUIRED_COLUMNS = [
    "medication",
    "indication",
    "route",
    "min_age_months",
    "max_age_months",
    "dose_basis",
    "dose_mg_per_kg",
    "frequency_hours",
    "max_single_dose_mg",
    "max_daily_dose_mg",
    "concentration_mg_per_ml",
    "source",
    "version",
]

NUMERIC_COLUMNS = [
    "min_age_months",
    "max_age_months",
    "dose_mg_per_kg",
    "frequency_hours",
    "max_single_dose_mg",
    "max_daily_dose_mg",
    "concentration_mg_per_ml",
]


def load_medications():

    if not DATA_FILE.exists():
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    try:
        df = pd.read_csv(DATA_FILE, dtype=str)

        missing = [
            col for col in REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            st.error(
                "Medication database is missing columns: "
                + ", ".join(missing)
            )
            return pd.DataFrame(columns=REQUIRED_COLUMNS)

        # Remove completely empty rows
        df = df.dropna(how="all")

        return df

    except Exception as e:
        st.error(f"Unable to load medication database: {e}")
        return pd.DataFrame(columns=REQUIRED_COLUMNS)


# ==========================================
# VALIDATION
# ==========================================

def validate_medication(row):

    try:
        for col in [
            "medication",
            "indication",
            "route",
            "dose_basis",
            "source",
            "version",
        ]:
            if pd.isna(row[col]) or not str(row[col]).strip():
                return False, f"Missing required field: {col}"

        if row["dose_basis"] not in [
            "mg/kg/dose",
            "mg/kg/day",
        ]:
            return False, "Unsupported dose basis"

        values = {}

        for col in NUMERIC_COLUMNS:

            value = row[col]

            if pd.isna(value) or str(value).strip() == "":
                values[col] = None
            else:
                values[col] = Decimal(str(value))

                if not values[col].is_finite():
                    return False, f"Invalid value: {col}"

        required_numeric = [
            "min_age_months",
            "max_age_months",
            "dose_mg_per_kg",
            "frequency_hours",
            "max_single_dose_mg",
            "max_daily_dose_mg",
        ]

        for col in required_numeric:
            if values[col] is None:
                return False, f"Missing required field: {col}"

        if values["dose_mg_per_kg"] <= 0:
            return False, "Dose must be positive"

        if values["frequency_hours"] <= 0:
            return False, "Frequency must be positive"

        if values["max_single_dose_mg"] <= 0:
            return False, "Maximum single dose must be positive"

        if values["max_daily_dose_mg"] <= 0:
            return False, "Maximum daily dose must be positive"

        if values["min_age_months"] < 0:
            return False, "Invalid minimum age"

        if (
            values["max_age_months"]
            < values["min_age_months"]
        ):
            return False, "Invalid age range"

        concentration = values["concentration_mg_per_ml"]

        if concentration is not None and concentration <= 0:
            return False, "Invalid concentration"

        return True, values

    except (InvalidOperation, ValueError, TypeError):
        return False, "Invalid medication data"


# ==========================================
# CALCULATION ENGINE
# ==========================================

def calculate_dose(weight, row, values):

    dose_per_kg = values["dose_mg_per_kg"]
    frequency = values["frequency_hours"]

    doses_per_day = Decimal("24") / frequency

    if row["dose_basis"] == "mg/kg/dose":

        calculated_single = weight * dose_per_kg

    else:

        calculated_daily = weight * dose_per_kg

        calculated_single = calculated_daily / doses_per_day

    max_single = values["max_single_dose_mg"]
    max_daily = values["max_daily_dose_mg"]

    # Both limits must be satisfied.
    daily_limit_per_dose = max_daily / doses_per_day

    final_dose = min(
        calculated_single,
        max_single,
        daily_limit_per_dose,
    )

    final_daily = final_dose * doses_per_day

    return {
        "calculated_single": calculated_single,
        "final_dose": final_dose,
        "final_daily": final_daily,
        "doses_per_day": doses_per_day,
        "max_single": max_single,
        "max_daily": max_daily,
        "was_capped": final_dose < calculated_single,
    }


# ==========================================
# MAIN STREAMLIT PAGE
# ==========================================

def run_medication_order_page():

    st.header("💊 Paediatric Medication Order Assistant")

    if st.button("🏠 Back to Home", key="med_order_back"):
        st.session_state.page = "home"
        st.rerun()

    st.warning(
        "PROTOTYPE ONLY — Not for clinical prescribing. "
        "Medication data and calculations require institutional "
        "pharmacy and medical validation before clinical use."
    )

    st.markdown(
        "Calculate a suggested weight-based medication order "
        "using an approved medication database."
    )

    medications = load_medications()

    if medications.empty:

        st.info(
            "No medications are currently available. "
            "Please populate the medication database with "
            "approved dosing information."
        )

        st.stop()

    # ======================================
    # PATIENT INFORMATION
    # ======================================

    st.subheader("1. Patient Information")

    col1, col2 = st.columns(2)

    with col1:

        age_years = st.number_input(
            "Age (years)",
            min_value=0,
            max_value=18,
            value=3,
            step=1,
            key="med_age_years",
        )

        age_months_extra = st.number_input(
            "Additional months",
            min_value=0,
            max_value=11,
            value=0,
            step=1,
            key="med_age_months",
        )

    with col2:

        weight = st.number_input(
            "Current weight (kg)",
            min_value=0.0,
            max_value=300.0,
            value=0.0,
            step=0.1,
            format="%.2f",
            key="med_weight",
        )

    total_age_months = age_years * 12 + age_months_extra

    if weight <= 0:

        st.warning("Please enter a valid patient weight.")
        st.stop()

    if weight < 1 or weight > 150:

        st.error(
            "Weight is outside the prototype's supported range. "
            "Verify the patient's measured weight."
        )

        st.stop()

    weight_decimal = Decimal(str(weight))

    st.caption(
        f"Patient age: {total_age_months} months | "
        f"Weight: {weight:.2f} kg"
    )

    st.divider()

    # ======================================
    # MEDICATION SELECTION
    # ======================================

    st.subheader("2. Select Medication")

    medication_list = sorted(
        medications["medication"].dropna().unique()
    )

    medication = st.selectbox(
        "Medication",
        medication_list,
        index=None,
        placeholder="Select medication",
        key="med_select",
    )

    if not medication:
        st.stop()

    med_df = medications[
        medications["medication"] == medication
    ]

    indication_list = sorted(
        med_df["indication"].dropna().unique()
    )

    indication = st.selectbox(
        "Indication",
        indication_list,
        index=None,
        placeholder="Select indication",
        key="med_indication",
    )

    if not indication:
        st.stop()

    indication_df = med_df[
        med_df["indication"] == indication
    ]

    route_list = sorted(
        indication_df["route"].dropna().unique()
    )

    route = st.selectbox(
        "Route",
        route_list,
        index=None,
        placeholder="Select route",
        key="med_route",
    )

    if not route:
        st.stop()

    selected = indication_df[
        indication_df["route"] == route
    ]

    # ======================================
    # AGE FILTER
    # ======================================

    eligible_rows = []

    for _, row in selected.iterrows():

        valid, result = validate_medication(row)

        if not valid:
            continue

        if (
            result["min_age_months"]
            <= total_age_months
            <= result["max_age_months"]
        ):

            eligible_rows.append((row, result))

    if len(eligible_rows) == 0:

        st.error(
            "No validated dosing record is available "
            "for this medication, indication, route "
            "and patient age."
        )

        st.stop()

    if len(eligible_rows) > 1:

        st.error(
            "Multiple dosing records match this patient. "
            "Database review is required before calculation."
        )

        st.stop()

    row, values = eligible_rows[0]

    st.divider()

    # ======================================
    # CALCULATE
    # ======================================

    st.subheader("3. Dose Calculation")

    if not st.checkbox(
        "I have verified the patient's current weight "
        "and selected medication details.",
        key="med_verify",
    ):

        st.info(
            "Verify the patient information to display "
            "the calculation."
        )

        st.stop()

    result = calculate_dose(
        weight_decimal,
        row,
        values,
    )

    st.write(
        f"**Dose basis:** {row['dose_basis']}"
    )

    st.write(
        f"**Recommended dose:** "
        f"{values['dose_mg_per_kg']} "
        f"{row['dose_basis']}"
    )

    st.write(
        f"**Calculated single dose:** "
        f"{result['calculated_single']:.2f} mg"
    )

    st.write(
        f"**Maximum single dose:** "
        f"{result['max_single']} mg"
    )

    st.write(
        f"**Maximum daily dose:** "
        f"{result['max_daily']} mg/day"
    )

    if result["was_capped"]:

        st.error(
            "⚠️ Calculated dose exceeds at least one "
            "configured maximum. The uncapped calculation "
            "must be reviewed against the approved guideline."
        )

        st.write(
            f"**Uncapped dose:** "
            f"{result['calculated_single']:.2f} mg"
        )

        st.write(
            f"**Dose after applying limits:** "
            f"{result['final_dose']:.2f} mg"
        )

        st.error(
            "Automatic dose capping is shown for "
            "demonstration only. No suggested order "
            "will be generated for this result."
        )

        st.stop()

    st.success(
        "Calculated dose is within the configured "
        "single-dose and daily-dose limits."
    )

    st.divider()

    # ======================================
    # FORMULATION CONVERSION
    # ======================================

    st.subheader("4. Formulation")

    concentration = values["concentration_mg_per_ml"]

    volume_text = ""

    if concentration is not None:

        volume = result["final_dose"] / concentration

        st.write(
            f"**Concentration:** "
            f"{concentration} mg/mL"
        )

        st.write(
            f"**Calculated volume:** "
            f"{volume:.3f} mL"
        )

        st.warning(
            "Volume is unrounded. Confirm the formulation, "
            "measurable volume and institution-approved "
            "rounding rules before use."
        )

        volume_text = f" ({volume:.3f} mL, unrounded)"

    else:

        st.info(
            "No liquid formulation is configured "
            "for this medication."
        )

    st.divider()

    # ======================================
    # SUGGESTED ORDER
    # ======================================

    st.subheader("5. Suggested Medication Order")

    final_dose = result["final_dose"]
    frequency = values["frequency_hours"]

    order = (
        f"{medication} {final_dose:.2f} mg"
        f"{volume_text} "
        f"{route} every {frequency} hours"
    )

    st.success(order)

    st.write(
        f"**Calculated daily exposure:** "
        f"{result['final_daily']:.2f} mg/day"
    )

    st.write(
        f"**Daily exposure per kg:** "
        f"{result['final_daily'] / weight_decimal:.2f} "
        "mg/kg/day"
    )

    # ======================================
    # SAFETY REMINDERS
    # ======================================

    st.subheader("6. Safety Reminders")

    st.warning(
        "Before prescribing, independently verify:\n\n"
        "- Patient identity and current measured weight\n"
        "- Medication indication and allergy status\n"
        "- Dose, route and frequency\n"
        "- Renal and hepatic function where applicable\n"
        "- Maximum dose and formulation\n"
        "- Relevant contraindications and interactions"
    )

    # ======================================
    # SOURCE
    # ======================================

    st.divider()

    st.caption(
        f"Source: {row['source']} | "
        f"Version: {row['version']}"
    )

    st.caption(
        "Prototype only. This tool does not replace "
        "clinical judgement or institutional "
        "prescribing guidelines."
    )