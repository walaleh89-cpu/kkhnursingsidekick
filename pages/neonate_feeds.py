import streamlit as st

def run_neonate_feeds_page():
    st.subheader("🍼 Neonate Feeds / IV Fluids Calculator")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # INPUTS
    # =========================

    weight_neonate = st.number_input(
        "Enter neonate weight (kg):",
        min_value=0.0,
        step=0.01,
        value=None,
        placeholder="Enter weight",
        key="ft_weight"
    )

    # Day of life dropdown
    day_options = [
        "Day 1 of life",
        "Day 2 of life",
        "Day 3 of life",
        "Day 4–28 of life"
    ]

    day_selection = st.selectbox(
        "Select Day of Life:",
        options=day_options,
        index=None,
        placeholder="Choose day of life",
        key="ft_day"
    )

    feed_interval = st.radio(
        "Feeding Interval:",
        ["2-hourly", "3-hourly"],
        index=None,
        key="ft_interval"
    )

    # =========================
    # FEED VOLUME MAPPING
    # =========================

    feed_mapping = {
        "Day 1 of life": 60,
        "Day 2 of life": 90,
        "Day 3 of life": 120,
        "Day 4–28 of life": 150
    }

    feed_ml_per_kg = (
        feed_mapping.get(day_selection)
        if day_selection
        else None
    )

    # =========================
    # CALCULATIONS
    # =========================

    if st.button("Calculate Feeds", key="calc_feeds"):

        if (
            weight_neonate is not None
            and day_selection is not None
            and feed_interval is not None
        ):

            total_feed = weight_neonate * feed_ml_per_kg

            feeds_per_day = (
                12 if feed_interval == "2-hourly" else 8
            )

            feed_per_time = total_feed / feeds_per_day

            iv_fluids = weight_neonate * 100

            # =========================
            # RESULTS
            # =========================

            st.success(
                f"Total Feed Volume: {total_feed:.0f} ml/day"
            )

            st.info(
                f"Feed Volume per Feed ({feed_interval}): "
                f"{feed_per_time:.0f} ml"
            )

            st.warning(
                f"IV Fluids Volume: {iv_fluids:.0f} ml/day"
            )

            st.caption(
                "Note: Neonate feeds and IV fluids can vary "
                "based on clinical conditions."
            )

        else:
            st.warning(
                "⚠️ Please enter all inputs before calculating."
            )