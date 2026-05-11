import streamlit as st
from data.antibiotics_data import antibiotics_data
from data.others_data import others_data

def run_dosage_page():

    st.subheader("💊 Dosage Verification / Dispensing Calculator")
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # ------------------------------
    # Inputs
    # ------------------------------
    weight = st.number_input("Patient weight (kg)", min_value=0.1, step=0.1)

    med_group = st.radio(
        "Medication group",
        ["Antibiotics", "Others"],
        horizontal=True
    )

    med_info = None

    # ---------------- ANTIBIOTICS ----------------
    if med_group == "Antibiotics":
        system = st.radio("Diagnosis by system", list(antibiotics_data.keys()), horizontal=True)

        med_search = st.text_input("Search antibiotic").strip()

        available_meds = sorted(antibiotics_data.get(system, {}).keys())

        filtered_meds = [
            m for m in available_meds
            if med_search.lower() in m.lower()
        ] if med_search else available_meds

        if not filtered_meds:
            st.warning("No antibiotic found.")
            st.stop()

        med = st.selectbox("Medication", filtered_meds)
        med_options = antibiotics_data[system][med]

        if len(med_options) == 1:
            selected_option = med_options[0]
        else:
            option_labels = [opt["route"] for opt in med_options]
            selected_label = st.radio("Choose route", option_labels, horizontal=True)
            selected_option = med_options[option_labels.index(selected_label)]

        med_info = selected_option

    # ---------------- OTHERS ----------------
    else:
        med_search = st.text_input("Search medication").strip()

        available_meds = sorted(others_data.keys())

        filtered_meds = [
            m for m in available_meds
            if med_search.lower() in m.lower()
        ] if med_search else available_meds

        if not filtered_meds:
            st.warning("No medication found.")
            st.stop()

        med = st.selectbox("Medication", filtered_meds)
        med_options = others_data[med]

        if len(med_options) == 1:
            selected_option = med_options[0]
        else:
            option_labels = [opt["route"] for opt in med_options]
            selected_label = st.radio("Choose route", option_labels, horizontal=True)
            selected_option = med_options[option_labels.index(selected_label)]

        med_info = selected_option

    if med_info is None:
        st.stop()

    st.markdown(f"**Route:** {med_info['route']}")
    st.markdown(f"**Unit:** {med_info['unit']}")

    # ------------------------------
    # Dose Inputs
    # ------------------------------
    dose = st.number_input(
        f"Ordered dose ({med_info['unit']})",
        min_value=0.0,
        step=0.1
    )

    freq_map = {"Q24H":1, "Q12H":2, "Q8H":3, "Q6H":4}
    freq = freq_map[st.selectbox("Frequency", list(freq_map.keys()))]

    # ------------------------------
    # MAIN BUTTON
    # ------------------------------
    if st.button("Check Dose", key="check_dose_main"):

        st.markdown("### ⚖️ Recommended vs Ordered Dose")

        key = "usual"
        daily = dose * freq

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📘 Recommended")

            if key in med_info:
                low, high = med_info[key]
                st.write(f"{low}–{high} mg/kg/day")
                st.write(f"{(low*weight/freq):.1f}–{(high*weight/freq):.1f} mg/dose")

        with col2:
            st.markdown("#### 📊 Ordered")
            st.write(f"{(daily/weight):.2f} mg/kg/day")
            st.write(f"{dose:.1f} mg/dose")

        # ---------------- Safety ----------------
        warnings = []

        if key in med_info:
            low, high = med_info[key]
            if daily/weight < low:
                warnings.append("Below recommended range")
            if daily/weight > high:
                warnings.append("Above recommended range")

        if "max_day" in med_info and daily > med_info["max_day"]:
            warnings.append("Exceeds max daily dose")

        if "max_dose" in med_info and dose > med_info["max_dose"]:
            warnings.append("Exceeds max per dose")

        for w in warnings:
            st.warning(w)

    # ------------------------------
    # DISPENSING CALCULATOR
    # ------------------------------
    st.markdown("### 🧴 Dispensing Calculator")

    # Ordered dose
    ordered_dose = st.number_input(
        "Enter ordered dose",
        min_value=0.0,
        step=0.1,
        key="ordered_dose"
    )

    # Unit dropdown
    dose_unit = st.selectbox(
        "Select unit",
        ["g", "mg", "mcg", "unit"],
        key="dose_unit"
    )

    # Medication form
    med_form = st.radio(
        "Medication form",
        ["Solution", "Tablet / Capsule"],
        key="med_form"
    )

    st.markdown("---")

    # =========================
    # SOLUTION
    # =========================
    if med_form == "Solution":

        st.markdown("#### 💧 Solution Strength")

        solution_strength = st.number_input(
            f"Medication strength ({dose_unit})",
            min_value=0.0,
            step=0.1,
            key="solution_strength"
        )

        solution_volume = st.number_input(
            "In how many ml?",
            min_value=0.1,
            step=0.1,
            key="solution_volume"
        )

        if st.button("Calculate Volume", key="calc_solution"):

            try:
                concentration = solution_strength / solution_volume
                required_volume = ordered_dose / concentration

                st.success(f"➡️ Dispense: {required_volume:.2f} ml")

            except:
                st.warning("Invalid input")


    # =========================
    # TABLET / CAPSULE
    # =========================
    else:

        st.markdown("#### 💊 Tablet / Capsule Strength")

        tablet_strength = st.number_input(
            f"Medication strength per tablet/capsule ({dose_unit})",
            min_value=0.0,
            step=0.1,
            key="tablet_strength"
        )

        if st.button("Calculate Tablets", key="calc_tablet"):

            try:
                tablets_needed = ordered_dose / tablet_strength

                st.success(f"➡️ Give: {tablets_needed:.2f} tablet(s) / capsule(s)")

            except:
                st.warning("Invalid input")