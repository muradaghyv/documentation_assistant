from pathlib import Path
from typing import List

def create_directory(directory_path: str) -> None:
    """Create directory if it doesn't exist."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent

def get_data_directory() -> Path:
    """Get the data directory path."""
    return get_project_root() / 'data'

def list_files(directory: Path, extension: str = None) -> List[Path]:
    """List all files in directory with optional extension filter."""
    if extension:
        return list(directory.glob(f"*.{extension}"))
    return list(directory.glob("*.*"))