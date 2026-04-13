import streamlit as st

def run_vitals_page():
    st.subheader("📊 Vital Signs Reference")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # AGE INPUT
    # =========================
    age_unit = st.radio(
        "Age unit:",
        ["Months (<1 yr)", "Years (≥1 yr)"],
        key="vs_unit"
    )

    age_years = None

    if age_unit == "Months (<1 yr)":
        age_months = st.number_input(
            "Age (months):",
            min_value=0,
            step=1,
            key="vs_months"
        )
        age_years = age_months / 12 if age_months else None

    else:
        age_years = st.number_input(
            "Age (years):",
            min_value=1,
            step=1,
            key="vs_years"
        )

    # =========================
    # VITAL SIGNS INPUTS
    # =========================
    hr = st.number_input("Heart Rate (bpm):", min_value=0, step=1, key="vs_hr")
    rr = st.number_input("Respiratory Rate:", min_value=0, step=1, key="vs_rr")
    sbp = st.number_input("Systolic BP (mmHg):", min_value=0, step=1, key="vs_sbp")

    # =========================
    # FEVER INPUT
    # =========================
    fever = st.radio("Fever (≥38°C)?", ["No", "Yes"], key="vs_fever")

    temp = None
    if fever == "Yes":
        temp = st.number_input(
            "Temperature (°C):",
            min_value=38.0,
            step=0.1,
            key="vs_temp"
        )

    # =========================
    # AGE RANGES
    # =========================
    ranges = [
        (0, 0.25, (90, 180), (30, 60)),
        (0.25, 0.5, (80, 160), (30, 60)),
        (0.5, 1, (80, 140), (25, 45)),
        (1, 6, (75, 130), (20, 30)),
        (6, 10, (70, 110), (16, 24)),
        (10, 15, (60, 100), (14, 20)),
        (15, 200, (60, 100), (12, 20))
    ]

    hr_range, rr_range = None, None

    if age_years is not None:
        for low, high, hr_r, rr_r in ranges:
            if low <= age_years < high:
                hr_range, rr_range = hr_r, rr_r
                break

    # =========================
    # SBP RANGE
    # =========================
    sbp_range = None

    if age_years is not None:
        if age_years < 10:
            sbp_min = (age_years * 2) + 70
            sbp_range = (sbp_min, 120)
        else:
            sbp_range = (90, 120)

    # =========================
    # FEVER HR ADJUSTMENT
    # =========================
    adjusted_hr = hr

    if temp and hr:
        compensation = int((temp - 37.0) * 10)
        adjusted_hr = hr - compensation
        st.info(f"Fever adjustment: -{compensation} bpm → {adjusted_hr} bpm")

    # =========================
    # RESULTS
    # =========================
    if hr_range and hr:
        if adjusted_hr < hr_range[0]:
            st.error(f"Bradycardia (HR {hr})")
        elif adjusted_hr > hr_range[1]:
            st.error(f"Tachycardia (HR {hr})")
        else:
            st.success(f"HR normal ({hr_range[0]}–{hr_range[1]})")

    if rr_range and rr:
        if rr < rr_range[0]:
            st.error("Bradypnea")
        elif rr > rr_range[1]:
            st.error("Tachypnea")
        else:
            st.success("RR normal")

    if sbp_range and sbp:
        if sbp < sbp_range[0]:
            st.error("Hypotension")
        elif sbp > sbp_range[1]:
            st.error("Hypertension")
        else:
            st.success("BP normal")