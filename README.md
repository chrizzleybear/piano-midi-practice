# Piano Practice App

A command-line MIDI practice tool that helps you master scale degrees and modes on a MIDI keyboard with real-time feedback.

## Features

- **MIDI Input Detection**: Auto-detects and connects to available MIDI devices
- **Note Recognition**: Converts MIDI input to note names (ignoring octave)
- **Two Practice Modes**:
  - **Scale Degree Practice**: Random intervals from a root note
  - **Mode/Scale Practice**: Play complete modes ascending and descending
- **Interactive Menus**: Navigate with arrow keys, use Space to toggle checkboxes, Enter to confirm
- **Customizable Mode Selection**: Choose which modes to practice (default: Major and Minor)
- **Adjustable Time Pressure**: Choose your difficulty level (None, Low, Medium, Hard)
- **Smart Feedback System**:
  - Shows note numbers during play (1-8)
  - Play through mistakes without interruption
  - Get complete error summary at the end of each round
  - Escape signal to end early (play octave interval)
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

### Testing the Interactive Menus

You can test the arrow key navigation without a MIDI keyboard:
```bash
python test_menus.py
```

This will show you how the interactive menus work.

### Example Mode Practice Session

```
Mode: Dorian | Key: D
Scale: D - E - F - G - A - B - C - D

Play ASCENDING:
  Expected: D → E → F → G → A → B → C → D
  Playing (1-8)... 1 2 3 4 5 6 7 8
  ✓ Ascending scale correct!

Play DESCENDING:
  Expected: D → C → B → A → G → F → E → D
  Playing (1-8)... 1 2 3 4 5 6 7 8
  ✗ Descending scale had errors:
    Note 3: Expected B, played Bb
    Note 5: Expected G, played F#
```

**Using the escape signal:**
If you make a mistake early and want to end the round immediately, play two notes an octave apart at the same time (e.g., C3 + C4 together).

### How it Works

1. The app connects to your MIDI keyboard
2. Select a practice mode (use ↑↓ arrow keys, press Enter to select):
   - **Scale Degree Practice**:
     - Random root note is displayed (e.g., "D")
     - Play the root note
     - App prompts scale degrees (e.g., "Play the 3", "Play the b7")
     - After 5-7 prompts, new root note is selected
   - **Mode/Scale Practice**:
     - Select which modes to practice (Space to toggle, Enter to confirm)
     - Default: Ionian (Major) and Aeolian (Minor) ✓
     - Can add: Dorian, Phrygian, Lydian, Mixolydian, Locrian
     - Random mode and key are displayed (e.g., "Dorian in F#")
     - Complete scale is shown
     - Play the scale ascending (8 notes)
       - App shows note numbers (1 2 3...) as you play
       - Continue playing even if you make mistakes
       - Feedback shown only after 8th note or escape signal
       - Escape signal: Play two notes an octave apart simultaneously to end early
     - Play the scale descending (8 notes, same rules)
     - Feedback shows all errors at once with note positions
     - New mode/key is selected
3. Select time pressure level (use ↑↓ arrow keys, press Enter):
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

**Scale Degree Practice:**
- ✓ **Green** = Correct answer
- ✗ **Red** = Wrong note (shows what you played)
- ⏱ **Yellow** = Timeout hint (shows expected note)

**Mode/Scale Practice:**
- **During play**: Shows note numbers (1 2 3 4 5 6 7 8)
- **After each round**: Shows complete error summary
  - ✓ **Green** = All 8 notes correct
  - ✗ **Red** = Lists each error with position and notes
  - Example: "Note 3: Expected E, played F"
- **Escape signal**: Play two notes an octave apart to end early and see results

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
- If you already installed dependencies before, run `pip install -r requirements.txt` again to get the interactive menu support
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
