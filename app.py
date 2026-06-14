import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="wide")

# Theme selection (sidebar)
theme_choice = st.sidebar.radio("Theme", ["Dark", "Light"], index=0)
show_dev = st.sidebar.checkbox("Show developer debug info", value=False)

# Color palettes for themes
if theme_choice == "Dark":
    BG = "#0b1020"
    SURFACE = "#0f1724"
    CARD = "#0f172a"
    TEXT = "#e6eef8"
    MUTED = "#94a3b8"
    ACCENT_A = "#7c3aed"
    ACCENT_B = "#06b6d4"
else:
    BG = "#f6f8ff"
    SURFACE = "#ffffff"
    CARD = "#ffffff"
    TEXT = "#0f172a"
    MUTED = "#475569"
    ACCENT_A = "#6366f1"
    ACCENT_B = "#06b6d4"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html, body, .stApp {{ font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; background: {BG}; color: {TEXT}; }}
.stApp {{ min-height: 100vh; }}
.block-container {{ padding-top: 0rem; padding-right: 2rem; padding-left: 2rem; padding-bottom: 2rem; }}
.game-container {{ max-width:960px; margin:28px auto; padding:0; }}
.game-header {{ display:flex; align-items:center; justify-content:space-between; gap:18px; }}
.hero {{ background: rgba(255,255,255,0.04); border-radius:14px; padding:22px; box-shadow: 0 14px 40px rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.08); }}
.title {{ font-size:24px; font-weight:600; margin:0; color:{TEXT}; }}
.tagline {{ color:{MUTED}; margin-top:6px; font-weight:300; }}
.summary-card {{ border-radius:12px; padding:18px; background: rgba(255,255,255,0.05); box-shadow:0 12px 28px rgba(0,0,0,0.24); margin-bottom:16px; color:{TEXT}; }}
.stButton>button {{ background: linear-gradient(90deg,{ACCENT_A},{ACCENT_B}); color:#fff; border:none; padding:12px 16px; border-radius:12px; box-shadow: 0 8px 24px rgba(12,18,33,0.12); }}
.stButton>button:hover {{ transform: translateY(-1px); }}
.stTextInput>div>input {{ border-radius:12px; padding:14px; border:1px solid rgba(255,255,255,0.14); background: rgba(255,255,255,0.05); color:{TEXT}; }}
.stTextInput>div>label {{ color:{TEXT}; }}
.stTextInput>div>div>span {{ color:{MUTED}; }}
.stMetric {{ color:{TEXT}; }}
.stMetric>div>div:first-child {{ color:{TEXT}; }}
.metrics-card {{ background: rgba(255,255,255,0.05); border-radius:12px; padding:16px; box-shadow:0 10px 24px rgba(0,0,0,0.22); color:{TEXT}; }}
.stSidebar {{ background: {SURFACE}; color:{TEXT}; border-right:1px solid rgba(255,255,255,0.08); }}
.stSidebar .css-1d391kg {{ color:{TEXT}; }}
.stSelectbox>div>div>div>div {{ background: {SURFACE}; color:{TEXT}; }}
.stCheckbox>div>label {{ color:{TEXT}; }}
footer, .css-16huue1 {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


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

st.markdown("""
<div class="game-container">
    <div class="game-header hero">
        <div>
            <h1 class="title">Game Glitch Investigator</h1>
            <div class="tagline">A refined number-guessing challenge with clear feedback.</div>
        </div>
        <div style="text-align:right; min-width:140px;">
            <div style="font-size:12px; color:var(--muted); margin-top:6px;">Focused. Minimal. Playful in spirit.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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

if show_dev:
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
    submit = st.form_submit_button("Submit")

col1, col2, col3 = st.columns(3)
with col1:
    new_game = st.button("New Game")
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
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
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
