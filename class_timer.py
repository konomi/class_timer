import streamlit as st
import time

st.set_page_config(
    page_title="Classrooom Timer"
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

min = st.slider('select time (minutes)', max_value=30)

ph = st.empty()
N = min * 60
for secs in range(N,0,-1):
    mm, ss = secs//60, secs%60
    ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
    time.sleep(1)
