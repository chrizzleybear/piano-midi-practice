#!/usr/bin/env python3
"""
Test script to demonstrate the interactive menus.
Run this to test menu navigation without needing a MIDI device.
"""

import sys
import questionary

def test_practice_mode_menu():
    """Test the practice mode selection menu."""
    print("="*50)
    print("Testing Practice Mode Selection")
    print("="*50)
    print("\nUse ↑↓ arrow keys to navigate, Enter to select\n")

    choice = questionary.select(
        "Select Practice Mode:",
        choices=[
            questionary.Choice(
                title="Scale Degree Practice - Random intervals from a root note",
                value=1
            ),
            questionary.Choice(
                title="Mode/Scale Practice - Play complete modes ascending and descending",
                value=2
            ),
            questionary.Choice(
                title="Quit",
                value=0
            ),
        ],
        style=questionary.Style([
            ('selected', 'fg:#00ff00 bold'),  # Green for selected
            ('pointer', 'fg:#00ff00 bold'),   # Green arrow
            ('highlighted', 'fg:#00ff00'),     # Green highlight
        ])
    ).ask()

    if choice == 0:
        print("\nYou selected: Quit")
        return False
    elif choice == 1:
        print("\nYou selected: Scale Degree Practice")
    elif choice == 2:
        print("\nYou selected: Mode/Scale Practice")

    return True


def test_time_pressure_menu():
    """Test the time pressure selection menu."""
    print("\n" + "="*50)
    print("Testing Time Pressure Selection")
    print("="*50)
    print("\nUse ↑↓ arrow keys to navigate, Enter to select\n")

    choice = questionary.select(
        "Select Time Pressure:",
        choices=[
            questionary.Choice(
                title="None - No time limit, take as long as you need",
                value='none'
            ),
            questionary.Choice(
                title="Low - 15 second timeout per note/sequence",
                value='low'
            ),
            questionary.Choice(
                title="Medium - 10 second timeout per note/sequence",
                value='medium'
            ),
            questionary.Choice(
                title="Hard - 5 second timeout per note/sequence",
                value='hard'
            ),
        ],
        style=questionary.Style([
            ('selected', 'fg:#ffff00 bold'),  # Yellow for selected
            ('pointer', 'fg:#ffff00 bold'),   # Yellow arrow
            ('highlighted', 'fg:#ffff00'),     # Yellow highlight
        ])
    ).ask()

    if choice:
        print(f"\nYou selected: {choice.upper()}")

    return True


def test_mode_selection_menu():
    """Test the mode selection checkbox menu."""
    print("\n" + "="*50)
    print("Testing Mode Selection")
    print("="*50)
    print("\nUse ↑↓ to navigate, Space to toggle, Enter to confirm\n")

    all_modes = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']

    choices = []
    for mode in all_modes:
        if mode == 'Ionian':
            description = f"{mode} (Major scale)"
        elif mode == 'Aeolian':
            description = f"{mode} (Natural minor)"
        else:
            description = mode

        choices.append(
            questionary.Choice(
                title=description,
                value=mode,
                checked=(mode in ['Ionian', 'Aeolian'])  # Default checked
            )
        )

    selected = questionary.checkbox(
        "Select modes to practice (use Space to toggle, Enter to confirm):",
        choices=choices,
        style=questionary.Style([
            ('selected', 'fg:#00ff00'),           # Green for selected items
            ('pointer', 'fg:#00ff00 bold'),       # Green arrow
            ('highlighted', 'fg:#00ff00'),         # Green highlight
            ('checkbox', 'fg:#00ff00'),            # Green checkbox
            ('checkbox-selected', 'fg:#00ff00 bold'),  # Bold green when checked
        ])
    ).ask()

    if selected:
        print(f"\nYou selected: {', '.join(selected)}")
    else:
        print("\nNo modes selected (would default to Ionian and Aeolian)")


if __name__ == "__main__":
    print("\nInteractive Menu Demo")
    print("Press Ctrl+C at any time to exit\n")

    try:
        # Test practice mode menu
        if test_practice_mode_menu():
            # Test time pressure menu
            if test_time_pressure_menu():
                # Test mode selection menu
                test_mode_selection_menu()

        print("\n" + "="*50)
        print("Demo complete!")
        print("="*50)

    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user")
        sys.exit(0)
