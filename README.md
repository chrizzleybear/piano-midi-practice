# Piano Practice App

A command-line MIDI practice tool that helps you master scale degrees and modes on a MIDI keyboard with real-time feedback.

## Features

- **MIDI Input Detection**: Auto-detects and connects to available MIDI devices
- **Note Recognition**: Converts MIDI input to note names (ignoring octave)
- **Two Practice Modes**:
  - **Scale Degree Practice**: Random intervals from a root note
  - **Mode/Scale Practice**: Play complete modes ascending and descending
- **Adjustable Time Pressure**: Choose your difficulty level (None, Low, Medium, Hard)
- **Real-time Feedback**: Color-coded correct/incorrect responses
- **Session Statistics**: Track your accuracy and progress
- **Timeout Hints**: Helpful hints if you take too long

## Requirements

- Python 3.8 or higher
- MIDI keyboard connected to your computer
- Required Python packages (see Installation)

## Installation

1. Clone or download this repository

2. Run the setup script (recommended):
```bash
./setup.sh
```

Or manually create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment (if not already active):
```bash
source venv/bin/activate
```

2. Run the application:
```bash
python -m piano_practice.main
```

3. When done, deactivate the virtual environment:
```bash
deactivate
```

### How it Works

1. The app connects to your MIDI keyboard
2. Select a practice mode:
   - **Mode 1 - Scale Degree Practice**:
     - Random root note is displayed (e.g., "D")
     - Play the root note
     - App prompts scale degrees (e.g., "Play the 3", "Play the b7")
     - After 5-7 prompts, new root note is selected
   - **Mode 2 - Mode/Scale Practice**:
     - Random mode and key are displayed (e.g., "Dorian in F#")
     - Complete scale is shown
     - Play the scale ascending (8 notes)
     - Play the scale descending (8 notes)
     - New mode/key is selected
3. Select time pressure level:
   - **None**: No time limit
   - **Low**: 15 seconds per note/sequence
   - **Medium**: 10 seconds per note/sequence
   - **Hard**: 5 seconds per note/sequence
4. Press Ctrl+C to exit and view your statistics

### Supported Intervals (Scale Degree Mode)

- **Major scale degrees**: 1, 2, 3, 4, 5, 6, 7
- **Flat alterations**: b2, b3, b5, b6, b7
- **Sharp alterations**: #4, #5

### Supported Modes (Mode Practice)

- **Ionian** (Major scale): W-W-H-W-W-W-H
- **Dorian**: W-H-W-W-W-H-W
- **Phrygian**: H-W-W-W-H-W-W
- **Lydian**: W-W-W-H-W-W-H
- **Mixolydian**: W-W-H-W-W-H-W
- **Aeolian** (Natural Minor): W-H-W-W-H-W-W
- **Locrian**: H-W-W-H-W-W-W

(W = Whole step, H = Half step)

### Feedback System

- ✓ **Green** = Correct answer
- ✗ **Red** = Wrong note (shows what you played)
- ⏱ **Yellow** = Timeout hint (shows expected note)

## Project Structure

```
piano_practice_app/
├── piano_practice/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── midi_handler.py      # MIDI device connection
│   ├── music_theory.py      # Note/interval calculations
│   └── practice_modes.py    # Practice logic
├── requirements.txt
├── setup.sh                 # Setup script
├── test_music_theory.py     # Test without MIDI
└── README.md
```

## Troubleshooting

**No MIDI device found:**
- Ensure your MIDI keyboard is connected via USB
- Check that no other application is using the MIDI device
- On macOS, you may need to grant microphone/input permissions

**Installation issues:**
- Make sure you have Python 3.8+ installed
- Use a virtual environment to avoid conflicts between Python versions
- If you see "externally-managed-environment" error, run `./setup.sh` instead
- Try installing packages one at a time if bulk install fails

**Notes not registering:**
- Check that your keyboard is sending MIDI data
- Try a different USB port
- Verify the keyboard is not in a special mode

## Future Enhancements

Planned features for future versions:
- Chord recognition practice mode
- Difficulty levels (limit interval types or modes)
- Custom interval/mode selection
- Session history and progress tracking
- Configuration file for user preferences
- Melodic/harmonic minor scales
- Ear training mode (app plays note, you identify it)

## License

This project is open source and available for educational purposes.
