"""
Practice mode implementations for different training exercises.
"""

import random
from typing import Dict, Tuple, List, Optional
from .music_theory import (
    get_random_note,
    get_random_interval,
    calculate_interval,
    midi_to_note_name,
    notes_match,
    format_interval_prompt,
    generate_scale,
    get_random_mode
)
from .midi_handler import MIDIHandler


# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class SessionStats:
    """Track practice session statistics."""

    def __init__(self):
        self.correct = 0
        self.incorrect = 0
        self.total_attempts = 0

    def record_correct(self):
        self.correct += 1
        self.total_attempts += 1

    def record_incorrect(self):
        self.incorrect += 1
        self.total_attempts += 1

    def get_accuracy(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return (self.correct / self.total_attempts) * 100

    def __str__(self) -> str:
        return (f"Correct: {self.correct} | "
                f"Incorrect: {self.incorrect} | "
                f"Accuracy: {self.get_accuracy():.1f}%")


def scale_degree_practice(midi_handler: MIDIHandler, timeout: Optional[float] = 10.0) -> SessionStats:
    """
    Main scale degree practice mode.

    Flow:
    1. Select random root note
    2. User plays root note
    3. Prompt random scale degrees
    4. After 5-7 prompts, select new root
    5. Continue until user quits

    Args:
        midi_handler: Connected MIDI handler instance
        timeout: Timeout in seconds per note (None for no timeout)

    Returns:
        SessionStats object with session results
    """
    stats = SessionStats()
    print(f"\n{Colors.BOLD}=== Scale Degree Practice Mode ==={Colors.RESET}")
    print("Play the notes as prompted. Press Ctrl+C to exit.\n")

    try:
        while True:
            # Select new root note
            root_note = get_random_note()
            prompts_in_round = random.randint(5, 7)

            # Prompt for root note
            print(f"\n{Colors.BLUE}{Colors.BOLD}New Root Note:{Colors.RESET}")
            if not _prompt_and_validate(midi_handler, stats, root_note, root_note, is_root=True, timeout=timeout):
                continue  # Retry if incorrect

            # Prompt for scale degrees
            for _ in range(prompts_in_round):
                interval = get_random_interval()
                expected_note = calculate_interval(root_note, interval)

                prompt_text = f"Play {format_interval_prompt(interval)} (from {root_note})"

                if not _prompt_and_validate(midi_handler, stats, expected_note, prompt_text, timeout=timeout):
                    # User got it wrong, repeat this interval
                    _prompt_and_validate(midi_handler, stats, expected_note, prompt_text, timeout=timeout)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Practice session ended.{Colors.RESET}")

    return stats


def _prompt_and_validate(
    midi_handler: MIDIHandler,
    stats: SessionStats,
    expected_note: str,
    prompt_text: str,
    is_root: bool = False,
    timeout: float = 10.0
) -> bool:
    """
    Display prompt, listen for note, and validate input.

    Args:
        midi_handler: MIDI handler instance
        stats: Session statistics tracker
        expected_note: Expected note name
        prompt_text: Text to display to user
        is_root: Whether this is a root note prompt
        timeout: Timeout in seconds

    Returns:
        True if correct, False if incorrect
    """
    print(f"\n{Colors.BOLD}Play: {prompt_text}{Colors.RESET}")

    # Listen for note with timeout
    midi_note = midi_handler.listen_for_note(timeout=timeout)

    if midi_note is None:
        # Timeout - show hint
        print(f"{Colors.YELLOW}⏱  Hint: The note is {expected_note}{Colors.RESET}")
        # Listen again without timeout
        midi_note = midi_handler.listen_for_note()

    played_note = midi_to_note_name(midi_note)

    # Validate
    if notes_match(played_note, expected_note):
        print(f"{Colors.GREEN}✓ Correct!{Colors.RESET}")
        if not is_root:  # Don't count root notes in stats
            stats.record_correct()
        return True
    else:
        print(f"{Colors.RED}✗ Wrong note (you played {played_note}, expected {expected_note}){Colors.RESET}")
        if not is_root:  # Don't count root notes in stats
            stats.record_incorrect()
        return False


def mode_practice(midi_handler: MIDIHandler, timeout: Optional[float] = 10.0) -> SessionStats:
    """
    Mode/Scale practice mode.

    Flow:
    1. Select random mode and key center
    2. Display mode and key to user
    3. User plays scale ascending (8 notes)
    4. User plays scale descending (8 notes)
    5. Continue with new mode/key

    Args:
        midi_handler: Connected MIDI handler instance
        timeout: Timeout in seconds per note (None for no timeout)
                 Will be multiplied for full scale sequences

    Returns:
        SessionStats object with session results
    """
    stats = SessionStats()
    print(f"\n{Colors.BOLD}=== Mode Practice ==={Colors.RESET}")
    print("Play the complete scale ascending, then descending.")
    print("Press Ctrl+C to exit.\n")

    # Calculate sequence timeout (multiply by 3 for 8-note sequences)
    sequence_timeout = None if timeout is None else timeout * 3

    try:
        while True:
            # Select random mode and key
            mode = get_random_mode()
            key = get_random_note()

            # Generate the scale
            scale_ascending = generate_scale(key, mode)
            scale_descending = scale_ascending[::-1]  # Reverse for descending

            # Display prompt
            print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*50}{Colors.RESET}")
            print(f"{Colors.BOLD}Mode: {mode} | Key: {key}{Colors.RESET}")
            print(f"{Colors.BLUE}Scale: {' - '.join(scale_ascending)}{Colors.RESET}")
            print(f"{Colors.BLUE}{'='*50}{Colors.RESET}\n")

            # Practice ascending
            print(f"{Colors.BOLD}Play ASCENDING:{Colors.RESET}")
            ascending_correct = _play_scale_sequence(
                midi_handler,
                scale_ascending,
                "ascending",
                timeout=sequence_timeout
            )

            if ascending_correct:
                stats.record_correct()
                print(f"\n{Colors.BOLD}Play DESCENDING:{Colors.RESET}")
                descending_correct = _play_scale_sequence(
                    midi_handler,
                    scale_descending,
                    "descending",
                    timeout=sequence_timeout
                )

                if descending_correct:
                    stats.record_correct()
                    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Complete! Well done!{Colors.RESET}")
                else:
                    stats.record_incorrect()
                    print(f"\n{Colors.YELLOW}Try this mode again...{Colors.RESET}")
            else:
                stats.record_incorrect()
                print(f"\n{Colors.YELLOW}Try this mode again...{Colors.RESET}")

            # Small pause before next round
            input(f"\n{Colors.BOLD}Press Enter for next mode...{Colors.RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Practice session ended.{Colors.RESET}")

    return stats


def _play_scale_sequence(
    midi_handler: MIDIHandler,
    expected_scale: List[str],
    direction: str,
    timeout: Optional[float] = 15.0
) -> bool:
    """
    Listen for user to play a sequence of notes and validate against expected scale.

    Args:
        midi_handler: MIDI handler instance
        expected_scale: List of expected note names in order
        direction: "ascending" or "descending" for display
        timeout: Timeout for the entire sequence (None for no timeout)

    Returns:
        True if all notes were correct, False otherwise
    """
    import time

    start_time = time.time() if timeout is not None else None
    notes_played = []
    current_index = 0

    print(f"  Expected: {' → '.join(expected_scale)}")
    print(f"  {Colors.YELLOW}Playing...{Colors.RESET}", end=" ", flush=True)

    while current_index < len(expected_scale):
        # Check timeout for entire sequence
        if timeout is not None and start_time is not None:
            if (time.time() - start_time) >= timeout:
                print(f"\n  {Colors.RED}⏱ Timeout! Try again.{Colors.RESET}")
                return False

        # Listen for next note (short timeout per note)
        midi_note = midi_handler.listen_for_note(timeout=3.0)

        if midi_note is None:
            continue  # Keep waiting

        played_note = midi_to_note_name(midi_note)
        expected_note = expected_scale[current_index]

        # Show progress
        print(f"{played_note}", end=" ", flush=True)
        notes_played.append(played_note)

        # Check if correct
        if notes_match(played_note, expected_note):
            current_index += 1
        else:
            # Wrong note
            print(f"\n  {Colors.RED}✗ Wrong! Expected {expected_note}, got {played_note}{Colors.RESET}")
            print(f"  You played: {' → '.join(notes_played)}")
            return False

    # All notes correct
    print(f"\n  {Colors.GREEN}✓ {direction.capitalize()} scale correct!{Colors.RESET}")
    return True


def display_final_stats(stats: SessionStats):
    """
    Display final session statistics.

    Args:
        stats: Session statistics
    """
    print(f"\n{Colors.BOLD}=== Session Statistics ==={Colors.RESET}")
    print(str(stats))
    print()
