"""
MIDI device handling for input detection and note parsing.
"""

import mido
from typing import List, Optional, Tuple
import time


class MIDIHandler:
    """Handles MIDI device connection and input parsing."""

    def __init__(self):
        self.input_port: Optional[mido.ports.BaseInput] = None
        self.device_name: Optional[str] = None

    def get_midi_devices(self) -> List[str]:
        """
        Get list of available MIDI input devices.

        Returns:
            List of device names
        """
        return mido.get_input_names()

    def connect_midi_input(self, device_name: Optional[str] = None) -> bool:
        """
        Connect to a MIDI input device.

        Args:
            device_name: Specific device name to connect to.
                        If None, connects to first available device.

        Returns:
            True if connection successful, False otherwise
        """
        devices = self.get_midi_devices()

        if not devices:
            print("No MIDI input devices found!")
            return False

        # If no device specified, use the first one
        if device_name is None:
            if len(devices) == 1:
                device_name = devices[0]
            else:
                # Multiple devices - let user choose
                print("\nMultiple MIDI devices found:")
                for i, dev in enumerate(devices, 1):
                    print(f"  {i}. {dev}")

                while True:
                    try:
                        choice = input("\nSelect device number (or press Enter for device 1): ").strip()
                        if choice == "":
                            choice = "1"
                        idx = int(choice) - 1
                        if 0 <= idx < len(devices):
                            device_name = devices[idx]
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(devices)}")
                    except ValueError:
                        print("Please enter a valid number")
                    except (KeyboardInterrupt, EOFError):
                        print("\nConnection cancelled")
                        return False

        # Attempt to connect
        try:
            self.input_port = mido.open_input(device_name)
            self.device_name = device_name
            print(f"\nConnected to MIDI device: {device_name}")
            return True
        except (IOError, OSError) as e:
            print(f"Error connecting to {device_name}: {e}")
            return False

    def listen_for_note(self, timeout: Optional[float] = None) -> Optional[int]:
        """
        Listen for a note-on message and return the MIDI note number.
        Blocks until a note is played or timeout is reached.

        Args:
            timeout: Maximum time to wait in seconds. None = wait forever.

        Returns:
            MIDI note number (0-127) or None if timeout or error
        """
        if not self.input_port:
            raise RuntimeError("MIDI port not connected. Call connect_midi_input() first.")

        start_time = time.time() if timeout else None

        try:
            while True:
                # Check timeout
                if timeout and (time.time() - start_time) >= timeout:
                    return None

                # Poll for messages with short timeout to allow checking our timeout
                msg = self.input_port.poll()

                if msg is None:
                    time.sleep(0.01)  # Short sleep to avoid busy waiting
                    continue

                # Check for note_on message with velocity > 0
                # (Some keyboards send note_on with velocity=0 instead of note_off)
                if msg.type == 'note_on' and msg.velocity > 0:
                    return msg.note

        except KeyboardInterrupt:
            raise  # Re-raise to allow graceful shutdown

    def close(self):
        """Close the MIDI input port."""
        if self.input_port:
            self.input_port.close()
            self.input_port = None
            self.device_name = None


def auto_connect_midi() -> Tuple[Optional[MIDIHandler], bool]:
    """
    Convenience function to auto-detect and connect to MIDI device.

    Returns:
        Tuple of (MIDIHandler instance or None, success boolean)
    """
    handler = MIDIHandler()
    success = handler.connect_midi_input()

    if success:
        return handler, True
    else:
        return None, False
