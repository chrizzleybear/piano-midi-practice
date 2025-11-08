"""
Music theory utilities for note conversion and interval calculations.
"""

import random
from typing import Optional, List, Tuple


# Chromatic scale starting from C
CHROMATIC_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Alternative flat notation
FLAT_NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# Enharmonic equivalents mapping
ENHARMONIC_MAP = {
    'C#': 'Db', 'Db': 'C#',
    'D#': 'Eb', 'Eb': 'D#',
    'F#': 'Gb', 'Gb': 'F#',
    'G#': 'Ab', 'Ab': 'G#',
    'A#': 'Bb', 'Bb': 'A#',
}

# Scale degree intervals (in semitones from root)
INTERVALS = {
    '1': 0,
    'b2': 1,
    '2': 2,
    'b3': 3,
    '3': 4,
    '4': 5,
    '#4': 6,
    'b5': 6,
    '5': 7,
    '#5': 8,
    'b6': 8,
    '6': 9,
    'b7': 10,
    '7': 11,
}

# Mode definitions (interval patterns in semitones)
# Each mode is defined by the pattern of intervals from the root
MODES = {
    'Ionian': [0, 2, 4, 5, 7, 9, 11, 12],        # W-W-H-W-W-W-H (Major scale)
    'Dorian': [0, 2, 3, 5, 7, 9, 10, 12],        # W-H-W-W-W-H-W
    'Phrygian': [0, 1, 3, 5, 7, 8, 10, 12],      # H-W-W-W-H-W-W
    'Lydian': [0, 2, 4, 6, 7, 9, 11, 12],        # W-W-W-H-W-W-H
    'Mixolydian': [0, 2, 4, 5, 7, 9, 10, 12],    # W-W-H-W-W-H-W
    'Aeolian': [0, 2, 3, 5, 7, 8, 10, 12],       # W-H-W-W-H-W-W (Natural minor)
    'Locrian': [0, 1, 3, 5, 6, 8, 10, 12],       # H-W-W-H-W-W-W
}


def midi_to_note_name(midi_num: int) -> str:
    """
    Convert MIDI note number (0-127) to note name, ignoring octave.

    Args:
        midi_num: MIDI note number (0-127)

    Returns:
        Note name (e.g., 'C', 'C#', 'D', etc.)
    """
    note_index = midi_num % 12
    return CHROMATIC_NOTES[note_index]


def note_name_to_index(note_name: str) -> Optional[int]:
    """
    Convert note name to chromatic index (0-11).
    Handles both sharp and flat notation.

    Args:
        note_name: Note name (e.g., 'C', 'C#', 'Db')

    Returns:
        Index in chromatic scale (0-11) or None if invalid
    """
    if note_name in CHROMATIC_NOTES:
        return CHROMATIC_NOTES.index(note_name)
    elif note_name in FLAT_NOTES:
        return FLAT_NOTES.index(note_name)
    return None


def calculate_interval(root_note: str, interval: str) -> str:
    """
    Calculate the note that is a given interval away from the root.

    Args:
        root_note: Starting note (e.g., 'D', 'F#')
        interval: Scale degree (e.g., '3', 'b7', '#4')

    Returns:
        Resulting note name

    Raises:
        ValueError: If interval is not supported
    """
    if interval not in INTERVALS:
        raise ValueError(f"Unsupported interval: {interval}")

    root_index = note_name_to_index(root_note)
    if root_index is None:
        raise ValueError(f"Invalid root note: {root_note}")

    semitones = INTERVALS[interval]
    result_index = (root_index + semitones) % 12

    # Prefer sharps for sharp roots, flats for flat roots
    if 'b' in root_note:
        return FLAT_NOTES[result_index]
    else:
        return CHROMATIC_NOTES[result_index]


def get_random_note() -> str:
    """
    Get a random note to use as a root note.
    Includes both natural notes and accidentals.

    Returns:
        Random note name
    """
    return random.choice(CHROMATIC_NOTES)


def get_random_interval() -> str:
    """
    Get a random scale degree interval for practice.
    Excludes '1' (root) to make it more challenging.

    Returns:
        Random interval string (e.g., '3', 'b7', '#4')
    """
    intervals = [k for k in INTERVALS.keys() if k != '1']
    return random.choice(intervals)


def notes_match(note1: str, note2: str) -> bool:
    """
    Check if two notes are the same, accounting for enharmonic equivalents.

    Args:
        note1: First note name
        note2: Second note name

    Returns:
        True if notes are equivalent, False otherwise
    """
    if note1 == note2:
        return True

    # Check enharmonic equivalents
    if note1 in ENHARMONIC_MAP and ENHARMONIC_MAP[note1] == note2:
        return True

    return False


def format_interval_prompt(interval: str) -> str:
    """
    Format an interval for display in prompts.

    Args:
        interval: Interval string (e.g., '3', 'b7')

    Returns:
        Formatted string (e.g., "the 3", "the b7")
    """
    return f"the {interval}"


def generate_scale(root_note: str, mode: str) -> List[str]:
    """
    Generate a scale from a root note and mode.

    Args:
        root_note: Starting note (e.g., 'C', 'F#', 'Bb')
        mode: Mode name (e.g., 'Ionian', 'Dorian')

    Returns:
        List of note names in the scale (including octave)

    Raises:
        ValueError: If mode is not supported
    """
    if mode not in MODES:
        raise ValueError(f"Unsupported mode: {mode}. Available: {list(MODES.keys())}")

    root_index = note_name_to_index(root_note)
    if root_index is None:
        raise ValueError(f"Invalid root note: {root_note}")

    intervals = MODES[mode]
    scale = []

    # Prefer sharps for sharp roots, flats for flat roots
    use_flats = 'b' in root_note

    for interval in intervals:
        note_index = (root_index + interval) % 12
        if use_flats:
            scale.append(FLAT_NOTES[note_index])
        else:
            scale.append(CHROMATIC_NOTES[note_index])

    return scale


def get_random_mode() -> str:
    """
    Get a random mode for practice.

    Returns:
        Random mode name (e.g., 'Ionian', 'Dorian')
    """
    return random.choice(list(MODES.keys()))


def get_mode_names() -> List[str]:
    """
    Get list of all available mode names.

    Returns:
        List of mode names
    """
    return list(MODES.keys())
