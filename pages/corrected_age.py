import streamlit as st
from datetime import datetime

def run_corrected_age_page():
    st.subheader("🍼 Corrected Age / Post Menstrual Age")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun() 
 
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

