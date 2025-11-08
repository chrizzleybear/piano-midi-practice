"""
Main entry point for the Piano Practice App.
"""

import sys
from typing import Optional
from .midi_handler import auto_connect_midi
from .practice_modes import scale_degree_practice, mode_practice, display_final_stats, Colors


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
    print(f"\n{Colors.BOLD}Select Practice Mode:{Colors.RESET}")
    print(f"  {Colors.BLUE}1.{Colors.RESET} Scale Degree Practice")
    print(f"     - Random intervals from a root note")
    print(f"     - Example: 'Play the 3', 'Play the b7'")
    print()
    print(f"  {Colors.BLUE}2.{Colors.RESET} Mode/Scale Practice")
    print(f"     - Play complete modes ascending and descending")
    print(f"     - Example: 'Dorian in F#', 'Lydian in Bb'")
    print()
    print(f"  {Colors.BLUE}Q.{Colors.RESET} Quit")
    print()

    while True:
        try:
            choice = input(f"{Colors.BOLD}Enter choice (1, 2, or Q): {Colors.RESET}").strip().upper()

            if choice == 'Q':
                return 0
            elif choice == '1':
                return 1
            elif choice == '2':
                return 2
            else:
                print(f"{Colors.RED}Invalid choice. Please enter 1, 2, or Q.{Colors.RESET}")

        except (KeyboardInterrupt, EOFError):
            print()
            return 0


def select_time_pressure() -> Optional[float]:
    """
    Display menu and get user's time pressure selection.

    Returns:
        Timeout value in seconds (None for no timeout)
    """
    print(f"\n{Colors.BOLD}Select Time Pressure:{Colors.RESET}")
    print(f"  {Colors.BLUE}1.{Colors.RESET} None")
    print(f"     - No time limit, take as long as you need")
    print()
    print(f"  {Colors.BLUE}2.{Colors.RESET} Low")
    print(f"     - 15 second timeout per note/sequence")
    print()
    print(f"  {Colors.BLUE}3.{Colors.RESET} Medium")
    print(f"     - 10 second timeout per note/sequence")
    print()
    print(f"  {Colors.BLUE}4.{Colors.RESET} Hard")
    print(f"     - 5 second timeout per note/sequence")
    print()

    while True:
        try:
            choice = input(f"{Colors.BOLD}Enter choice (1-4): {Colors.RESET}").strip()

            if choice == '1':
                return TIME_PRESSURE_CONFIG['none']
            elif choice == '2':
                return TIME_PRESSURE_CONFIG['low']
            elif choice == '3':
                return TIME_PRESSURE_CONFIG['medium']
            elif choice == '4':
                return TIME_PRESSURE_CONFIG['hard']
            else:
                print(f"{Colors.RED}Invalid choice. Please enter 1, 2, 3, or 4.{Colors.RESET}")

        except (KeyboardInterrupt, EOFError):
            print()
            # Default to medium if interrupted
            return TIME_PRESSURE_CONFIG['medium']


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

        # Run selected practice mode with timeout
        if mode_choice == 1:
            stats = scale_degree_practice(midi_handler, timeout=timeout)
        elif mode_choice == 2:
            stats = mode_practice(midi_handler, timeout=timeout)
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
