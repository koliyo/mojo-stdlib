#!/usr/bin/env python3
"""Sync mojo stdlib and docs from modular submodule to mojo/ directory."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result


def main():
    """Main sync function."""
    parser = argparse.ArgumentParser(description="Sync mojo stdlib and docs.")
    parser.add_argument(
        "--skip-submodule-update",
        action="store_true",
        help="Skip updating the modular submodule.",
    )
    parser.add_argument(
        "--skip-commit",
        action="store_true",
        help="Skip creating a git commit.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.resolve()

    # Step 1: Update submodule
    if args.skip_submodule_update:
        print("Step 1: Skipping submodule update.")
    else:
        print("Step 1: Updating git submodule...")
        run_command(["git", "submodule", "update", "--remote", "--merge"])
    
    # Step 2: Copy directories
    print("\nStep 2: Copying directories...")
    
    source_stdlib = repo_root / "modular" / "mojo" / "stdlib"
    source_docs = repo_root / "modular" / "mojo" / "docs"
    dest_stdlib = repo_root / "mojo" / "stdlib"
    dest_docs = repo_root / "mojo" / "docs"
    
    # Verify source directories exist
    if not source_stdlib.exists():
        print(f"Error: Source directory {source_stdlib} does not exist", file=sys.stderr)
        sys.exit(1)
    if not source_docs.exists():
        print(f"Error: Source directory {source_docs} does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Delete existing copies if they exist
    if dest_stdlib.exists():
        print(f"Deleting existing {dest_stdlib}...")
        shutil.rmtree(dest_stdlib)
    if dest_docs.exists():
        print(f"Deleting existing {dest_docs}...")
        shutil.rmtree(dest_docs)
    
    # Create parent directory if needed
    dest_stdlib.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy directories
    print(f"Copying {source_stdlib} to {dest_stdlib}...")
    shutil.copytree(source_stdlib, dest_stdlib)
    
    print(f"Copying {source_docs} to {dest_docs}...")
    shutil.copytree(source_docs, dest_docs)
    
    # Step 3: Create zip artifact
    print("\nStep 3: Creating zip artifact...")
    zip_path = repo_root / "mojo-stdlib.zip"
    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(
        base_name=str(zip_path.with_suffix("")),
        format="zip",
        root_dir=str(repo_root / "mojo"),
        base_dir="stdlib",
    )

    if args.skip_commit:
        print("Skipping git commit.")
        print("\nSync complete!")
        return

    # Step 4: Make git commit
    print("\nStep 4: Making git commit...")

    # Check if there are changes to commit
    run_command(["git", "add", "mojo/stdlib", "mojo/docs", "mojo-stdlib.zip"], check=False)

    result = run_command(["git", "status", "--porcelain"], check=False)
    if not result.stdout.strip():
        print("No changes to commit.")
        return

    run_command(["git", "commit", "-m", "Sync stdlib and docs from modular submodule"])

    print("\nSync complete!")


if __name__ == "__main__":
    main()
