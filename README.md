# File Integrity Monitor

A Python cybersecurity utility for detecting unauthorized file changes using SHA-256 cryptographic hashes.

## Overview

The File Integrity Monitor creates a trusted baseline of files within a monitored directory and later compares the current state of those files against the baseline.

It identifies files that have been:

- Added
- Modified
- Deleted

This type of monitoring can help security teams identify unexpected or unauthorized changes to sensitive configuration files, system files, and application resources.

## Skills Demonstrated

This project demonstrates practical experience with:

- Python scripting
- SHA-256 cryptographic hashing
- File integrity monitoring
- Defensive cybersecurity concepts
- Filesystem analysis
- JSON data storage
- Command-line interfaces
- Automated unit testing
- Technical documentation

## Features

- Generates SHA-256 hashes for monitored files
- Creates trusted integrity baselines
- Detects modified files
- Detects newly added files
- Detects deleted files
- Supports recursive directory monitoring
- Stores baseline information in JSON format
- Provides clear command-line reports
- Includes automated unit tests

## Project Structure

```text
file-integrity-monitor/
├── monitor.py
├── sample_files/
│   └── server.conf
├── tests/
│   └── test_monitor.py
├── README.md
├── .gitignore
└── LICENSE