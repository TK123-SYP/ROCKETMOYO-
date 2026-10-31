import streamlit as st
from datetime import date
import pandas as pd
from pybaseball import statcast



st.set_page_config(
    page_title="ROCKETMOYO",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 ROCKETMOYO")
st.subheader("⚾ MLB Batting Analytics")

st.write(
    "Explore how exit velocity and launch angle "
    "relate to baseball batting outcomes."
)

st.divider()
st.header("📅 Select Your Analysis Period")

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start date",
        value=date(2024, 4, 1)
    )

with col2:
    end_date = st.date_input(
        "End date",
        value=date(2024, 4, 30)
    )

if start_date > end_date:
    st.error("The start date must be before the end date.")

elif st.button("⚾ Load MLB Statcast Data"):
    try:
        with st.spinner("Fetching MLB data. Please wait..."):
            data = statcast(
                start_dt=str(start_date),
                end_dt=str(end_date)
            )

        if data is None or data.empty:
            st.warning(
                "No data returned. Try a different date range."
            )
        else:
            st.success(f"Loaded {len(data):,} Statcast pitches!")

            st.write("### Data Preview")
            st.dataframe(data.head(20), use_container_width=True)

            st.write("### Available batting metrics")
            metrics = [
                col for col in
                ["release_speed", "launch_speed", "launch_angle",
                 "events", "player_name"]
                if col in data.columns
            ]
            st.write(", ".join(metrics))

            csv = data.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Statcast CSV",
                data=csv,
                file_name="rocketmoyo_statcast.csv",
                mime="text/csv"
            )

    except Exception as error:
        st.error(
            "Could not load Statcast data. Check your internet "
            "connection and try again."
        )
        st.caption(f"Technical details: {error}")

##manual analysis
manual_page = st.Page(
    "pages/1_Manual_Analysis.py",
    title="Manual Player Analysis",
    icon="⚾"
)


#launch angle vs exit velocity
st.divider()
st.header("📂 Analyze Downloaded Statcast Data")

uploaded_file = st.file_uploader(
    "Choose your Statcast CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.success(f"Loaded {len(data):,} rows.")

    st.subheader("Missing Values")
    missing = data.isna().sum()

    missing_summary = pd.DataFrame({
        "Column": missing.index,
        "Missing values": missing.values,
        "Missing (%)": (
            missing.values / len(data) * 100
        ).round(2)
    })

    st.dataframe(
        missing_summary,
        use_container_width=True
    )

    st.subheader("Data Preview")
    st.dataframe(data.head(10), use_container_width=True)

st.divider()
st.header("⚾ Exit Velocity vs Launch Angle")

if uploaded_file is not None:
    chart_data = data.dropna(
        subset=["launch_speed", "launch_angle"]
    ).copy()

    if chart_data.empty:
        st.warning(
            "No rows contain both exit velocity and launch angle."
        )
    else:
        st.write(
            f"Using {len(chart_data):,} rows with both metrics."
        )

        st.scatter_chart(
            chart_data,
            x="launch_angle",
            y="launch_speed",
            x_label="Launch Angle (degrees)",
            y_label="Exit Velocity (mph)"
        )
#batting outcome summary

st.divider()
st.header("📊 Batting Outcome Summary")

if uploaded_file is not None:
    if "events" in data.columns:
        outcomes = (
            data["events"]
            .dropna()
            .value_counts()
            .reset_index()
        )

        outcomes.columns = ["Outcome", "Count"]

        st.dataframe(
            outcomes,
            use_container_width=True
        )

        st.bar_chart(
            outcomes,
            x="Outcome",
            y="Count"
        )
    else:
        st.warning(
            "The CSV does not contain an 'events' column."
        )
#hard hit analysis

st.divider()
st.header("💥 Hard-Hit Analysis")

if uploaded_file is not None:
    if "launch_speed" in data.columns:
        exit_velo = pd.to_numeric(
            data["launch_speed"],
            errors="coerce"
        ).dropna()

        if len(exit_velo) > 0:
            hard_hits = (exit_velo >= 95).sum()
            hard_hit_rate = hard_hits / len(exit_velo) * 100

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Balls with Exit Velocity",
                f"{len(exit_velo):,}"
            )

            col2.metric(
                "Hard-Hit Balls",
                f"{hard_hits:,}"
            )

            col3.metric(
                "Hard-Hit Rate",
                f"{hard_hit_rate:.1f}%"
            )
        else:
            st.warning("No valid exit-velocity values found.")
    else:
        st.warning("The CSV has no launch_speed column.")






        