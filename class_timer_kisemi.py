import streamlit as st
import time
import random
from pathlib import Path

st.set_page_config(
    page_title="Classroom Timer"
)

st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 100px;
}
</style>
""",
    unsafe_allow_html=True,
)

if "running" not in st.session_state:
    st.session_state.running = False
if "end_ts" not in st.session_state:
    st.session_state.end_ts = None
if "remaining_sec" not in st.session_state:
    st.session_state.remaining_sec = 0
if "finished_shown" not in st.session_state:
    st.session_state.finished_shown = False

minutes = st.slider("select time (minutes)", min_value=1, max_value=90, value=10)
duration_sec = minutes * 60

start_col, pause_col, reset_col = st.columns(3)

if start_col.button("SStart"):
    # Start a fresh timer based on the currently selected duration.
    st.session_state.running = True
    st.session_state.end_ts = time.time() + duration_sec
    st.session_state.finished_shown = False

if pause_col.button("Pause") and st.session_state.running:
    st.session_state.remaining_sec = max(0, int(st.session_state.end_ts - time.time()))
    st.session_state.running = False
    st.session_state.end_ts = None

if reset_col.button("Reset"):
    st.session_state.running = False
    st.session_state.end_ts = None
    st.session_state.remaining_sec = 0
    st.session_state.finished_shown = False

if st.session_state.running:
    remaining = max(0, int(st.session_state.end_ts - time.time()))
else:
    remaining = st.session_state.remaining_sec

ph = st.empty()
mm, ss = remaining // 60, remaining % 60
ph.metric("Countdown", f"{mm:02d}:{ss:02d}")

if st.session_state.running and remaining == 0:
    st.session_state.running = False
    st.session_state.end_ts = None
    if not st.session_state.finished_shown:
        image_choices = ["happy.jpg", "thecat.jpg", "unsplash-cat.jpg"]
        existing_images = [name for name in image_choices if Path(name).exists()]
        if existing_images:
            st.image(random.choice(existing_images), caption="countdown finished")
        else:
            st.warning("Countdown finished (no image assets found).")
        st.session_state.finished_shown = True

if st.session_state.running:
    # Keep the app responsive while advancing the timer once per second.
    time.sleep(1)
    st.rerun()

