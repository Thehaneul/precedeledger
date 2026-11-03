"""Obtain one official pinned release archive for both local verification tools."""
import shutil
from pathlib import Path

from genvm_linter.validate.artifacts import download_artifacts
from gltest.direct import sdk_loader

VERSION = "v0.3.0-rc7"


def main():
    source = Path(download_artifacts(VERSION))
    destination = sdk_loader.CACHE_DIR / ("genvm-universal-" + VERSION + ".tar.xz")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        print("Direct-mode SDK archive already present:", destination)
        return
    try:
        destination.hardlink_to(source)
    except OSError:
        shutil.copyfile(source, destination)
    print("Prepared official SDK release", VERSION, "for direct-mode tests.")


if __name__ == "__main__":
    main()
