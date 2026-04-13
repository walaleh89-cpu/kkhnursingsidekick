import streamlit as st

def run_bmi_page():
    st.subheader("⚖️ BMI Calculator")

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # ALWAYS independent inputs (NO self-reference)
    height_bmi = st.number_input(
        "Height (cm):",
        min_value=0.0,
        step=0.1,
        value=0.0,
        key="bmi_height"
    )

    weight_bmi = st.number_input(
        "Weight (kg):",
        min_value=0.0,
        step=0.1,
        value=0.0,
        key="bmi_weight"
    )

    if st.button("Calculate BMI"):
        if height_bmi > 0 and weight_bmi > 0:
            bmi = weight_bmi / ((height_bmi / 100) ** 2)
            st.success(f"BMI: {bmi:.1f}")
        else:
            st.warning("Please enter both height and weight.")