
import streamlit as st
import pandas as pd
import os

HISTORY_FILE = "rocketmoyo_history.csv"
def save_history(history):
    df = pd.DataFrame(history)
    df.to_csv(HISTORY_FILE, index=False)


if "player_history" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        saved_df = pd.read_csv(HISTORY_FILE)
        st.session_state.player_history = (
            saved_df.to_dict("records")
        )
    else:
        st.session_state.player_history = []

if "pending_match_record" not in st.session_state:
    st.session_state.pending_match_record = None

st.set_page_config(page_title="Manual Analysis", page_icon="⚾")

st.title("🇿🇼 ROCKETMOYO")
st.header("Manual Batting Analysis")

st.write("Enter a player's batting statistics.")


# Get player names from saved match history
existing_players = sorted({
    record["Player"]
    for record in st.session_state.player_history
    if record.get("Player")
})

with st.form("batting_form"):
    player_choice = st.selectbox(
        "Select an existing player or add a new one",
        ["New player"] + existing_players
    )

    if player_choice == "New player":
        player_name = st.text_input("Player name")
    else:
        player_name = player_choice

    team_name = st.text_input("Club or school")

    matches = st.number_input(
        "Matches played", min_value=1, value=1
    )
    at_bats = st.number_input(
        "At-bats", min_value=0, value=1
    )
    hits = st.number_input(
        "Hits", min_value=0, value=0
    )
    strikeouts = st.number_input(
        "Strikeouts", min_value=0, value=0
    )

    submitted = st.form_submit_button("Analyse Player")

if submitted:
    if not player_name.strip():
        st.error("Please enter the player's name.")
    elif hits > at_bats or strikeouts > at_bats:
        st.error("Hits and strikeouts cannot exceed at-bats.")
    else:
        average = hits / at_bats if at_bats > 0 else 0
        strikeout_rate = (
            strikeouts / at_bats * 100 if at_bats > 0 else 0
        )

        match_record = {
            "Player": player_name.strip(),
            "Club": team_name or "Not entered",
            "Matches": matches,
            "At-bats": at_bats,
            "Hits": hits,
            "Strikeouts": strikeouts,
            "Batting Average": round(average, 3),
            "Strikeout Rate (%)": round(strikeout_rate, 1)
        }

        st.session_state.pending_match_record = match_record

        st.subheader("Player Report")
        st.write("Player:", player_name)
        st.write("Club or school:", team_name or "Not entered")
        st.metric("Batting Average", f"{average:.3f}")
        st.metric("Strikeout Rate", f"{strikeout_rate:.1f}%")

        
    st.subheader("🔎 ROCKETMOYO Weakness Detective")

    if at_bats < 10:
        st.info(
            "Not enough data for a useful assessment yet. "
            "Record more at-bats across additional matches."
        )

    else:
        weaknesses_found = False

    # Check batting average
    if average < 0.200:
        weaknesses_found = True

        st.warning("Possible area to improve: Batting consistency")

        st.write("Recommended training:")
        st.write("- Practise hitting from a batting tee.")
        st.write("- Use soft toss to practise consistent contact.")
        st.write("- Ask a coach to observe your stance and swing.")

    # Check strikeout rate
    if strikeout_rate >= 30:
        weaknesses_found = True

        st.warning("Possible area to improve: Making contact")

        st.write("Recommended training:")
        st.write("- Practise tracking the ball with your eyes.")
        st.write("- Use controlled toss drills to improve timing.")
        st.write("- Practise swinging at hittable pitches.")
        st.write("- Ask a coach to review your pitch recognition.")

    # If no rule is triggered
    if not weaknesses_found:
        st.success(
            "No major concern flagged by these initial rules."
        )

        st.write(
            "Keep practising, track future matches, "
            "and review your progress with a coach."
        )

st.caption(
    "These are preliminary statistical indicators, not a diagnosis. "
    "The thresholds are starting rules, not universal standards."
)

# Save the result outside the submitted block
if st.session_state.pending_match_record is not None:
    st.subheader("📈 Save Match Result")

    
if st.button("Save Match Result"):
    record = st.session_state.pending_match_record

    if record is not None:
        st.session_state.player_history.append(record)

        save_history(st.session_state.player_history)

        st.session_state.pending_match_record = None
        st.success("Match result saved permanently!")



# Display history outside the submitted block

st.subheader("📊 Player Progress History")

if st.session_state.player_history:
    history_df = pd.DataFrame(
        st.session_state.player_history
    )

    existing_players = sorted(
        history_df["Player"].dropna().unique()
    )

    selected_player = st.selectbox(
        "Choose a player profile",
        existing_players
    )

    player_df = history_df[
        history_df["Player"] == selected_player
    ]

    st.dataframe(
        player_df,
        use_container_width=True
    )

    st.subheader("Batting Average Across Saved Matches")
    st.line_chart(player_df["Batting Average"])

else:
    st.info("No match results saved yet.")


# Compare the player's saved match results


st.subheader("📈 Performance Improvement")

if st.session_state.player_history:
    history_df = pd.DataFrame(
        st.session_state.player_history
    )

    if "selected_player" in locals():
        player_df = history_df[
            history_df["Player"] == selected_player
        ]

        if len(player_df) >= 2:
            first_average = player_df[
                "Batting Average"
            ].iloc[0]

            latest_average = player_df[
                "Batting Average"
            ].iloc[-1]

            change = latest_average - first_average

            percentage_change = (
                (change / first_average) * 100
                if first_average > 0 else None
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Starting Average",
                f"{first_average:.3f}"
            )

            col2.metric(
                "Latest Average",
                f"{latest_average:.3f}"
            )

            col3.metric(
                "Overall Improvement",
                f"{change:+.3f}"
            )

            if percentage_change is not None:
                st.metric(
                    "Percentage Change",
                    f"{percentage_change:+.1f}%"
                )
            else:
                st.info(
                    "Percentage change unavailable because "
                    "the starting average was zero."
                )

            if change > 0:
                st.success(
                    "Performance has improved since the first match!"
                )
            elif change < 0:
                st.warning(
                    "Performance has declined since the first match."
                )
            else:
                st.info(
                    "Performance is unchanged since the first match."
                )

        else:
            st.info(
                "Save at least two match results for this player."
            )
    else:
        st.info("Select a player profile to track progress.")

else:
    st.info("Save a match result to begin tracking progress.")
