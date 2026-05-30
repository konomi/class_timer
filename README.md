# class_timer

Simple Streamlit classroom countdown timer.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Main app:

```bash
streamlit run class_timer.py
```

Alternative variant:

```bash
streamlit run class_timer_kisemi.py
```

Windows helper:

```bat
.\go.bat
```

## Behavior

- Choose the countdown duration with the minutes slider.
- `Start` begins the timer from the selected duration.
- `Pause` stops and keeps the remaining time.
- `Reset` clears state and sets remaining time to `00:00`.
- When the countdown reaches zero, the app displays a random completion image.

## Image Assets

Place these files at the repository root:

- `happy.jpg`
- `thecat.jpg`
- `unsplash-cat.jpg`

If none of the images exist, the app shows a text warning instead.


