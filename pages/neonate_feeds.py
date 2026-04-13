import streamlit as st

def run_neonate_feeds_page():
    st.subheader("🍼 Neonate Feeds / IV Fluids Calculator")

    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()
        # --- Inputs with blank defaults ---
    weight_neonate = st.number_input(
        "Enter neonate weight (kg):",
        min_value=0.0,
        step=0.01,
        value=None,
        placeholder="Enter weight",
        key="ft_weight"
    )

    day_of_life = st.number_input(
        "Enter Day of Life:",
        min_value=1,
        step=1,
        value=None,
        placeholder="Enter day",
        key="ft_day"
    )

    feed_interval = st.radio(
        "Feeding Interval:",
        ["2-hourly", "3-hourly"],
        index=None,   # 👈 no default selection
        key="ft_interval"
    )

    # Feed ml/kg/day by day (default from day 4 onwards is 150 ml/kg/day)
    feed_dict = {1: 60, 2: 90, 3: 120}
    feed_ml_per_kg = feed_dict.get(day_of_life, 150) if day_of_life else None

    if st.button("Calculate Feeds", key="calc_feeds"):
        if weight_neonate is not None and day_of_life is not None and feed_interval is not None:
            total_feed = weight_neonate * feed_ml_per_kg
            feeds_per_day = 12 if feed_interval == "2-hourly" else 8
            feed_per_time = total_feed / feeds_per_day
            iv_fluids = weight_neonate * 100

            st.success(f"Total Feed Volume: {total_feed:.0f} ml/day")
            st.info(f"Feed Volume per Feed ({feed_interval}): {feed_per_time:.0f} ml")
            st.warning(f"IV Fluids Volume: {iv_fluids:.0f} ml/day")
        else:
            st.warning("⚠️ Please enter all inputs before calculating.")    