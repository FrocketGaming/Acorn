import requests
from pathlib import Path
import arrow
import subprocess
import sys


class UpdateManager:
    CURRENT_VERISON = "0.3"
    REPO = "FrocketGaming/Acorn"
    URL = f"https://api.github.com/repos/{REPO}/releases"
    DOWNLOAD_DIR = Path.home() / "Downloads"
    UPDATE_SCRIPT = DOWNLOAD_DIR / "Update_Acorn.bat"
    FILE_NAME = f"acornInstaller_{arrow.now().format('YYYY-MM-DD')}.exe"

    def __init__(self):
        self.application_path = Path.cwd().parent
        self.headers = {
            "User-Agent": "Mozilla/5.0",
        }
        self.update_required = False
        self.response = self.get_response()
        self.latest_version = self.get_latest_version()
        self.version_check()

    @staticmethod
    def get_current_version():
        return UpdateManager.CURRENT_VERISON

    def version_check(self):
        if (
            self.CURRENT_VERISON < self.latest_version
            and self.latest_version is not None
        ):
            self.update_required = True

    def update(self):
        download_url = self.get_installer()
        self.download_latest_version(download_url)
        self.create_update_bat()
        self.process_update()

    def get_response(self):
        try:
            r = requests.get(self.URL, headers=self.headers)
            r.raise_for_status()

            return r.json()

        except requests.exceptions.RequestException as e:
            return None

    def get_latest_version(self):
        try:
            return self.response[0]["tag_name"]
        except Exception:
            return None

    def get_installer(self):
        if "assets" in self.response[0]:
            return self.response[0]["assets"][0]["browser_download_url"]
        return None

    def download_latest_version(self, download_url):
        self.headers.update({"Accept": "application/octet-stream"})

        exe_path = self.DOWNLOAD_DIR / self.FILE_NAME

        try:
            with requests.get(
                download_url, headers=self.headers, stream=True, allow_redirects=True
            ) as r:
                r.raise_for_status()

                with open(exe_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            return exe_path

        except requests.exceptions.RequestException as e:
            return None

    def create_update_bat(self):
        with open(self.UPDATE_SCRIPT, "w") as f:
            f.write(f"""
            @echo off
            timeout /t 2 /nobreak >nul
            start /wait "" "{str(self.DOWNLOAD_DIR / self.FILE_NAME)}"
            start "" "{str(self.application_path / "acorn.exe")}"
            del "%~f0"
            exit
            """)

    def process_update(self):
        subprocess.Popen(str(self.UPDATE_SCRIPT), shell=True)
        sys.exit()


if __name__ == "__main__":
    um = UpdateManager()
