"""
Main entry point for the Piano Practice App.
"""

import sys
from typing import Optional, List
import questionary
from .midi_handler import auto_connect_midi
from .practice_modes import scale_degree_practice, mode_practice, display_final_stats, Colors
from .music_theory import get_mode_names


# Time pressure configurations (timeout in seconds)
TIME_PRESSURE_CONFIG = {
    'none': None,      # No timeout
    'low': 15.0,       # 15 seconds
    'medium': 10.0,    # 10 seconds
    'hard': 5.0,       # 5 seconds
}


def select_practice_mode() -> int:
    """
    Display menu and get user's practice mode selection.

    Returns:
        Mode number (1 or 2), or 0 to exit
    """
    try:
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

        if choice is None:  # User pressed Ctrl+C
            return 0

        return choice

    except (KeyboardInterrupt, EOFError):
        print()
        return 0


def select_time_pressure() -> Optional[float]:
    """
    Display menu and get user's time pressure selection.

    Returns:
        Timeout value in seconds (None for no timeout)
    """
    try:
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

        if choice is None:  # User pressed Ctrl+C
            # Default to medium if interrupted
            return TIME_PRESSURE_CONFIG['medium']

        return TIME_PRESSURE_CONFIG[choice]

    except (KeyboardInterrupt, EOFError):
        print()
        # Default to medium if interrupted
        return TIME_PRESSURE_CONFIG['medium']


def select_modes() -> List[str]:
    """
    Display checkbox menu to select which modes to practice.

    Returns:
        List of selected mode names (defaults to Ionian and Aeolian)
    """
    all_modes = get_mode_names()

    # Create choices with default selection for Ionian and Aeolian
    choices = []
    for mode in all_modes:
        # Add description for common modes
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
                checked=(mode in ['Ionian', 'Aeolian'])  # Default to major and minor
            )
        )

    try:
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

        if selected is None or len(selected) == 0:
            # Default to Ionian and Aeolian if cancelled or nothing selected
            print(f"{Colors.YELLOW}No modes selected. Using default: Ionian and Aeolian{Colors.RESET}")
            return ['Ionian', 'Aeolian']

        return selected

    except (KeyboardInterrupt, EOFError):
        print()
        # Default to Ionian and Aeolian if interrupted
        return ['Ionian', 'Aeolian']


def main():
    """Main application entry point."""

    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}  Piano Practice App - MIDI Trainer{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}\n")

    # Connect to MIDI device
    print("Connecting to MIDI device...")
    midi_handler, success = auto_connect_midi()

    if not success or midi_handler is None:
        print(f"\n{Colors.RED}Failed to connect to MIDI device.{Colors.RESET}")
        print("Please ensure:")
        print("  1. Your MIDI keyboard is connected")
        print("  2. No other application is using the MIDI device")
        print("  3. Required packages are installed (run: pip install -r requirements.txt)")
        sys.exit(1)

    try:
        # Select practice mode
        mode_choice = select_practice_mode()

        if mode_choice == 0:
            print(f"{Colors.YELLOW}Exiting...{Colors.RESET}")
            return

        # Select time pressure
        timeout = select_time_pressure()

        # If mode practice, select which modes to include
        enabled_modes = None
        if mode_choice == 2:
            enabled_modes = select_modes()
            print(f"\n{Colors.BLUE}Practicing modes: {', '.join(enabled_modes)}{Colors.RESET}\n")

        # Run selected practice mode with timeout
        if mode_choice == 1:
            stats = scale_degree_practice(midi_handler, timeout=timeout)
        elif mode_choice == 2:
            stats = mode_practice(midi_handler, timeout=timeout, enabled_modes=enabled_modes)
        else:
            print(f"{Colors.RED}Invalid mode selection{Colors.RESET}")
            return

        # Display final statistics
        display_final_stats(stats)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")

    except Exception as e:
        print(f"\n{Colors.RED}Error during practice session: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()

    finally:
        # Clean up MIDI connection
        if midi_handler:
            midi_handler.close()
            print(f"{Colors.BLUE}MIDI connection closed.{Colors.RESET}")

    print("\nThanks for practicing!\n")


if __name__ == "__main__":
    main()
