import streamlit as st
import pandas as pd

def run_compatibility_page():
    st.subheader("💉 Pediatric Drug Compatibility")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # LOAD CSV
    # =========================
    df = pd.read_csv("data/compatibility.csv")

    # =========================
    # GET ALL UNIQUE DRUGS
    # =========================
    drugs = sorted(
        list(
            set(df["Drug1"]).union(set(df["Drug2"]))
    )
)
    drug1 = st.selectbox("Select Drug 1:", drugs, index=0)
    drug2 = st.selectbox("Select Drug 2:", drugs, index=1)

    if st.button("Check Compatibility"):

        # Same drug
        if drug1 == drug2:
            st.info("Same drug — generally compatible")

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

                result = result_row.iloc[0]["Compatibility"]

                if "Not compatible" in result:
                    st.error(f"⚠️ {result}")

                elif "Compatible" in result:
                    st.success(f"✅ {result}")

                else:
                    st.warning(f"ℹ️ {result}")

            # If not found
            else:
                st.warning("ℹ️ No information available")