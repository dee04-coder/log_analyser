"""Step 1: read login records and flag accounts with many failed logins.
 
Usage:
    python count_failures.py
    python count_failures.py data/sample_logins.csv --threshold 5
"""
 
import argparse
import csv
from collections import Counter
from pathlib import Path
 
DEFAULT_FILE = Path("data/sample_logins.csv")
DEFAULT_THRESHOLD = 5
 
 
def read_logins(path):
    """Read the CSV and return a list of login records (dicts)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
 
 
def count_failures(records):
    """Return a Counter of failed login attempts per username."""
    failures = Counter()
    for row in records:
        if row["status"].strip().lower() == "failure":
            failures[row["username"].strip()] += 1
    return failures
 
 
def main():
    parser = argparse.ArgumentParser(description="Count failed logins per user.")
    parser.add_argument("csv_file", nargs="?", default=DEFAULT_FILE, type=Path)
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    args = parser.parse_args()
 
    records = read_logins(args.csv_file)
    failures = count_failures(records)
 
    print(f"Read {len(records)} login records from {args.csv_file}\n")
 
    print("Failed logins per username:")
    for username, count in failures.most_common():
        print(f"  {username:<10} {count}")
 
    print(f"\nAccounts with {args.threshold}+ failures (need investigation):")
    flagged = [(u, c) for u, c in failures.most_common() if c >= args.threshold]
    if flagged:
        for username, count in flagged:
            print(f"  {username:<10} {count} failures")
    else:
        print("  none")
 
 
if __name__ == "__main__":
    main()
