import streamlit as st

def run_fluids_page():
    st.subheader("🧒 Pediatric Fluids Requirement")

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    weight_fluid = st.text_input(
        "Enter child's weight (kg):",
        key="fluids_weight",
        placeholder="e.g., 12.5"
    )

    option = st.radio(
        "Include Rehydration?",
        ["Maintenance Only", "Maintenance + 3% Rehydration", "Maintenance + 5% Rehydration"],
        index=0,
        key="rehydration_option"
    )

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
            rehydration_3 = weight_val * 30
            rehydration_5 = weight_val * 50

            if option == "Maintenance Only":
                total = maintenance
            elif option == "Maintenance + 3% Rehydration":
                total = maintenance + rehydration_3
            else:
                total = maintenance + rehydration_5

            st.success(f"{total:.0f} ml/day | {total/24:.0f} ml/hr")

        except ValueError:
            st.warning("Enter valid weight.")