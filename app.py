import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

# Small UI polish: background gradient and header style to feel less "AI-generated"
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg,#f8f9fa,#eef2ff); }
    .header { font-weight:700; letter-spacing:0.5px; }
    .summary-card { border-radius:16px; padding:16px; background:rgba(255,255,255,0.92); box-shadow:0 14px 28px rgba(0,0,0,0.08); margin-bottom:16px; }
    .summary-card strong { color:#0f172a; }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_session_summary(history):
    if not history:
        return
    st.markdown("### Session Summary")
    try:
        import pandas as _pd
        df = _pd.DataFrame(history, columns=["Guess", "Outcome"])
        st.table(df)
    except Exception:
        st.write(history)

st.title("🎮 Game Glitch Investigator", anchor=False)
st.markdown("<div class='header'>A playful, modern UI for the Number Guessing Game.</div>", unsafe_allow_html=True)

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# Top-line metrics for a cleaner UI
metrics_col1, metrics_col2 = st.columns(2)
metrics_col1.metric("Attempts Left", attempt_limit - st.session_state.attempts)
metrics_col2.metric("Score", st.session_state.score)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2, col3 = st.columns(3)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append((raw_guess, "Invalid"))
        st.error(err)
    else:
        st.session_state.history.append((guess_int, None))

        secret = st.session_state.secret
        outcome, message = check_guess(guess_int, secret)

        # update the last history entry with the outcome
        st.session_state.history[-1] = (guess_int, outcome)

        # Color-coded, user-friendly hint output
        if show_hint:
            if outcome == "Win":
                st.success(message)
            elif outcome == "Too High":
                st.error(message)
            else:
                st.info(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

        if st.session_state.history:
            st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
            st.markdown(f"**Last guess:** {raw_guess}")
            if ok:
                st.markdown(f"**Outcome:** {outcome}")
            st.markdown(f"**Attempt:** {st.session_state.attempts}/{attempt_limit}")
            st.markdown("</div>", unsafe_allow_html=True)

            render_session_summary(st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
