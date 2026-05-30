# Copilot Instructions

## Commands

| Task | Command |
| --- | --- |
| Install dependencies | `pip install -r requirements.txt` |
| Run the app | `streamlit run class_timer.py` |
| Run the app via helper script | `.\go.bat` |

There are no dedicated test, single-test, build, or lint commands configured in this repository.

## High-level architecture

This repository is a small Streamlit application centered on a single executable script, `class_timer.py`.

- `class_timer.py` is the main app entry point. It defines the UI, countdown behavior, inline CSS, and the end-of-timer image selection in one file.
- `go.bat` is the Windows launch helper and should stay aligned with the main entry point.
- `class_timer_kisemi.py` is an alternate variant of the app, not the script launched by `go.bat`.
- Image assets (`happy.jpg`, `thecat.jpg`, `unsplash-cat.jpg`) are loaded by relative filename from the repository root when the countdown finishes.

Because this is a Streamlit app, the script executes top-to-bottom on each interaction. UI elements and countdown logic are not separated into modules or helper functions, so changes to timing, widget behavior, or asset selection usually happen directly in `class_timer.py`.

## Key conventions

- Treat `class_timer.py` as the source of truth for the shipped app; do not assume `class_timer_kisemi.py` is kept in sync.
- Keep asset references as repository-root relative filenames unless the app is refactored to use a dedicated asset path.
- The large timer display is implemented with inline CSS targeting Streamlit's metric test ID, and the countdown display is updated through a single `st.empty()` placeholder plus `metric()`.
- The current countdown behavior is a blocking `for` loop with `time.sleep(1)`, so edits that add controls or new UI state must account for Streamlit reruns and the synchronous loop structure.
