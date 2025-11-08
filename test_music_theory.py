#!/usr/bin/env python3
"""
Simple test script to verify music theory calculations.
Run this to test the core logic without needing a MIDI device.
"""

from piano_practice.music_theory import (
    midi_to_note_name,
    calculate_interval,
    notes_match,
    get_random_note,
    get_random_interval,
    generate_scale,
    get_random_mode,
    get_mode_names,
)


def test_midi_to_note():
    """Test MIDI number to note name conversion."""
    print("Testing MIDI to Note conversion...")

    tests = [
        (60, 'C'),   # Middle C
        (61, 'C#'),
        (62, 'D'),
        (69, 'A'),   # A440
        (72, 'C'),   # C one octave up (should still be 'C')
    ]

    for midi_num, expected in tests:
        result = midi_to_note_name(midi_num)
        status = "✓" if result == expected else "✗"
        print(f"  {status} MIDI {midi_num} -> {result} (expected {expected})")


def test_intervals():
    """Test interval calculations."""
    print("\nTesting interval calculations...")

    tests = [
        ('C', '1', 'C'),
        ('C', '3', 'E'),
        ('C', '5', 'G'),
        ('C', 'b7', 'A#'),
        ('D', '3', 'F#'),
        ('D', 'b3', 'F'),
        ('G', '5', 'D'),
        ('A', 'b6', 'F'),
    ]

    for root, interval, expected in tests:
        result = calculate_interval(root, interval)
        # Use notes_match to handle enharmonic equivalents
        status = "✓" if notes_match(result, expected) else "✗"
        print(f"  {status} {root} + {interval} = {result} (expected {expected})")


def test_note_matching():
    """Test enharmonic equivalent matching."""
    print("\nTesting enharmonic matching...")

    tests = [
        ('C#', 'Db', True),
        ('D#', 'Eb', True),
        ('C', 'C', True),
        ('C', 'D', False),
        ('F#', 'Gb', True),
    ]

    for note1, note2, expected in tests:
        result = notes_match(note1, note2)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{note1}' == '{note2}': {result} (expected {expected})")


def test_random_functions():
    """Test random generation functions."""
    print("\nTesting random generation...")

    # Test random note generation
    notes = [get_random_note() for _ in range(5)]
    print(f"  Random notes: {', '.join(notes)}")

    # Test random interval generation
    intervals = [get_random_interval() for _ in range(5)]
    print(f"  Random intervals: {', '.join(intervals)}")


def test_modes():
    """Test mode generation."""
    print("\nTesting mode generation...")

    # Get all mode names
    modes = get_mode_names()
    print(f"  Available modes: {', '.join(modes)}")

    # Test specific mode scales
    tests = [
        ('C', 'Ionian', ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']),
        ('C', 'Aeolian', ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#', 'C']),
        ('D', 'Dorian', ['D', 'E', 'F', 'G', 'A', 'B', 'C', 'D']),
        ('G', 'Mixolydian', ['G', 'A', 'B', 'C', 'D', 'E', 'F', 'G']),
    ]

    for root, mode, expected in tests:
        result = generate_scale(root, mode)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {mode} in {root}: {' - '.join(result)}")
        if result != expected:
            print(f"     Expected: {' - '.join(expected)}")


def test_random_modes():
    """Test random mode generation."""
    print("\nTesting random mode generation...")

    # Generate random modes
    for _ in range(3):
        mode = get_random_mode()
        key = get_random_note()
        scale = generate_scale(key, mode)
        print(f"  {mode} in {key}: {' - '.join(scale)}")


if __name__ == "__main__":
    print("="*50)
    print("Piano Practice App - Music Theory Tests")
    print("="*50 + "\n")

    test_midi_to_note()
    test_intervals()
    test_note_matching()
    test_random_functions()
    test_modes()
    test_random_modes()

    print("\n" + "="*50)
    print("Tests complete!")
    print("="*50)
