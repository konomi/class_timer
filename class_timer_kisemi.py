import math
import base64
import io
import struct
import time
import wave

import streamlit as st


DURATION_SEC = 2 * 60


def make_chime_wav_data_uri(repeats=1, gap_sec=0.25):
    sample_rate = 44100
    duration_sec = 0.9
    frames = []
    total_samples = int(sample_rate * duration_sec)
    gap_samples = int(sample_rate * gap_sec)

    for repeat_index in range(repeats):
        for i in range(total_samples):
            t = i / sample_rate
            fade = math.exp(-4.5 * t)
            tone = (
                0.55 * math.sin(2 * math.pi * 880 * t)
                + 0.35 * math.sin(2 * math.pi * 1320 * t)
            )
            sample = int(max(-1, min(1, tone * fade)) * 32767)
            frames.append(struct.pack("<h", sample))

        if repeat_index < repeats - 1:
            frames.extend(struct.pack("<h", 0) for _ in range(gap_samples))

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"".join(frames))

    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:audio/wav;base64,{encoded}"


CHIME_DATA_URI = make_chime_wav_data_uri()
DOUBLE_CHIME_DATA_URI = make_chime_wav_data_uri(repeats=2)

st.set_page_config(
    page_title="Classroom Timer 2"
)

st.markdown(
    """
<style>
.timer-row {
    display: flex;
    align-items: baseline;
    gap: 2rem;
    margin: 1.5rem 0;
}
.timer-text {
    font-size: 100px;
    font-weight: 700;
    line-height: 1;
}
.count-text {
    color: blue;
    font-size: 80px;
    font-weight: 700;
    line-height: 1;
}
.phase-text {
    font-size: 28px;
    font-weight: 600;
    margin-top: -0.75rem;
}
</style>
""",
    unsafe_allow_html=True,
)

audio_slot = st.empty()

if "running" not in st.session_state:
    st.session_state.running = False
if "end_ts" not in st.session_state:
    st.session_state.end_ts = None
if "remaining_sec" not in st.session_state:
    st.session_state.remaining_sec = DURATION_SEC
if "complete_count" not in st.session_state:
    st.session_state.complete_count = 1
if "minute_sound_played" not in st.session_state:
    st.session_state.minute_sound_played = False
if "last_remaining_sec" not in st.session_state:
    st.session_state.last_remaining_sec = DURATION_SEC

start_col, pause_col, reset_col = st.columns(3)

if start_col.button("Start", key="start_button"):
    remaining = st.session_state.remaining_sec
    if remaining <= 0:
        remaining = DURATION_SEC
        st.session_state.minute_sound_played = False
        st.session_state.last_remaining_sec = DURATION_SEC
    st.session_state.running = True
    st.session_state.end_ts = time.time() + remaining

if pause_col.button("Pause", key="pause_button") and st.session_state.running:
    st.session_state.remaining_sec = max(0, math.ceil(st.session_state.end_ts - time.time()))
    st.session_state.running = False
    st.session_state.end_ts = None

if reset_col.button("Reset", key="reset_button"):
    st.session_state.running = False
    st.session_state.end_ts = None
    st.session_state.remaining_sec = DURATION_SEC
    st.session_state.minute_sound_played = False
    st.session_state.last_remaining_sec = DURATION_SEC

if st.session_state.running:
    remaining_sec = max(0, math.ceil(st.session_state.end_ts - time.time()))
else:
    remaining_sec = st.session_state.remaining_sec

play_finish_chime = False

if st.session_state.running and remaining_sec == 0:
    st.session_state.complete_count += 1
    st.session_state.minute_sound_played = False
    st.session_state.last_remaining_sec = DURATION_SEC
    st.session_state.end_ts = time.time() + DURATION_SEC
    st.session_state.remaining_sec = DURATION_SEC
    remaining_sec = DURATION_SEC
    play_finish_chime = True

timer_color = "green" if 0 < remaining_sec <= 60 else "black"
phase_color = "green" if 0 < remaining_sec <= 60 else "black"
phase_text = "\u3082\u306e\u307e\u306d\u30bf\u30a4\u30e0" if 0 < remaining_sec <= 60 else "\u81ea\u5df1\u7d39\u4ecb\u30bf\u30a4\u30e0"
mm, ss = remaining_sec // 60, remaining_sec % 60

if (
    st.session_state.running
    and not st.session_state.minute_sound_played
    and st.session_state.last_remaining_sec > 60
    and remaining_sec <= 60
):
    st.session_state.minute_sound_played = True
    audio_slot.markdown(
        f'<audio src="{CHIME_DATA_URI}" autoplay></audio>',
        unsafe_allow_html=True,
    )

if play_finish_chime:
    audio_slot.markdown(
        f'<audio src="{DOUBLE_CHIME_DATA_URI}" autoplay></audio>',
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
<div class="timer-row">
    <div class="timer-text" style="color: {timer_color};">{mm:02d}:{ss:02d}</div>
    <div class="count-text">{st.session_state.complete_count}</div>
</div>
<div class="phase-text" style="color: {phase_color};">{phase_text}</div>
""",
    unsafe_allow_html=True,
)

plus_col, minus_col, one_col = st.columns(3)

if plus_col.button("+1", key="plus_one_button"):
    st.session_state.complete_count += 1
    st.rerun()

if minus_col.button("-1", key="minus_one_button"):
    st.session_state.complete_count = max(0, st.session_state.complete_count - 1)
    st.rerun()

if one_col.button("=1", key="reset_count_to_one_button"):
    st.session_state.complete_count = 1
    st.rerun()

if st.session_state.running:
    st.session_state.remaining_sec = remaining_sec
    st.session_state.last_remaining_sec = remaining_sec
    time.sleep(1)
    st.rerun()
