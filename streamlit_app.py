import streamlit as st
from datetime import datetime
import pytz
from pages.dosage import run_dosage_page 
from pages.fluids import run_fluids_page
from pages.bmi import run_bmi_page
from pages.corrected_age import run_corrected_age_page
from pages.neonate_feeds import run_neonate_feeds_page
from pages.compatibility import run_compatibility_page
from pages.vitals import run_vitals_page
from pages.urine_output import run_urine_output_page


st.set_page_config(page_title="🩺 Nursing Calculator", page_icon="🩺", layout="wide")
st.title("🩺 Nursing Calculator App")

st.markdown(
    "<p style='font-size:14px; color:gray; text-align:center; margin-top:-10px;'>"
    "© Property of KK Women’s and Children’s Hospital APN Office"
    "</p>",
    unsafe_allow_html=True
)

st.markdown("A collection of essential nursing calculators.")

# ------------------------------
# SESSION STATE
# ------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "sync_ordered_dose" not in st.session_state:
    st.session_state.sync_ordered_dose = 0.0


# ------------------------------
# HOME PAGE
# ------------------------------
def show_home():
    st.subheader("Select a Calculator:")

    calculators = [
        ("💊 Dosage Verification / Dispensing", "dosage_dispensing"),
        ("🧒 Pediatric Fluids Requirement", "fluids"),
        ("⚖️ BMI", "bmi"),
        ("🌞 Neonatal Jaundice", "jaundice"),
        ("🍼 Corrected Age", "corrected_age"),
        ("🍼 Neonate Feeds", "neonate_feeds"),
        ("💉 Drug Compatibility", "compatibility"),
        ("📊 Vital Signs", "vitals"),
        ("🚰 Urine Output", "urine_output"),
    ]

    for i in range(0, len(calculators), 5):
        cols = st.columns(5)
        for col, (name, key) in zip(cols, calculators[i:i+5]):
            if col.button(name, key=key):
                st.session_state.page = key
                st.rerun()


def back_to_home():
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ------------------------------
# NAVIGATION
# ------------------------------
if st.session_state.page == "home":
    show_home()


# ==========================================================
#1 💊 DOSAGE PAGE (FIXED - FULLY SCOPED)
# ==========================================================
elif st.session_state.page == "dosage_dispensing":
    run_dosage_page()

# ------------------------------
#2 Pediatric Fluids Requirement
# ------------------------------
elif st.session_state.page == "fluids":
    run_fluids_page()

# ------------------------------
# 4. BMI
# ------------------------------
elif st.session_state.page == "bmi":
    run_bmi_page()

# ------------------------------
# 5. Neonatal Jaundice
# ------------------------------
elif st.session_state.page == "jaundice":
    st.subheader("🌞 Neonatal Jaundice")
    back_to_home()

    from datetime import datetime
    import pytz

    # ===============================
    # TIMEZONE CONFIGURATION
    # ===============================
    HOSPITAL_TZ = pytz.timezone("Asia/Singapore")

    # --- Patient birth info ---
    dob = st.date_input("Date of Birth")
    birth_time = st.time_input("Time of Birth (24-hour format)")

    # --- Calculate hours of life ---
    hours_of_life = None
    try:
        birth_naive = datetime.combine(dob, birth_time)
        birth_datetime = HOSPITAL_TZ.localize(birth_naive)
        current_datetime = datetime.now(HOSPITAL_TZ)
        hours_of_life = (current_datetime - birth_datetime).total_seconds() / 3600
        st.success(f"✅ Hours of Life: {hours_of_life:.1f} hours")
    except Exception:
        st.warning("Unable to calculate age. Please check date and time inputs.")

    # --- High-Risk Criteria ---
    st.markdown("**Select Risk Factors (High-Risk Criteria):**")
    risk_factors = st.multiselect(
        "Check all that apply:",
        [
            "Visible jaundice within 24 hours of age",
            "G6PD deficiency & other hemolytic conditions",
            "ABO incompatibility",
            "Rhesus incompatibility",
            "Rapidly rising serum bilirubin (>103 µmol/L per day)",
            "Late preterm (35–36 weeks)",
            "Asphyxia (Apgar ≤ 5 at 1 and 5 minutes)",
            "Family history of severe NNJ in siblings needing exchange transfusion",
            "Inadequate breastfeeding plus weight loss ≥ 10%",
            "Infants with birth weight 2000–2500 g",
            "Mother's blood group and antibody titers unknown",
            "Exclusive breastfeeding with ≥10% weight loss before regaining birth weight"
        ]
    )

    auto_risk = "High-Risk" if risk_factors else "Normal-Risk"
    selected_risk = st.radio(
        "Infant Risk Category (can override):",
        ["High-Risk", "Normal-Risk"],
        index=0 if auto_risk == "High-Risk" else 1
    )

    # --- Measurement Type ---
    measurement_type = st.radio(
        "Measurement Type:",
        ["Transcutaneous Bilirubin (TcB)", "Serum Bilirubin (SB)"]
    )

    # ===============================
    # TcB → SB SCREENING
    # ===============================
    def tcb_to_sb_needed(hours, risk, tcb):
        rules_normal = [
            (25,36,160),(37,48,180),(49,72,200),(73,96,220),
            (97,120,220),(121,168,240),(169,336,250)
        ]
        rules_high = [
            (0,12,80),(13,24,120),(25,36,140),(37,48,160),
            (49,72,180),(73,96,200),(97,120,200),
            (121,168,220),(169,336,240)
        ]
        rules = rules_high if risk == "High-Risk" else rules_normal
        for start, end, threshold in rules:
            if start <= hours <= end:
                return tcb > threshold
        return False

    # ===============================
    # SB RULE TABLES
    # ===============================
    HIGH_RISK_RULES = [
        (0,12,   None,100,150,175,200),
        (13,24,  None,150,200,225,250),
        (25,36,  135,175,225,250,275),
        (37,48,  160,200,250,275,300),
        (49,72,  185,225,275,300,325),
        (73,96,  210,250,300,325,350),
        (97,120, 210,250,300,325,350),
        (121,168,235,275,325,350,375),
        (169,336,260,300,325,350,375),
    ]

    NORMAL_RISK_RULES = [
        (25,36,  160,200,250,275,300),
        (37,48,  185,225,300,325,350),
        (49,72,  210,250,300,325,350),
        (73,96,  235,275,325,350,375),
        (97,120, 235,275,350,375,400),
        (121,168,260,300,350,375,400),
        (169,336,285,325,375,400,425),
    ]

    # ===============================
    # SB EVALUATION ENGINE
    # ===============================
    def evaluate_jaundice(age, sb, on_phototherapy, rules):
        for start, end, stop_pt, single, double, intense, exchange in rules:
            if start <= age <= end:

                # INPATIENT
                if on_phototherapy:
                    if stop_pt is not None and sb <= stop_pt:
                        return ("🟢 Stop phototherapy", "lightblue")
                    if sb < double:
                        return ("🟡 Continue single blue phototherapy", "khaki")
                    if sb < intense:
                        return ("🟠 Double blue phototherapy", "orange")
                    if sb < exchange:
                        return ("🔴 Intense phototherapy", "tomato")
                    return ("⚠️ Exchange transfusion indicated", "red")

                # OUTPATIENT
                else:
                    if sb < single:
                        return ("🟢 Continue monitoring (outpatient)", "lightgreen")
                    if sb < double:
                        return ("🟡 Start single blue phototherapy", "khaki")
                    if sb < intense:
                        return ("🟠 Double blue phototherapy", "orange")
                    if sb < exchange:
                        return ("🔴 Intense phototherapy", "tomato")
                    return ("⚠️ Exchange transfusion indicated", "red")

        return ("Age out of range", "lightgray")

    # ===============================
    # DISPLAY RESULTS
    # ===============================
    if hours_of_life is not None:

        if measurement_type == "Transcutaneous Bilirubin (TcB)":
            tcb_value = st.number_input("Enter TcB level (µmol/L):", min_value=0)
            if st.button("Evaluate TcB"):
                if tcb_to_sb_needed(hours_of_life, selected_risk, tcb_value):
                    st.warning("⚠️ TcB exceeds threshold – perform Serum Bilirubin test")
                else:
                    st.success("✅ TcB below threshold – continue monitoring")

        else:
            sb_level = st.number_input("Enter SB level (µmol/L):", min_value=0)
            on_phototherapy = st.checkbox("Infant is currently on phototherapy (inpatient)")

            if st.button("Evaluate SB"):
                rules = HIGH_RISK_RULES if selected_risk == "High-Risk" else NORMAL_RISK_RULES
                message, color = evaluate_jaundice(
                    hours_of_life,
                    sb_level,
                    on_phototherapy,
                    rules
                )

                st.markdown(
                    f"<div style='background-color:{color}; padding:15px; "
                    f"border-radius:10px; font-weight:bold; text-align:center;'>"
                    f"{message}</div>",
                    unsafe_allow_html=True
                )

# ------------------------------
# 6. Corrected Age
# ------------------------------
elif st.session_state.page == "corrected_age":
    run_corrected_age_page()


#7. Neonate feeds 
#------------------------------
elif st.session_state.page == "neonate_feeds":
    run_neonate_feeds_page()

# ------------------------------
# 8. Drug Compatibility
# ------------------------------
elif st.session_state.page == "compatibility":
    run_compatibility_page()

# 9. Vital Signs
# ------------------------------
elif st.session_state.page == "vitals":
    run_vitals_page()

# 10. Urine Output
#----------------------------------------------
elif st.session_state.page == "urine_output":
    run_urine_output_page()