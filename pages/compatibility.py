import streamlit as st

def run_compatibility_page():
    st.subheader("💉 Pediatric Drug Compatibility")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # DRUG LIST
    # =========================
    drugs = [
        "Acetaminophen (Paracetamol)",
        "Acyclovir",
        "Amikacin",
        "Amoxicillin/Clavulanate (Co-amoxiclav)",
        "Ampicillin",
        "Ampicillin/Sulbactam (Unasyn)"
    ]

    # =========================
    # COMPATIBILITY DATA
    # =========================
    compatibility = {
        "Acetaminophen (Paracetamol)": {
            "Acyclovir": "Not compatible",
            "Amikacin": "No information",
            "Amoxicillin/Clavulanate (Co-amoxiclav)": "No information",
            "Ampicillin": "No information",
            "Ampicillin/Sulbactam (Unasyn)": "No information"
        },
        "Acyclovir": {
            "Acetaminophen (Paracetamol)": "Not compatible",
            "Amikacin": "Compatible",
            "Amoxicillin/Clavulanate (Co-amoxiclav)": "No information",
            "Ampicillin": "Compatible",
            "Ampicillin/Sulbactam (Unasyn)": "Not compatible"
        },
        "Amikacin": {
            "Acetaminophen (Paracetamol)": "No information",
            "Acyclovir": "Compatible",
            "Amoxicillin/Clavulanate (Co-amoxiclav)": "No information",
            "Ampicillin": "Compatible if NaCl 0.9% used",
            "Ampicillin/Sulbactam (Unasyn)": "Compatible if NaCl 0.9% used"
        },
        "Amoxicillin/Clavulanate (Co-amoxiclav)": {
            "Acetaminophen (Paracetamol)": "No information",
            "Acyclovir": "No information",
            "Amikacin": "No information",
            "Ampicillin": "No information",
            "Ampicillin/Sulbactam (Unasyn)": "No information"
        },
        "Ampicillin": {
            "Acetaminophen (Paracetamol)": "No information",
            "Acyclovir": "Compatible",
            "Amikacin": "Compatible if NaCl 0.9% used",
            "Amoxicillin/Clavulanate (Co-amoxiclav)": "No information",
            "Ampicillin/Sulbactam (Unasyn)": "No information"
        },
        "Ampicillin/Sulbactam (Unasyn)": {
            "Acetaminophen (Paracetamol)": "Not compatible",
            "Acyclovir": "Not compatible",
            "Amikacin": "Compatible if NaCl 0.9% used",
            "Amoxicillin/Clavulanate (Co-amoxiclav)": "No information",
            "Ampicillin": "No information"
        }
    }

    # =========================
    # UI
    # =========================
    drug1 = st.selectbox("Select Drug 1:", drugs, index=0)
    drug2 = st.selectbox("Select Drug 2:", drugs, index=1)

    if st.button("Check Compatibility"):
        if drug1 == drug2:
            st.info("Same drug — generally compatible")
        else:
            result = compatibility.get(drug1, {}).get(drug2, "No information")

            if "Not compatible" in result:
                st.error(f"⚠️ {result}")
            elif "Compatible" in result:
                st.success(f"✅ {result}")
            else:
                st.warning(f"ℹ️ {result}")