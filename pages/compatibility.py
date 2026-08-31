import streamlit as st
import pandas as pd


def run_compatibility_page():
    st.subheader("💉 Drug Compatibility Checker")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # SELECT PATIENT GROUP
    # =========================
    patient_group = st.radio(
        "Select Patient Group:",
        ["Paediatric", "Neonatal"],
        horizontal=True
    )

    # =========================
    # LOAD CORRECT CSV
    # =========================
    if patient_group == "Paediatric":
        df = pd.read_csv("data/compatibility.csv")
    else:
        df = pd.read_csv("data/neonatal_compatibility.csv")

    # =========================
    # GET ALL UNIQUE DRUGS
    # =========================
    drugs = sorted(
        list(
            set(df["Drug1"]).union(set(df["Drug2"]))
        )
    )

    drug1 = st.selectbox(
        "Select Drug 1:",
        drugs,
        index=0,
        key=f"drug1_{patient_group}"
    )

    drug2 = st.selectbox(
        "Select Drug 2:",
        drugs,
        index=1,
        key=f"drug2_{patient_group}"
    )

    if st.button("Check Compatibility"):

        # Same drug
        if drug1 == drug2:
            st.info("Same drug — compatibility should be verified according to clinical guidance.")

        else:
            # Search BOTH directions
            result_row = df[
                (
                    (df["Drug1"] == drug1) &
                    (df["Drug2"] == drug2)
                )
                |
                (
                    (df["Drug1"] == drug2) &
                    (df["Drug2"] == drug1)
                )
            ]

            # If found
            if not result_row.empty:

                result = str(result_row.iloc[0]["Compatibility"])

                # Neonatal CSV also contains Code
                code = None
                if "Code" in df.columns:
                    code = str(result_row.iloc[0]["Code"])

                if "Not compatible" in result:
                    st.error(f"⚠️ {result}")

                elif "No information" in result:
                    st.warning(f"ℹ️ {result}")

                elif "Compatible" in result:
                    st.success(f"✅ {result}")

                else:
                    st.warning(f"ℹ️ {result}")

                # Show neonatal code when available
                if patient_group == "Neonatal" and code:
                    st.caption(f"Compatibility code: {code}")

            else:
                st.warning("ℹ️ No information available")

    # =========================
    # DISCLAIMER
    # =========================
    if patient_group == "Neonatal":
        st.caption(
            "Neonatal compatibility information is intended as a clinical reference guide. "
            "Interpret results according to the patient's clinical situation and applicable pharmacy guidance."
        )
