GitHub User Activity CLI
A simple command-line tool to fetch and display the recent public activity of a GitHub user.

Description
This is a command-line application that uses the GitHub API to retrieve a user's recent public events. Instead of reading through complex JSON data, the application parses the data and displays a clean, concise summary of the user's 3 most recent actions—such as pushing commits, publishing releases, or creating new branches/repositories.

Features
Fetches real-time public event data using the GitHub API.

Automatically handles different types of GitHub events (Push, Release, Create, Delete).

Formats the raw JSON data into easy-to-read, human-friendly sentences.

Built entirely using Python's standard libraries (urllib, json, argparse)—no external dependencies required.

Takes the GitHub username directly as a command-line argument for quick usage.

How to Use
Make sure you have Python installed on your system.

Clone or download the project files.

Open your terminal or command prompt.

Navigate to the project directory.

Run the script by passing a GitHub username as an argument. For example:

Bash
python github_activity.py kamranahmedse
Example Output:

Plaintext
OUTPUT:
- Pushed 3 commit(s) to kamranahmedse/developer-roadmap
- Published release 1.1.0 in kamranahmedse/mondex
- Created a new branch in kamranahmedse/test-repo
Project Files
github_activity.py: Contains the core logic for API requests, JSON parsing, and event formatting.

README.md: This file, providing information about the project.

[Inspiration](https://roadmap.sh/projects/github-user-activity)
