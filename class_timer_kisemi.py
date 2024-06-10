import streamlit as st
import time
import random

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

st.radio("test", ("1","2","3","4","5"), horizontal=True)
min = st.slider('select time (minutes)', max_value=90)

ph = st.empty()
N = min * 60
for secs in range(N,-1,-1):
    mm, ss = secs//60, secs%60
    ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
    time.sleep(1)
    if N > 0 and secs == 0:
        image_num = random.randint(1,2)
        if image_num == 1:
            image_name = 'happy.jpg'
        elif image_num == 2:
            image_name = 'thecat.jpg'
        st.image(image_name, caption='countdown finished')

