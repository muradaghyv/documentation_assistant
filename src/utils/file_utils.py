from pathlib import Path

def create_directory(directory_path: str) -> None:
    """Create directory if it doesn't exist."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent

def get_data_directory() -> Path:
    """Get the data directory path."""
    return get_project_root() / 'data'