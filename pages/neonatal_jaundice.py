import streamlit as st
from datetime import datetime
import pytz

def run_neonatal_jaundice_page():

    st.subheader("🌞 Neonatal Jaundice")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()
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