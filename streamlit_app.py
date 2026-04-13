import streamlit as st
from datetime import datetime
import pytz
from pages.dosage import run_dosage_page 
from pages.fluids import run_fluids_page
from pages.bmi import run_bmi_page
from pages.neonatal_jaundice import run_neonatal_jaundice_page
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
    run_neonatal_jaundice_page()

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