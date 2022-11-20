from pathlib import Path


def get_project_root() -> Path:
    r"""."""
    return Path(__file__).parent.parent
