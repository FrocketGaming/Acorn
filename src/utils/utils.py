from pathlib import Path
import sys
import logging


class UtilityManager:
    @staticmethod
    def get_resource_path(relative_path: str) -> Path:
        """Get the absolute path to a resource, handling .exe and source environments."""
        try:
            if hasattr(sys, "_MEIPASS"):
                # PyInstaller's temporary directory
                base_path = Path(sys._MEIPASS)
            else:
                # Normal environment
                base_path = Path(__file__).resolve().parent.parent

            full_path = base_path / relative_path

            # Return the Path object (don't convert to string)
            return full_path
        except Exception as e:
            print(f"Error in get_resource_path: {e}")
            raise
