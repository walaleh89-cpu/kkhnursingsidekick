import streamlit as st
import pandas as pd

def run_pews_page():

    st.subheader("📊 PEWS Calculator")

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # =====================================================
    # SCORING FUNCTIONS
    # =====================================================

    def score_hr(age, hr):

        if age == "<3 months":
            if hr <= 80 or hr >= 190: return 4
            elif 81 <= hr <= 90 or 180 <= hr <= 189: return 2
            elif 91 <= hr <= 110 or 150 <= hr <= 179: return 1
            elif 111 <= hr <= 149: return 0

        elif age == "3 months - <1 year":
            if hr <= 70 or hr >= 180: return 4
            elif 71 <= hr <= 80 or 170 <= hr <= 179: return 2
            elif 81 <= hr <= 100 or 150 <= hr <= 169: return 1
            elif 99 <= hr <= 149: return 0

        elif age == "1 - 4 years":
            if hr <= 60 or hr >= 170: return 4
            elif 61 <= hr <= 70 or 150 <= hr <= 169: return 2
            elif 71 <= hr <= 90 or 120 <= hr <= 149: return 1
            elif 91 <= hr <= 119: return 0

        elif age == ">4 - 12 years":
            if hr <= 50 or hr >= 150: return 4
            elif 51 <= hr <= 60 or 130 <= hr <= 149: return 2
            elif 61 <= hr <= 70 or 110 <= hr <= 129: return 1
            elif 71 <= hr <= 109: return 0

        elif age == ">12 years":
            if hr <= 40 or hr >= 140: return 4
            elif 41 <= hr <= 50 or 120 <= hr <= 139: return 2
            elif 51 <= hr <= 60 or 100 <= hr <= 119: return 1
            elif 61 <= hr <= 99: return 0

        return 0


    def score_rr(age, rr):

        if age == "<3 months":
            if rr <= 15 or rr >= 91: return 4
            elif 16 <= rr <= 19 or 81 <= rr <= 90: return 2
            elif 20 <= rr <= 29 or 61 <= rr <= 80: return 1
            elif 30 <= rr <= 60: return 0

        elif age == "3 months - <1 year":
            if rr <= 15 or rr >= 81: return 4
            elif 16 <= rr <= 19 or 71 <= rr <= 80: return 2
            elif 20 <= rr <= 24 or 51 <= rr <= 70: return 1
            elif 25 <= rr <= 50: return 0

        elif age == "1 - 4 years":
            if rr <= 12 or rr >= 71: return 4
            elif 13 <= rr <= 15 or 61 <= rr <= 70: return 2
            elif 16 <= rr <= 19 or 41 <= rr <= 60: return 1
            elif 20 <= rr <= 40: return 0

        elif age == ">4 - 12 years":
            if rr <= 10 or rr >= 51: return 4
            elif 11 <= rr <= 14 or 41 <= rr <= 50: return 2
            elif 15 <= rr <= 19 or 31 <= rr <= 40: return 1
            elif 20 <= rr <= 30: return 0

        elif age == ">12 years":
            if rr <= 9 or rr >= 30: return 4
            elif rr == 10 or 23 <= rr <= 29: return 2
            elif rr == 11 or 17 <= rr <= 22: return 1
            elif 12 <= rr <= 16: return 0

        return 0


    def score_sbp(age, sbp):

        if age == "<3 months":
            if sbp <= 45 or sbp >= 130: return 4
            elif 46 <= sbp <= 50 or 100 <= sbp <= 129: return 2
            elif 51 <= sbp <= 60 or 80 <= sbp <= 99: return 1
            elif 61 <= sbp <= 79: return 0

        elif age == "3 months - <1 year":
            if sbp <= 60 or sbp >= 150: return 4
            elif 61 <= sbp <= 70 or 120 <= sbp <= 149: return 2
            elif 71 <= sbp <= 80 or 100 <= sbp <= 119: return 1
            elif 81 <= sbp <= 99: return 0

        elif age == "1 - 4 years":
            if sbp <= 65 or sbp >= 160: return 4
            elif 66 <= sbp <= 75 or 125 <= sbp <= 159: return 2
            elif 76 <= sbp <= 90 or 110 <= sbp <= 124: return 1
            elif 91 <= sbp <= 109: return 0

        elif age == ">4 - 12 years":
            if sbp <= 70 or sbp >= 170: return 4
            elif 71 <= sbp <= 80 or 140 <= sbp <= 169: return 2
            elif 81 <= sbp <= 90 or 120 <= sbp <= 139: return 1
            elif 91 <= sbp <= 119: return 0

        elif age == ">12 years":
            if sbp <= 75 or sbp >= 190: return 4
            elif 76 <= sbp <= 85 or 150 <= sbp <= 189: return 2
            elif 86 <= sbp <= 100 or 130 <= sbp <= 149: return 1
            elif 101 <= sbp <= 129: return 0

        return 0


    def score_crt(crt):
        return 0 if crt == "≤2 sec" else 4


    def score_spo2(spo2):
        if spo2 >= 95:
            return 0
        elif 91 <= spo2 <= 94:
            return 1
        else:
            return 2


    def score_oxygen(oxygen):

        if oxygen == "Room Air":
            return 0

        elif oxygen == "≤5 L/min (NC/Facemask/Free Flow)":
            return 2

        elif oxygen == "≥6 L/min or ≥50%":
            return 4

        return 0


    def score_distress(distress):

        return {
            "None": 0,
            "Mild": 1,
            "Moderate": 2,
            "Severe": 4
        }[distress]


    # =====================================================
    # INPUTS
    # =====================================================

    age = st.selectbox(
        "Age Group",
        [
            "<3 months",
            "3 months - <1 year",
            "1 - 4 years",
            ">4 - 12 years",
            ">12 years"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        hr = st.number_input("Heart Rate", min_value=0)
        rr = st.number_input("Respiratory Rate", min_value=0)
        sbp = st.number_input("Systolic BP", min_value=0)

    with col2:
        spo2 = st.number_input("SpO₂ (%)", min_value=0, max_value=100)

        crt = st.selectbox(
            "Capillary Refill Time",
            ["≤2 sec", "≥3 sec"]
        )

        oxygen = st.selectbox(
            "Oxygen Delivery",
            [
                "Room Air",
                "≤5 L/min (NC/Facemask/Free Flow)",
                "≥6 L/min or ≥50%"
            ]
        )

    distress = st.selectbox(
        "Respiratory Distress",
        ["None", "Mild", "Moderate", "Severe"]
    )

    avpu = st.selectbox(
        "AVPU",
        ["Alert", "Voice", "Pain", "Unresponsive"]
    )

    # =====================================================
    # CALCULATE
    # =====================================================

    if st.button("Calculate PEWS"):

        hr_score = score_hr(age, hr)
        rr_score = score_rr(age, rr)
        sbp_score = score_sbp(age, sbp)
        crt_score = score_crt(crt)
        spo2_score = score_spo2(spo2)
        oxygen_score = score_oxygen(oxygen)
        distress_score = score_distress(distress)

        total_score = (
            hr_score +
            rr_score +
            sbp_score +
            crt_score +
            spo2_score +
            oxygen_score +
            distress_score
        )

        st.metric("Total PEWS Score", total_score)

        score_df = pd.DataFrame({
            "Parameter": [
                "Heart Rate",
                "Respiratory Rate",
                "Systolic BP",
                "CRT",
                "SpO₂",
                "Oxygen Delivery",
                "Respiratory Distress"
            ],
            "Score": [
                hr_score,
                rr_score,
                sbp_score,
                crt_score,
                spo2_score,
                oxygen_score,
                distress_score
            ]
        })

        st.dataframe(score_df, hide_index=True)

        critical_parameters = score_df[
            score_df["Score"] == 4
        ]["Parameter"].tolist()

        if critical_parameters:
            st.error(
                "Critical parameter(s): "
                + ", ".join(critical_parameters)
            )

        st.markdown("---")
        st.markdown("### Recommended Actions")

        if total_score <= 2:

            st.success("🟢 Routine Care")

            st.markdown("""
            **Frequency of EWS**
            - Once daily (AM)

            **Notification**
            - None
            """)

        elif 3 <= total_score <= 4 or avpu == "Voice":

            st.warning("🟡 Increased Monitoring")

            st.markdown("""
            **Intervention**
            - Recheck all EWS parameters
            - If still elevated:
            - HO review within 1 hour
            - Clinical assessment with MO/Reg

            **Frequency of EWS**
            - Q8H

            **Notification**
            - Non-intrusive notification to nurse
            """)

        elif 5 <= total_score <= 7 or avpu == "Pain":

            st.warning("🟠 Urgent Review")

            st.markdown("""
            **Intervention**
            - Recheck all EWS parameters
            - If still elevated:
            - MO review within 30 minutes

            **Frequency of EWS**
            - Q4H
            """)

        elif (
            total_score >= 8
            or avpu == "Unresponsive"
            or len(critical_parameters) > 0
        ):

            st.error("🔴 Critical Escalation")

            st.markdown("""
            **Intervention**
            - Recheck all EWS parameters
            - If still elevated:
            - Registrar review within 15 minutes
            - Continuous monitoring
            - Consider HD/ICU escalation
            - Consider Code Blue

            **Frequency of EWS**
            - Hourly (Q1H)
            - If persistently ≥8 for 4 hours:
            escalate to Consultant

            **Notification**
            1. Intrusive notification to nurse and documented doctor notification
            2. Mobile notification to RRT phone
            """)