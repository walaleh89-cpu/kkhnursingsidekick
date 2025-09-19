import streamlit as st

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Nursing Calculator", page_icon="🩺", layout="centered")
st.title("🩺 Nursing Calculator App")
st.markdown("A collection of essential nursing calculators.")

# --- Create Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "💊 Drug Dosage", 
    "🧒 Pediatric Fluids Requirement", 
    "⚖️ BMI", 
    "🌞 Neonatal Jaundice",
    "🍼 Corrected Age",
    "🍼 Neonate Feeds",
    "💉 Drug Compatibility",
    "📊 Vital Signs",
    "🚰 Urine Output"
])

# --- Tab 1: Pediatric Dose Verification & Dispensing ---
with tab1:
    st.subheader("💊 Pediatric Dose Verification & Dispensing Calculator")
    
    # --- Patient Info ---
    st.markdown("<div style='background-color:#E3F2FD; padding:10px; border-radius:10px;'>"
                "<h4>🧍 Patient Info</h4></div>", unsafe_allow_html=True)
    weight = st.number_input("Enter patient weight (kg):", min_value=0.0, step=0.1, format="%.1f")
    
    # --- Medication Info ---
    st.markdown("<div style='background-color:#BBDEFB; padding:10px; border-radius:10px;'>"
                "<h4>💊 Medication Info</h4></div>", unsafe_allow_html=True)
    
    route_selection = st.selectbox("Select Route:", ["PO (Per oral)", "IV (Intravenous)"])
    route = "PO" if route_selection == "PO (Per oral)" else "IV"
    
    medications = {
        "PO": {
            "Antipyretics": {
                "Paracetamol": {"min_dose_per_kg": 10, "max_dose_per_kg": 15, "unit": "mg"},
                "Ibuprofen": {"min_dose_per_kg": 5, "max_dose_per_kg": 10, "unit": "mg"},
            },
            "Antibiotics": {
                "Amoxicillin": {"min_dose_per_kg": 20, "max_dose_per_kg": 40, "unit": "mg"},
                "Azithromycin": {"min_dose_per_kg": 10, "max_dose_per_kg": 12, "unit": "mg"},
            }
        },
        "IV": {
            "Antibiotics": {
                "Ceftriaxone": {"min_dose_per_kg": 50, "max_dose_per_kg": 75, "unit": "mg"},
                "Vancomycin": {"min_dose_per_kg": 10, "max_dose_per_kg": 15, "unit": "mg"},
            },
            "Analgesics": {
                "Morphine": {"min_dose_per_kg": 0.05, "max_dose_per_kg": 0.2, "unit": "mg"},
                "Fentanyl": {"min_dose_per_kg": 0.001, "max_dose_per_kg": 0.003, "unit": "mg"},
            }
        }
    }
    
    classification = st.selectbox("Select Classification:", list(medications[route].keys()))
    med = st.selectbox("Select Medication:", list(medications[route][classification].keys()))
    unit = medications[route][classification][med]["unit"]
    
    # --- Ordered Dose & Frequency ---
    ordered_dose = st.number_input(f"Enter ordered dose per administration ({unit}):", min_value=0.0, step=0.1, format="%.2f")
    frequency = st.number_input("Enter frequency (times per day):", min_value=1, step=1, value=1)
    
    if st.button("Check Dose"):
        med_info = medications[route][classification][med]
        min_per_kg = med_info["min_dose_per_kg"]
        max_per_kg = med_info["max_dose_per_kg"]
        
        # Calculations
        dose_per_kg = ordered_dose / weight if weight > 0 else 0
        daily_total = ordered_dose * frequency
        daily_per_kg = daily_total / weight if weight > 0 else 0
        
        # Display
        st.info(
            f"📏 **Recommended per dose:** {min_per_kg} – {max_per_kg} {unit}/kg\n"
            f"💊 **Ordered per dose:** {dose_per_kg:.2f} {unit}/kg\n"
            f"🗓 **Ordered daily total:** {daily_per_kg:.2f} {unit}/kg/day"
        )
        
        if weight <= 0:
            st.warning("⚠️ Please enter a valid patient weight to verify dose.")
        elif dose_per_kg < min_per_kg:
            st.warning("⚠️ Ordered dose is **below** recommended per-dose range")
        elif dose_per_kg > max_per_kg:
            st.warning("⚠️ Ordered dose is **above** recommended per-dose range")
        else:
            st.success("✅ Ordered dose is within recommended range")
    
    # --- Dispensing Calculation ---
    st.markdown("<div style='background-color:#C8E6C9; padding:10px; border-radius:10px;'>"
                "<h4>🧴 Dispensing Calculator</h4></div>", unsafe_allow_html=True)
    
    disp_ordered_dose = st.number_input(f"Enter ordered dose ({unit}):", min_value=0.0, step=0.1, format="%.2f", key="disp_dose")
    concentration = st.number_input(f"Enter concentration of medication ({unit}/ml):", min_value=0.0, step=0.1, format="%.2f")
    
    if st.button("Calculate Volume to Dispense"):
        if concentration > 0:
            volume = disp_ordered_dose / concentration
            st.success(f"➡️ Dispense: {volume:.2f} ml per dose")
        else:
            st.warning("⚠️ Please enter a valid concentration")

# --- Tab 2: Pediatric Fluids Requirement ---
with tab2:
    st.subheader("🧒 Pediatric Fluids Requirement (Holliday–Segar Method)")

    weight_fluid = st.number_input(
        "Enter child's weight (kg):", 
        min_value=0.0, 
        step=0.1, 
        format="%.1f", 
        key="weight_fluid"
    )

    def calculate_fluids(weight):
        if weight <= 0:
            return 0
        elif weight <= 10:
            return weight * 100
        elif weight <= 20:
            return (10 * 100) + (weight - 10) * 50
        else:
            return (10 * 100) + (10 * 50) + (weight - 20) * 20

    if st.button("Calculate Fluids Requirement", key="calc_fluids"):
        fluids = calculate_fluids(weight_fluid)
        hourly = fluids / 24 if fluids > 0 else 0

        st.success(
            f"💧 **Daily Maintenance Fluids Requirement:** {fluids:.0f} ml/day\n\n"
            f"⏱️ **Hourly Rate:** {hourly:.0f} ml/hr"
        )

        st.caption(
            "👉 Holliday–Segar Method:\n"
            "- 100 ml/kg/day for the first 10 kg\n"
            "- 50 ml/kg/day for the next 10 kg (10–20 kg)\n"
            "- 20 ml/kg/day for each kg above 20 kg"
        )

    # Side note for age restriction
    st.info("ℹ️ This calculation applies only to children **older than 28 days** (infants > 1 month).")

# --- Tab 3: BMI Calculator ---
with tab3:
    st.subheader("⚖️ BMI Calculator")
    height_bmi = st.number_input("Enter height (cm):", min_value=0.0, step=0.1, key="height_bmi")
    weight_bmi = st.number_input("Enter weight (kg):", min_value=0.0, step=0.1, key="weight_bmi")

    if st.button("Calculate BMI", key="calc_bmi"):
        if height_bmi > 0:
            bmi = weight_bmi / ((height_bmi / 100) ** 2)
            st.success(f"Your BMI: {bmi:.1f}")
            if bmi < 18.5:
                st.info("Underweight")
            elif 18.5 <= bmi < 24.9:
                st.success("Normal weight")
            elif 25 <= bmi < 29.9:
                st.warning("Overweight")
            else:
                st.error("Obese")
        else:
            st.error("Height must be greater than 0.")


# --- Tab 4: Neonatal Jaundice ---
# --- Tab 4: Neonatal Jaundice ---
with tab4:
    st.subheader("🌞 Neonatal Jaundice Guidelines")
    dob = st.date_input("Date of Birth")
    time_of_birth_str = st.text_input("Time of Birth (HH:MM, 24-hour format):", value="00:00")

    hours_of_life = None
    try:
        birth_hour, birth_minute = map(int, time_of_birth_str.split(":"))
        birth_datetime = datetime.combine(dob, datetime.min.time()).replace(hour=birth_hour, minute=birth_minute)
        current_datetime = datetime.now()
        hours_of_life = (current_datetime - birth_datetime).total_seconds() / 3600
        st.success(f"✅ Hours of Life: {hours_of_life:.1f} hours")
    except Exception:
        st.warning("Please enter time in HH:MM format, e.g., 14:30.")

    st.markdown("**Select Risk Factors:**")
    risk_factors = st.multiselect(
        "Check all that apply:",
        [
            "Gestational age < 38 weeks",
            "Hemolysis (ABO/Rh incompatibility)",
            "G6PD deficiency",
            "Previous sibling required phototherapy",
            "Significant clinical illness"
        ]
    )
    auto_risk = "High-Risk" if len(risk_factors) > 0 else "Normal-Risk"
    selected_risk = st.radio(
        "Infant Risk Category (can override):",
        ["High-Risk", "Normal-Risk"],
        index=0 if auto_risk == "High-Risk" else 1
    )

    measurement_type = st.radio("Measurement Type:", ["Transcutaneous Bilirubin (TcB)", "Serum Bilirubin (SB)"])

    # TcB Threshold Function
    def tcb_to_sb_needed(hours, risk, tcb):
        rules_normal = [(25,36,160),(37,48,180),(49,72,200),(73,96,220),(97,120,220),(121,168,240),(169,336,250)]
        rules_high = [(0,12,80),(13,24,120),(25,36,140),(37,48,160),(49,72,180),(73,96,200),(97,120,200),(121,168,220),(169,336,240)]
        rules = rules_high if risk=="High-Risk" else rules_normal
        for start,end,threshold in rules:
            if start <= hours <= end:
                return tcb > threshold
        return False

    # High-Risk SB Evaluation
    def get_jaundice_category_highrisk(age, sb):
        rules = [
            (0,12, [100,150,175,200]),
            (13,24,[150,200,225,250]),
            (25,36,[135,175,225,250,275]),
            (37,48,[160,200,250,275,300]),
            (49,72,[185,225,275,300,325]),
            (73,96,[210,250,300,325,350]),
            (97,120,[210,250,300,325,350]),
            (121,168,[235,275,325,350,375]),
            (169,336,[260,300,325,350,375])
        ]
        for start,end,thr in rules:
            if start <= age <= end:
                if sb < thr[0]:
                    return ("🟢 Stop phototherapy or continue monitoring SB for outpatient", "lightblue")
                elif sb < thr[1]:
                    return ("🟢 Continue monitoring", "lightgreen")
                elif sb < thr[2]:
                    return ("🟡 Single blue phototherapy", "khaki")
                elif sb < thr[3]:
                    return ("🟠 Double blue phototherapy", "orange")
                elif sb < thr[4]:
                    return ("🔴 Intense phototherapy", "tomato")
                else:
                    return ("⚠️ Exchange transfusion indicated", "red")
        return ("Age out of range (0–14 days)", "lightgray")

    # Normal-Risk SB Evaluation
    def get_jaundice_category_normal(age, sb):
        rules = [
            (25,36,[160,200,250,275,300]),
            (37,48,[185,225,300,325,350]),
            (49,72,[210,250,300,325,350]),
            (73,96,[235,275,325,350,375]),
            (97,120,[235,275,350,375,400]),
            (121,168,[260,300,350,375,400]),
            (169,336,[285,325,375,400,425])
        ]
        for start,end,thr in rules:
            if start <= age <= end:
                if sb < thr[0]:
                    return ("🟢 Stop phototherapy or continue monitoring SB for outpatient", "lightblue")
                elif sb < thr[1]:
                    return ("🟢 Continue monitoring", "lightgreen")
                elif sb < thr[2]:
                    return ("🟡 Single blue phototherapy", "khaki")
                elif sb < thr[3]:
                    return ("🟠 Double blue phototherapy", "orange")
                elif sb < thr[4]:
                    return ("🔴 Intense phototherapy", "tomato")
                else:
                    return ("⚠️ Exchange transfusion indicated", "red")
        return ("Age out of range (25h – 14 days)", "lightgray")

    # Display results
    if hours_of_life is not None:
        if measurement_type == "Transcutaneous Bilirubin (TcB)":
            tcb_value = st.number_input("Enter TcB level (µmol/L):", min_value=0, key="tcb_input")
            if st.button("Evaluate TcB"):
                need_sb = tcb_to_sb_needed(hours_of_life, selected_risk, tcb_value)
                if need_sb:
                    st.warning("⚠️ TcB exceeds threshold – perform Serum Bilirubin test")
                else:
                    st.success("✅ TcB below threshold – no immediate SB needed")
        else:
            sb_level = st.number_input("Enter SB level (µmol/L):", min_value=0, key="sb_input")
            if st.button("Evaluate SB"):
                if selected_risk == "High-Risk":
                    message, color = get_jaundice_category_highrisk(hours_of_life, sb_level)
                else:
                    message, color = get_jaundice_category_normal(hours_of_life, sb_level)
                st.markdown(
                    f"<div style='background-color:{color}; padding:15px; border-radius:10px; font-weight:bold; text-align:center;'>{message}</div>",
                    unsafe_allow_html=True
                )

# --- Tab 5: Corrected Age ---
with tab5:
    st.subheader("🍼 Corrected Age / Post Menstrual Age (Preterm Infants)")

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

# --- Tab 6: Neonate Feeds ---
with tab6:
    st.subheader("🍼 Neonate Feeds / IV Fluids Calculator")
    weight_neonate = st.number_input("Enter neonate weight (kg):", min_value=0.0, step=0.01, key="ft_weight")
    day_of_life = st.number_input("Enter Day of Life:", min_value=1, max_value=28, step=1, key="ft_day")
    feed_interval = st.radio("Feeding Interval:", ["2-hourly", "3-hourly"], key="ft_interval")

    feed_dict = {1: 60, 2: 90, 3: 120}
    feed_ml_per_kg = feed_dict.get(day_of_life, 150)

    if st.button("Calculate Feeds", key="calc_feeds"):
        total_feed = weight_neonate * feed_ml_per_kg
        feeds_per_day = 12 if feed_interval == "2-hourly" else 8
        feed_per_time = total_feed / feeds_per_day
        iv_fluids = weight_neonate * 100

        st.success(f"Total Feed Volume: {total_feed:.0f} ml/day")
        st.info(f"Feed Volume per Feed ({feed_interval}): {feed_per_time:.0f} ml")
        st.warning(f"IV Fluids Volume: {iv_fluids:.0f} ml/day")

# --- Tab 7: Drug Compatibility ---
with tab7:
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
                
with tab8:
    st.subheader("📋 Vital Signs Checker")
    st.markdown(
        "Key in age and vital signs to check if they are within normal ranges. "
        "If the patient has fever, heart rate compensation is applied: **+10 bpm for every 1 °C above 37.0 °C**."
    )

    # Age input
    age_unit = st.radio("Age unit:", ["Months (<1 yr)", "Years (≥1 yr)"])
    if age_unit == "Months (<1 yr)":
        age_months = st.number_input("Age (months):", min_value=0, step=1, value=0, format="%d")
        age_months = int(age_months)
        age_years = age_months / 12
    else:
        age_years = st.number_input("Age (years):", min_value=1, step=1, value=1, format="%d")
        age_years = int(age_years)
        age_months = age_years * 12

    # Vital signs input
    hr = st.number_input("Heart Rate (bpm):", min_value=0, step=1, format="%d")
    rr = st.number_input("Respiratory Rate (breaths/min):", min_value=0, step=1, format="%d")
    sbp = st.number_input("Systolic BP (mmHg, optional):", min_value=0, step=1, format="%d")
    temp = st.number_input("Temperature (°C, optional):", min_value=30.0, max_value=45.0, step=0.1, format="%.1f")

    # Define normal ranges
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
    for (low, high, hr_r, rr_r) in ranges:
        if low <= age_years < high:
            hr_range, rr_range = hr_r, rr_r
            break

    # SBP minimum for <10 years
    sbp_range = None
    if age_years < 10:
        sbp_min = (age_years * 2) + 70
        sbp_range = (sbp_min, 120)  # arbitrary upper reference
    else:
        sbp_range = (90, 120)

    # Adjust HR for fever
    adjusted_hr = hr
    if temp and temp > 37.0:
        compensation = int((temp - 37.0) * 10)
        adjusted_hr = hr - compensation
        st.info(f"Fever compensation applied: -{compensation} bpm "
                f"(HR adjusted to {adjusted_hr} bpm for analysis).")

    # Results
    if hr_range:
        if adjusted_hr < hr_range[0]:
            st.error(f"⚠️ Bradycardia: HR {hr} (adjusted {adjusted_hr}) below normal ({hr_range[0]}–{hr_range[1]})")
        elif adjusted_hr > hr_range[1]:
            st.error(f"⚠️ Tachycardia: HR {hr} (adjusted {adjusted_hr}) above normal ({hr_range[0]}–{hr_range[1]})")
        else:
            st.success(f"✅ HR {hr} (adjusted {adjusted_hr}) within normal range ({hr_range[0]}–{hr_range[1]})")

    if rr_range:
        if rr < rr_range[0]:
            st.error(f"⚠️ Bradypnea: RR {rr} below normal ({rr_range[0]}–{rr_range[1]})")
        elif rr > rr_range[1]:
            st.error(f"⚠️ Tachypnea: RR {rr} above normal ({rr_range[0]}–{rr_range[1]})")
        else:
            st.success(f"✅ RR {rr} within normal range ({rr_range[0]}–{rr_range[1]})")

    if sbp:
        if sbp < sbp_range[0]:
            st.error(f"⚠️ Hypotension: SBP {sbp} below minimum ({sbp_range[0]})")
        elif sbp > sbp_range[1]:
            st.error(f"⚠️ Hypertension: SBP {sbp} above normal ({sbp_range[1]})")
        else:
            st.success(f"✅ SBP {sbp} within normal range ({sbp_range[0]}–{sbp_range[1]})")
    else:
        st.info("ℹ️ SBP not checked for this age")

# --- Tab 9: Urine Output ---
with tab9:
    st.subheader("🚰 Urine Output Calculator")

    age_group = st.radio("Select Age Group:", ["Neonate (<28 days)", "Pediatric (≥28 days)"])
    weight_uo = st.number_input("Enter weight (kg):", min_value=0.0, step=0.1, key="uo_weight")
    urine_24h = st.number_input("Enter total urine in 24 hours (ml):", min_value=0.0, step=1.0, key="uo_24h")

    if st.button("Calculate Urine Output", key="calc_uo"):
        if weight_uo > 0:
            uo_mlkg_hr = urine_24h / weight_uo / 24
            st.info(f"Urine Output: {uo_mlkg_hr:.2f} ml/kg/hr")

            if age_group == "Neonate (<28 days)":
                if uo_mlkg_hr > 0.5:
                    st.success("✅ Within normal limits for neonates (>0.5 ml/kg/hr)")
                else:
                    st.error("⚠️ Low urine output for neonates (<0.5 ml/kg/hr)")
            else:
                if uo_mlkg_hr > 1:
                    st.success("✅ Within normal limits for pediatrics (>1 ml/kg/hr)")
                else:
                    st.error("⚠️ Low urine output for pediatrics (<1 ml/kg/hr)")
        else:
            st.warning("Please enter a valid weight.")
