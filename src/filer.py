import os
from shutil import copy2, rmtree
from pathlib import Path

def copy_static_files(src_dir, dest_dir, clear_dest=False):
    """
    Recursively copies static files from src_dir to dest_dir,
    preserving the directory structure and file metadata.
    """
    src_path = Path(src_dir)
    dest_path = Path(dest_dir)

    if not src_path.exists() or not src_path.is_dir():
        raise ValueError(f"Source directory {src_dir} does not exist or is not a directory.")
    
    if clear_dest and dest_path.exists():
        rmtree(dest_path)
        dest_path.mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(src_path):
        relative_root = Path(root).relative_to(src_path)
        target_root = dest_path / relative_root

        # Create target directories if they don't exist
        target_root.mkdir(parents=True, exist_ok=True)

        for file in files:
            src_file = Path(root) / file
            dest_file = target_root / file
            copy2(src_file, dest_file)  # copy2 preserves metadata 
            