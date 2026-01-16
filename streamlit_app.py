
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="🩺 Nursing Calculator", page_icon="🩺", layout="wide")
st.title("🩺 Nursing Calculator App")

# Polished hospital-style ownership footer
st.markdown(
    "<p style='font-size:14px; color:gray; text-align:center; margin-top:-10px;'>"
    "© Property of KK Women’s and Children’s Hospital APN Office"
    "</p>",
    unsafe_allow_html=True
)

st.markdown("A collection of essential nursing calculators.")

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Initialize sync state for ordered dose
if "sync_ordered_dose" not in st.session_state:
    st.session_state.sync_ordered_dose = 0.0

def show_home():
    st.subheader("Select a Calculator:")
    st.markdown(
    """
    <div style="font-size:20px; font-weight:bold; color:red; text-align:center; animation: blinker 1.5s linear infinite;">
        👉 Click to navigate to the calculator.
    </div>

    <style>
    @keyframes blinker {
      50% { opacity: 0; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


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

    # Display in rows of 5
    for i in range(0, len(calculators), 5):
        cols = st.columns(5)
        for col, (name, key) in zip(cols, calculators[i:i+5]):
            clicked = col.button(name, key=key, use_container_width=True)
            if clicked: 
                st.session_state.page = key
                st.rerun()
            ##if col.button(name, use_container_width=True):
                ##st.session_state.page = key


# --- Back button ---
def back_to_home():
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# --- Main App Navigation ---
if st.session_state.page == "home":
    show_home()

# ------------------------------
# Dosage Verification Page
# ------------------------------
if st.session_state.page == "dosage_dispensing":
    st.subheader("💊 Dosage Verification / Dispensing Calculator")
    back_to_home()

    # ------------------------------
    # Medication Data
    # ------------------------------
    medications = {
        "PO": {
            "Antibiotics": {
                "Amoxicillin": {"unit":"mg","usual":[50,50],"high":[80,90],"max_day":4000},
                "Amoxicillin-Clavulanate (Augmentin)": {"unit":"mg","usual":[50,50],"high":[80,90],"max_day":4000},
                "Cephalexin": {"unit":"mg","usual":[25,50],"severe":[100,150],"max_day":6000},
                "Ciprofloxacin": {"unit":"mg","usual":[20,30],"severe":[40,40],"max_dose":750,"max_day":1500},
                "Clarithromycin": {"unit":"mg","usual":[15,15],"max_dose":500,"max_day":1000},
                "Cloxacillin": {"unit":"mg","usual":[50,100],"max_dose":1000,"max_day":6000},
                "Metronidazole": {"unit":"mg","usual":[20,50],"max_day":2250},
                "Vancomycin (C. difficile)": {"unit":"mg","usual":[10,10],"max_dose":500,"max_day":2000}
            },
            "Antivirals": {
                "Acyclovir": {"unit":"mg","usual":[80,80],"max_dose":800,"max_day":4000},
                "Oseltamivir": {"unit":"mg","max_dose":75}
            },
            "Others": {
                "Omeprazole": {
                    "unit":"mg",
                    "usual":[0.8,0.8],
                    "max_dose":40,
                    "notes":"Give 30 minutes before meals for best effect."
                },
                "Nifedipine": {
                    "unit":"mg",
                    "usual":[1,2],
                    "max_dose":10,
                    "max_day":120,
                    "notes":"Also max 3 mg/kg/day."
                },
                "Aspirin (Antiplatelet)": {
                    "unit":"mg",
                    "usual":[1,5],
                    "notes":"Once daily antiplatelet dosing."
                },
                "Aspirin (Anti-inflammatory)": {
                    "unit":"mg",
                    "usual":[80,100],
                    "notes":"Divide Q6–8H."
                },
                "Prednisolone": {
                    "unit":"mg",
                    "usual":[1,2],
                    "max_day":60
                },
                "Sodium Valproate": {
                    "unit":"mg",
                    "usual":[10,15],
                    "severe":[60,60],
                    "notes":"Given BD or TDS."
                },
                "Salbutamol MDI": {
                    "unit":"puffs",
                    "notes":"0.2–0.3 puffs/kg/dose (min 2, max 8 puffs)."
                },
                "Salbutamol Nebuliser (0.5%)": {
                    "unit":"mL",
                    "notes":"0.03 mL/kg/dose, max 2 mL."
                }
            }
        },
        "IV / IM": {
            "Antibiotics": {
                "Cefazolin": {"unit":"mg","usual":[25,50],"severe":[100,150],"max_day":12000},
                "Ceftriaxone": {"unit":"mg","usual":[50,75],"severe":[100,100],"max_dose":2000,"max_day":4000},
                "Cloxacillin": {"unit":"mg","usual":[100,100],"severe":[200,300],"max_dose":2000,"max_day":12000},
                "Gentamicin": {"unit":"mg","usual":[5,7.5]},
                "Metronidazole": {"unit":"mg","usual":[22.5,40],"max_day":4000},
                "Vancomycin": {"unit":"mg","usual":[30,60],"max_dose":500,"max_day":2000}
            },
            "Antivirals": {
                "Acyclovir": {"unit":"mg","usual":[30,30]}
            },
            "Others": {
                "Omeprazole": {
                    "unit":"mg",
                    "usual":[1,1],
                    "max_dose":40
                },
                "Hydrocortisone": {
                    "unit":"mg",
                    "usual":[16,16],
                    "max_dose":100,
                    "max_day":400
                }
            }
        }
    }

    # ------------------------------
    # Inputs
    # ------------------------------
    weight = st.number_input("Patient weight (kg)", min_value=0.1, step=0.1)

    route = st.selectbox("Route", list(medications.keys()))
    category = st.selectbox("Category", list(medications[route].keys()))
    med = st.selectbox("Medication", list(medications[route][category].keys()))
    med_info = medications[route][category][med]

    severity = st.radio("Severity", ["Usual / Mild–Moderate", "Severe"], horizontal=True)

    dose = st.number_input(
        f"Ordered dose per administration ({med_info['unit']})",
        min_value=0.0,
        step=0.1
    )

    freq_map = {"Q24H":1,"Q12H":2,"Q8H":3,"Q6H":4}
    freq_label = st.selectbox("Frequency", list(freq_map.keys()))
    freq = freq_map[freq_label]

    # ------------------------------
    # Side-by-side Display
    # ------------------------------
    st.markdown("### ⚖️ Recommended vs Ordered Dose")

    key = "severe" if severity == "Severe" and "severe" in med_info else "usual"

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📘 Recommended")
        if key in med_info:
            low, high = med_info[key]
            st.write(f"**mg/kg/day:** {low}–{high}")
            st.write(f"**mg/day:** {(low*weight):.1f}–{(high*weight):.1f}")
            st.write(f"**mg/dose:** {(low*weight/freq):.1f}–{(high*weight/freq):.1f}")
        if "notes" in med_info:
            st.info(med_info["notes"])

    with col2:
        st.markdown("#### 📊 Ordered")
        daily = dose * freq
        st.write(f"**mg/kg/day:** {(daily/weight):.2f}")
        st.write(f"**mg/day:** {daily:.1f}")
        st.write(f"**mg/dose:** {dose:.1f}")

    # ------------------------------
    # Safety Check
    # ------------------------------
    if st.button("Check Dose"):
        warnings = []

        if key in med_info:
            low, high = med_info[key]
            if daily/weight < low:
                warnings.append("Below recommended range")
            if daily/weight > high:
                warnings.append("Above recommended range")

        if "max_day" in med_info and daily > med_info["max_day"]:
            warnings.append("Exceeds maximum daily dose")

        if "max_dose" in med_info and dose > med_info["max_dose"]:
            warnings.append("Exceeds maximum per dose")

        if warnings:
            for w in warnings:
                st.error(f"⚠️ {w}")
        else:
            st.success("✅ Ordered dose within recommended limits")

    # ---------------- Dispensing Calculator ----------------
    st.markdown("### 🧴 Dispensing Calculator")

    unit_disp = st.text_input("Medication unit (e.g., mg):", key="disp_unit", placeholder="mg")

    ordered_dose_dispense = st.number_input(
        f"Enter ordered dose ({unit_disp}):",
        min_value=0.0, step=0.1,
        value=st.session_state.get("sync_ordered_dose", 0.0),
        key="ordered_dose_dispense"
    )

    # Two-way sync
    if ordered_dose_dispense != st.session_state.sync_ordered_dose:
        st.session_state.sync_ordered_dose = ordered_dose_dispense
        st.session_state["ordered_dose_admin"] = ordered_dose_dispense

    st.markdown("### Medication Concentration")
    med_amount = st.text_input(f"Enter medication strength ({unit_disp}):", key="disp_med_amount", placeholder="e.g., 250")
    med_volume = st.text_input("Enter volume of solution (ml):", key="disp_med_volume", placeholder="e.g., 5")

    if st.button("Calculate Volume to Dispense"):
        try:
            ordered_val = float(ordered_dose_dispense)
            med_amount_val = float(med_amount)
            med_volume_val = float(med_volume)

            if med_amount_val > 0 and med_volume_val > 0:
                concentration_per_ml = med_amount_val / med_volume_val
                volume_to_dispense = ordered_val / concentration_per_ml
                st.success(f"➡️ Dispense: {volume_to_dispense:.2f} ml per dose")
                st.info(f"(Based on {med_amount_val} {unit_disp} per {med_volume_val} ml, "
                        f"concentration = {concentration_per_ml:.2f} {unit_disp}/ml)")
            else:
                st.warning("⚠️ Please enter valid medication strength and volume.")
        except ValueError:
            st.warning("⚠️ Please enter numeric values for dose, strength, and volume.")

# ------------------------------
elif st.session_state.page == "fluids":
    st.subheader("🧒 Pediatric Fluids Requirement")
    back_to_home()

    # --- Initialize defaults ---
    if "fluids_weight" not in st.session_state:
        st.session_state["fluids_weight"] = ""

    # --- Clear All ---
    if st.button("Clear All", key="clear_fluids"):
        st.session_state["fluids_weight"] = ""
        st.rerun()

    # --- Input ---
    weight_fluid = st.text_input("Enter child's weight (kg):", key="fluids_weight", placeholder="e.g., 12.5")

    # --- Rehydration option (always visible) ---
    option = st.radio(
        "Include Rehydration?",
        ["Maintenance Only", "Maintenance + 3% Rehydration", "Maintenance + 5% Rehydration"],
        index=0,
        key="rehydration_option"
    )

    # --- Calculation ---
    if st.button("Calculate Fluids Requirement", key="calc_fluids"):
        try:
            weight_val = float(weight_fluid)

            def calculate_fluids(weight):
                if weight <= 10:
                    return weight * 100
                elif weight <= 20:
                    return 1000 + (weight - 10) * 50
                else:
                    return 1500 + (weight - 20) * 20

            maintenance = calculate_fluids(weight_val)

            # Rehydration
            rehydration_3 = weight_val * 30   # 3%
            rehydration_5 = weight_val * 50   # 5%

            # Apply selection
            if option == "Maintenance Only":
                total = maintenance
            elif option == "Maintenance + 3% Rehydration":
                total = maintenance + rehydration_3
            elif option == "Maintenance + 5% Rehydration":
                total = maintenance + rehydration_5

            # ✅ Only show final result
            st.success(f"✅ Total Fluids: {total:.0f} ml/day | {total/24:.0f} ml/hr")

        except ValueError:
            st.warning("⚠️ Please enter a valid numeric weight.")

# ------------------------------
# 4. BMI
# ------------------------------
elif st.session_state.page == "bmi":
    st.subheader("⚖️ BMI Calculator")
    back_to_home()
    height_bmi = st.number_input("Height (cm):", min_value=0.0, step=0.1)
    weight_bmi = st.number_input("Weight (kg):", min_value=0.0, step=0.1)
    if st.button("Calculate BMI"):
        if height_bmi>0:
            bmi = weight_bmi/((height_bmi/100)**2)
            st.success(f"BMI: {bmi:.1f}")

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
    st.subheader("🍼 Corrected Age / Post Menstrual Age (Preterm Infants)")
    back_to_home()
    # Date of birth (preterm)
    dob_preterm = st.date_input("Date of Birth (Preterm)", key="dob_preterm")

    # Gestational age (weeks + days) side-by-side
    st.markdown("**Gestational Age at Birth:**")
    col1, col2 = st.columns(2)
    with col1:
        gestational_age_weeks = st.number_input(
            "Weeks", min_value=22, max_value=42, step=1, format="%d", key="gest_weeks"
        )
    with col2:
        gestational_age_days = st.number_input(
            "Days", min_value=0, max_value=6, step=1, format="%d", key="gest_days"
        )

    st.markdown(f"**Entered GA:** {gestational_age_weeks}+{gestational_age_days} weeks")

    # Current date
    current_date = st.date_input("Current Date", value=datetime.today(), key="current_date")

    # Validate dates
    chronological_age_days = (current_date - dob_preterm).days
    if chronological_age_days < 0:
        st.error("⚠️ Current date is before the date of birth. Please check your inputs.")
    else:
        # Chronological age
        chronological_weeks = chronological_age_days // 7
        chronological_days = chronological_age_days % 7
        st.write(f"📅 Chronological Age: **{chronological_weeks} weeks + {chronological_days} days**")

        # GA total days
        gestational_age_total_days = gestational_age_weeks * 7 + gestational_age_days

        # Correction for prematurity
        full_term_days = 40 * 7
        correction_days = full_term_days - gestational_age_total_days
        corrected_age_days = chronological_age_days - correction_days

        if corrected_age_days >= 0:
            corrected_weeks = corrected_age_days // 7
            corrected_days = corrected_age_days % 7
            st.success(
                f"✅ Corrected Age: **{corrected_weeks} weeks + {corrected_days} days**\n\n"
                "Corrected age is used for growth and developmental assessment in preterm infants."
            )
        else:
            pma_total_days = gestational_age_total_days + chronological_age_days
            pma_weeks = pma_total_days // 7
            pma_days = pma_total_days % 7
            st.info(
                f"ℹ️ Post-Menstrual Age (PMA): **{pma_weeks} weeks + {pma_days} days**\n\n"
                "PMA = gestational age at birth + chronological age."
            )


#7. Neonate feeds 
#------------------------------
elif st.session_state.page == "neonate_feeds":
    st.subheader("🍼 Neonate Feeds / IV Fluids Calculator")
    back_to_home()

    # --- Inputs with blank defaults ---
    weight_neonate = st.number_input(
        "Enter neonate weight (kg):",
        min_value=0.0,
        step=0.01,
        value=None,
        placeholder="Enter weight",
        key="ft_weight"
    )

    day_of_life = st.number_input(
        "Enter Day of Life:",
        min_value=1,
        step=1,
        value=None,
        placeholder="Enter day",
        key="ft_day"
    )

    feed_interval = st.radio(
        "Feeding Interval:",
        ["2-hourly", "3-hourly"],
        index=None,   # 👈 no default selection
        key="ft_interval"
    )

    # Feed ml/kg/day by day (default from day 4 onwards is 150 ml/kg/day)
    feed_dict = {1: 60, 2: 90, 3: 120}
    feed_ml_per_kg = feed_dict.get(day_of_life, 150) if day_of_life else None

    if st.button("Calculate Feeds", key="calc_feeds"):
        if weight_neonate is not None and day_of_life is not None and feed_interval is not None:
            total_feed = weight_neonate * feed_ml_per_kg
            feeds_per_day = 12 if feed_interval == "2-hourly" else 8
            feed_per_time = total_feed / feeds_per_day
            iv_fluids = weight_neonate * 100

            st.success(f"Total Feed Volume: {total_feed:.0f} ml/day")
            st.info(f"Feed Volume per Feed ({feed_interval}): {feed_per_time:.0f} ml")
            st.warning(f"IV Fluids Volume: {iv_fluids:.0f} ml/day")
        else:
            st.warning("⚠️ Please enter all inputs before calculating.")


# ------------------------------
# 8. Drug Compatibility
# ------------------------------
elif st.session_state.page == "compatibility":
    st.subheader("💉 Drug Compatibility")
    back_to_home()
    st.subheader("💉 Pediatric Y-Site Drug Compatibility Checker")
    drugs = ["Acetaminophen (Paracetamol)", "Acyclovir", "Amikacin", "Amoxicillin/Clavulanate (Co-amoxiclav)", "Ampicillin", "Ampicillin/Sulbactam (Unasyn)"]

    compatibility = {
        "Acetaminophen (Paracetamol)": {"Acyclovir": "Not compatible","Amikacin": "No information","Amoxicillin/Clavulanate (Co-amoxiclav)": "No information","Ampicillin": "No information","Ampicillin/Sulbactam (Unasyn)": "No information"},
        "Acyclovir": {"Acetaminophen (Paracetamol)": "Not compatible","Amikacin": "Compatible","Amoxicillin/Clavulanate (Co-amoxiclav)": "No information","Ampicillin": "Compatible","Ampicillin/Sulbactam (Unasyn)": "Not compatible"},
        "Amikacin": {"Acetaminophen (Paracetamol)": "No information","Acyclovir": "Compatible","Amoxicillin/Clavulanate (Co-amoxiclav)": "No information","Ampicillin": "Compatible if diluent is NaCl 0.9%","Ampicillin/Sulbactam (Unasyn)": "Compatible if diluent is NaCl 0.9%"},
        "Amoxicillin/Clavulanate (Co-amoxiclav)": {"Acetaminophen (Paracetamol)": "No information","Acyclovir": "No information","Amikacin": "No information","Ampicillin": "No information","Ampicillin/Sulbactam (Unasyn)": "No information"},
        "Ampicillin": {"Acetaminophen (Paracetamol)": "No information","Acyclovir": "Compatible","Amikacin": "Compatible if diluent is NaCl 0.9%","Amoxicillin/Clavulanate (Co-amoxiclav)": "No information","Ampicillin/Sulbactam (Unasyn)": "No information"},
        "Ampicillin/Sulbactam (Unasyn)": {"Acetaminophen (Paracetamol)": "No information","Acyclovir": "Not compatible","Amikacin": "Compatible if diluent is NaCl 0.9%","Amoxicillin/Clavulanate (Co-amoxiclav)": "No information","Ampicillin": "No information"}
    }

    drug1 = st.selectbox("Select Drug 1:", options=drugs, index=0)
    drug2 = st.selectbox("Select Drug 2:", options=drugs, index=1)

    if st.button("Check Compatibility"):
        if drug1 == drug2:
            st.info("✅ Same drug, usually compatible")
        else:
            result = compatibility.get(drug1, {}).get(drug2, "No information")
            if "Not compatible" in result:
                st.error(f"⚠️ {drug1} + {drug2}: {result}")
            elif "Compatible" in result:
                st.success(f"✅ {drug1} + {drug2}: {result}")
            else:
                st.warning(f"⚠️ {drug1} + {drug2}: {result}")

# 9. Vital Signs
# ------------------------------
elif st.session_state.page == "vitals":
    st.subheader("📊 Vital Signs Reference")
    back_to_home()
    st.subheader("📋 Vital Signs Checker")
    st.markdown(
        "Key in age and vital signs to check if they are within normal ranges. "
        "If the patient has fever, heart rate compensation is applied: **+10 bpm for every 1 °C above 37.0 °C**."
    )

    # --- Age input ---
    age_unit = st.radio("Age unit:", ["Months (<1 yr)", "Years (≥1 yr)"], index=None)

    age_months, age_years = None, None
    if age_unit == "Months (<1 yr)":
        age_months = st.number_input(
            "Age (months):",
            min_value=0,
            step=1,
            value=None,
            placeholder="Enter months",
            format="%d"
        )
        if age_months is not None:
            age_years = age_months / 12
    elif age_unit == "Years (≥1 yr)":
        age_years = st.number_input(
            "Age (years):",
            min_value=1,
            step=1,
            value=None,
            placeholder="Enter years",
            format="%d"
        )
        if age_years is not None:
            age_months = age_years * 12

    # --- Vital signs input ---
    hr = st.number_input("Heart Rate (bpm):", min_value=0, step=1, value=None, placeholder="Enter HR", format="%d")
    rr = st.number_input("Respiratory Rate (breaths/min):", min_value=0, step=1, value=None, placeholder="Enter RR", format="%d")
    sbp = st.number_input("Systolic BP (mmHg, optional):", min_value=0, step=1, value=None, placeholder="Enter SBP", format="%d")

    # --- Fever question ---
    fever = st.radio("Is there a fever? (Temperature >= 38°C)", ["No", "Yes"], index=0)
    temp = None
    if fever == "Yes":
        temp = st.number_input(
            "Enter Temperature (°C):",
            min_value=38.0,
            max_value=45.0,
            step=0.1,
            value=None,
            placeholder="Enter Temp",
            format="%.1f"
        )

    # --- Define normal ranges ---
    ranges = [
        (0, 3/12, (90, 180), (30, 60)),       # <3 months
        (3/12, 6/12, (80, 160), (30, 60)),    # 3–6 months
        (6/12, 12/12, (80, 140), (25, 45)),   # 6–12 months
        (1, 6, (75, 130), (20, 30)),          # 1–6 years
        (6, 10, (70, 110), (16, 24)),         # 6–10 years
        (10, 15, (60, 100), (14, 20)),        # 10–15 years
        (15, 200, (60, 100), (12, 20))        # 15+ years
    ]

    hr_range, rr_range = None, None
    if age_years is not None:
        for (low, high, hr_r, rr_r) in ranges:
            if low <= age_years < high:
                hr_range, rr_range = hr_r, rr_r
                break

    # --- SBP range ---
    sbp_range = None
    if age_years is not None:
        if age_years < 10:
            sbp_min = (age_years * 2) + 70
            sbp_range = (sbp_min, 120)
        else:
            sbp_range = (90, 120)

    # --- Adjust HR for fever ---
    adjusted_hr = hr 
    if temp is not None and hr is not None and temp > 37.0:
        compensation = int((temp - 37.0) * 10)
        adjusted_hr = hr - compensation
        st.info(f"Fever compensation applied: -{compensation} bpm "
                f"(HR adjusted to {adjusted_hr} bpm for analysis).")

    # --- Results ---
    if hr_range and hr is not None:
        if adjusted_hr < hr_range[0]:
            st.error(f"⚠️ Bradycardia: HR {hr} (adjusted {adjusted_hr}) below normal ({hr_range[0]}–{hr_range[1]})")
        elif adjusted_hr > hr_range[1]:
            st.error(f"⚠️ Tachycardia: HR {hr} (adjusted {adjusted_hr}) above normal ({hr_range[0]}–{hr_range[1]})")
        else:
            st.success(f"✅ HR {hr} (adjusted {adjusted_hr}) within normal range ({hr_range[0]}–{hr_range[1]})")

    if rr_range and rr is not None:
        if rr < rr_range[0]:
            st.error(f"⚠️ Bradypnea: RR {rr} below normal ({rr_range[0]}–{rr_range[1]})")
        elif rr > rr_range[1]:
            st.error(f"⚠️ Tachypnea: RR {rr} above normal ({rr_range[0]}–{rr_range[1]})")
        else:
            st.success(f"✅ RR {rr} within normal range ({rr_range[0]}–{rr_range[1]})")

    if sbp is not None and sbp_range:
        if sbp < sbp_range[0]:
            st.error(f"⚠️ Hypotension: SBP {sbp} below minimum ({sbp_range[0]})")
        elif sbp > sbp_range[1]:
            st.error(f"⚠️ Hypertension: SBP {sbp} above normal ({sbp_range[1]})")
        else:
            st.success(f"✅ SBP {sbp} within normal range ({sbp_range[0]}–{sbp_range[1]})")
    else:
        st.info("ℹ️ SBP not checked for this age")

# 10. Urine Output
#----------------------------------------------
elif st.session_state.page == "urine_output":
    st.subheader("🚰 Urine Output Calculator")
    back_to_home()
    st.subheader("🚰 Urine Output Calculator")

    # --- Initialize defaults ---
    if "uo_weight" not in st.session_state:
        st.session_state["uo_weight"] = ""
    if "uo_24h" not in st.session_state:
        st.session_state["uo_24h"] = ""
    if "uo_age_group" not in st.session_state:
        st.session_state["uo_age_group"] = None

    # --- Clear All ---
    if st.button("Clear All", key="clear_uo"):
        st.session_state["uo_weight"] = ""
        st.session_state["uo_24h"] = ""
        st.session_state["uo_age_group"] = None
        st.rerun()

    # --- Inputs ---
    age_group = st.radio(
        "Select Age Group:",
        ["Neonate (<28 days)", "Pediatric (≥28 days)"],
        index=0 if st.session_state["uo_age_group"] == "Neonate (<28 days)"
              else 1 if st.session_state["uo_age_group"] == "Pediatric (≥28 days)"
              else None,
        key="uo_age_group"
    )

    weight_uo = st.text_input("Enter weight (kg):", key="uo_weight", placeholder="e.g., 3.2")
    urine_24h = st.text_input("Enter total urine in 24 hours (ml):", key="uo_24h", placeholder="e.g., 150")

    # --- Calculation ---
    if st.button("Calculate Urine Output", key="calc_uo"):
        try:
            weight_val = float(weight_uo)
            urine_val = float(urine_24h)
            if weight_val > 0:
                uo_mlkg_hr = urine_val / weight_val / 24
                st.info(f"Urine Output: {uo_mlkg_hr:.2f} ml/kg/hr")

                if age_group == "Neonate (<28 days)":
                    if uo_mlkg_hr > 0.5:
                        st.success("✅ Within normal limits for neonates (>0.5 ml/kg/hr)")
                    else:
                        st.error("⚠️ Low urine output for neonates (<0.5 ml/kg/hr)")
                elif age_group == "Pediatric (≥28 days)":
                    if uo_mlkg_hr > 1:
                        st.success("✅ Within normal limits for pediatrics (>1 ml/kg/hr)")
                    else:
                        st.error("⚠️ Low urine output for pediatrics (<1 ml/kg/hr)")
            else:
                st.warning("⚠️ Please enter a valid weight.")
        except ValueError:
            st.warning("⚠️ Please enter numeric values for weight and urine volume.")