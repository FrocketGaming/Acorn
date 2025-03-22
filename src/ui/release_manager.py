from pathlib import Path


#TODO: When should I display the release notes, how do I determine when a user has updated their client?
"""
- Use a DB entry.
- Use a local file on the computer to determine.
"""

class ReleaseManager:
    @staticmethod
    def load_release_notes():
        release_file_path = Path.home() / "release_notes.md"
        with open(release_file_path, "r") as file:
            data = file.readlines()

        return data
