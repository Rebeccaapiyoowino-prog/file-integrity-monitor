import argparse
import hashlib
import json
from pathlib import Path


def calculate_hash(file_path):
    """Return the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def build_snapshot(directory):
    """Create a dictionary containing file paths and SHA-256 hashes."""
    root = Path(directory)

    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    snapshot = {}

    for file_path in sorted(root.rglob("*")):
        if file_path.is_file():
            relative_path = file_path.relative_to(root).as_posix()
            snapshot[relative_path] = calculate_hash(file_path)

    return snapshot


def save_baseline(snapshot, baseline_file):
    """Save a snapshot to a JSON baseline file."""
    with open(baseline_file, "w", encoding="utf-8") as file:
        json.dump(snapshot, file, indent=4, sort_keys=True)


def load_baseline(baseline_file):
    """Load a previously generated baseline."""
    path = Path(baseline_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Baseline file not found: {baseline_file}"
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def compare_snapshots(baseline, current):
    """Identify added, modified, and deleted files."""
    baseline_files = set(baseline)
    current_files = set(current)

    added = sorted(current_files - baseline_files)
    deleted = sorted(baseline_files - current_files)

    modified = sorted(
        file_name
        for file_name in baseline_files & current_files
        if baseline[file_name] != current[file_name]
    )

    return {
        "added": added,
        "modified": modified,
        "deleted": deleted,
    }


def print_report(changes):
    """Display integrity-check results."""
    print("\n=== File Integrity Report ===")

    if not any(changes.values()):
        print("No file integrity changes detected.")
        return

    if changes["added"]:
        print("\nAdded files:")
        for file_name in changes["added"]:
            print(f"  + {file_name}")

    if changes["modified"]:
        print("\nModified files:")
        for file_name in changes["modified"]:
            print(f"  ! {file_name}")

    if changes["deleted"]:
        print("\nDeleted files:")
        for file_name in changes["deleted"]:
            print(f"  - {file_name}")


def create_baseline(directory, baseline_file):
    snapshot = build_snapshot(directory)
    save_baseline(snapshot, baseline_file)

    print(
        f"Baseline created successfully with "
        f"{len(snapshot)} monitored file(s)."
    )


def check_integrity(directory, baseline_file):
    baseline = load_baseline(baseline_file)
    current = build_snapshot(directory)

    changes = compare_snapshots(baseline, current)
    print_report(changes)

    return changes


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Detect file additions, modifications, and deletions "
            "using SHA-256 hashes."
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    baseline_parser = subparsers.add_parser(
        "baseline",
        help="Create a trusted file-integrity baseline"
    )

    baseline_parser.add_argument(
        "directory",
        help="Directory to monitor"
    )

    baseline_parser.add_argument(
        "baseline_file",
        help="JSON file used to store the baseline"
    )

    check_parser = subparsers.add_parser(
        "check",
        help="Compare current files against an existing baseline"
    )

    check_parser.add_argument(
        "directory",
        help="Directory to monitor"
    )

    check_parser.add_argument(
        "baseline_file",
        help="Existing baseline JSON file"
    )

    args = parser.parse_args()

    if args.command == "baseline":
        create_baseline(
            args.directory,
            args.baseline_file
        )

    elif args.command == "check":
        check_integrity(
            args.directory,
            args.baseline_file
        )


if __name__ == "__main__":
    main()
