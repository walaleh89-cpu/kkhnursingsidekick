import streamlit as st
from datetime import datetime
import pytz

def run_community_nurse_page():

    st.subheader("👶 Community Nurse Tools")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("---")

    # Singapore time
    sg_tz = pytz.timezone("Asia/Singapore")
    now_sg = datetime.now(sg_tz)

    # =========================
    # 1. HOURS OF LIFE
    # =========================
    st.markdown("## ⏰ Hours of Life Calculator")

    dob = st.date_input("Date of Birth", key="cn_dob")

    # Manual time input (HH:MM)
    tob_str = st.text_input(
        "Time of Birth (HH:MM)",
        placeholder="e.g. 14:35",
        key="cn_tob"
    )

    current_date = st.date_input(
        "Current Date",
        value=now_sg.date(),
        key="cn_current_date"
    )

    current_time = st.time_input(
        "Current Time (Singapore Time)",
        value=now_sg.time(),
        key="cn_current_time"
    )

    # Convert HH:MM safely
    tob = None
    if tob_str:
        try:
            tob = datetime.strptime(tob_str, "%H:%M").time()
        except ValueError:
            st.error("⚠️ Invalid Time of Birth format. Please use HH:MM (e.g. 09:45)")

    # =========================
    # CALCULATION BLOCK
    # =========================
    if dob and tob and current_date and current_time:

        birth_datetime = datetime.combine(dob, tob)
        current_datetime = datetime.combine(current_date, current_time)

        hours_of_life = (current_datetime - birth_datetime).total_seconds() / 3600

        if hours_of_life < 0:
            st.error("⚠️ Current date/time is before birth date/time.")
        else:
            st.success(f"✅ Hours of Life: **{hours_of_life:.1f} hours**")

            st.markdown("---")

            # =========================
            # 2. WEIGHT LOSS CALCULATOR
            # =========================
            st.markdown("## ⚖️ Weight Loss Calculator")

            birthweight = st.number_input(
                "Birth Weight (g)",
                min_value=0.0,
                step=1.0,
                key="birthweight"
            )

            current_weight = st.number_input(
                "Current Weight (g)",
                min_value=0.0,
                step=1.0,
                key="current_weight"
            )

            if birthweight > 0 and current_weight > 0:

                weight_loss_percent = (
                    (birthweight - current_weight)
                    / birthweight
                ) * 100

                # ✅ NEW LOGIC: No weight loss case
                if weight_loss_percent <= 0:
                    st.success("✅ No weight loss")

                elif weight_loss_percent > 10:
                    st.error(
                        f"🚨 Weight Loss: **{weight_loss_percent:.1f}%**"
                    )

                else:
                    st.success(
                        f"✅ Weight Loss: **{weight_loss_percent:.1f}%**"
                    )

            st.markdown("---")

            # =========================
            # 3. NEONATE FEED GUIDE
            # =========================
            st.markdown("## 🍼 Neonate Feed Guide")

            if hours_of_life < 24:
                feed_recommendation = "10 mL/feed"

            elif 24 <= hours_of_life < 48:
                feed_recommendation = "10–15 mL/feed"

            elif 48 <= hours_of_life < 72:
                feed_recommendation = "15–30 mL/feed"

            elif 72 <= hours_of_life < 96:
                feed_recommendation = "30–60 mL/feed"

            else:
                feed_recommendation = "Refer to institutional feeding guidelines"

            st.info(
                f"Recommended Feed Volume: **{feed_recommendation}**"
            )

            st.caption(
                "Guideline applicable to all term well babies ≥37 weeks gestation."
            )