import streamlit as st

def run_urine_output_page():
    st.subheader("🚰 Urine Output Calculator")

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # INPUTS
    # =========================

    age_group = st.radio(
        "Select Age Group:",
        ["Neonate (<28 days)", "Pediatric (≥28 days)"],
        key="uo_age_group"
    )

    weight = st.number_input(
        "Weight (kg):",
        min_value=0.0,
        step=0.1,
        key="uo_weight"
    )

    urine_24h = st.number_input(
        "Total urine in 24 hours (ml):",
        min_value=0.0,
        step=1.0,
        key="uo_urine"
    )

    # =========================
    # CLEAR BUTTON
    # =========================
    if st.button("Clear All", key="clear_uo"):
        st.session_state["uo_weight"] = 0.0
        st.session_state["uo_urine"] = 0.0
        st.rerun()

    # =========================
    # CALCULATION
    # =========================
    if st.button("Calculate Urine Output", key="calc_uo"):

        if weight > 0 and urine_24h > 0:

            uo_mlkg_hr = urine_24h / weight / 24

            st.info(f"Urine Output: {uo_mlkg_hr:.2f} ml/kg/hr")

            # =========================
            # HIGH OUTPUT WARNING
            # =========================
            if uo_mlkg_hr > 4:
                st.warning(
                    "⚠️ High urine output (>4 ml/kg/hr). "
                    "Correlate clinically as this may suggest polyuria."
                )

            # =========================
            # NEONATE
            # =========================
            if age_group == "Neonate (<28 days)":

                if uo_mlkg_hr < 0.5:
                    st.error("⚠️ Low urine output")
                else:
                    st.success("✅ Normal (>0.5 ml/kg/hr)")

            # =========================
            # PEDIATRIC
            # =========================
            else:

                if uo_mlkg_hr < 1.0:
                    st.error("⚠️ Low urine output")
                else:
                    st.success("✅ Normal (>1 ml/kg/hr)")

        else:
            st.warning("Please enter valid values.")