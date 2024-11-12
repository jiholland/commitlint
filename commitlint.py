#!/usr/bin/env python3
"""
Python module that will lint commit messages according to https://www.conventionalcommits.org
Intended to be used in a Git CI/CD pipeline.

Usage:
    Run without arguments.
    $ python3 commitlint.py

    Pass the Git root directory as an argument.
    $ python3 commitlint.py "$(realpath git_example_root_dir)"

    Pass the GitLab project directory as an argument.
    $ python3 commitlint.py $CI_PROJECT_DIR
"""
__version__ = "24.11.0"
__author__ = "Jorn Ivar Holland"

import subprocess
import sys

def commit_msg(path="."):
    """
    Return the latest commit message if we are in a Git repo.
    """
    if subprocess.run(["git", "-C", path, "status"], stdout = subprocess.DEVNULL, check=True):
        commit = subprocess.run(["git", "-C", path, "log", "-1", "--pretty=%B"],
                                capture_output=True, text=True, check=False)
        return commit.stdout
    return None

def header_type(commit_message):
    """
    Assert commit header type is found in value.
    Example:
      echo "foo: some message" # fails
      echo "fix: some message" # passes
    """
    commit_type = commit_message.split()[0]
    conventional_commit_type = (
            'build:', 'chore:', 'ci:', 'docs:', 'feat:', 'fix:',
            'perf:', 'refactor:', 'revert:', 'style:', 'test:'
    )
    if not commit_type.startswith(tuple(conventional_commit_type)):
        print("Subject type must be one of", conventional_commit_type)
        return True
    return False

def subject_empty(commit_message):
    """
    Assert subject is not empty.
    Example:
      echo "fix:" # fails
      echo "fix: some message" # passes
    """
    commit_header = commit_message.splitlines()[0].strip()
    commit_subject = commit_header.split(":")[-1]

    if ":" not in commit_header or not bool(commit_subject):
        print("Subject may not be empty.")
        return True
    return False

def subject_length(commit_message):
    """
    Assert header has value or less characters.
    Example:
      echo "fix: some message that is way too long and breaks the line max-length" # fails
      echo "fix: some message" # passes
    """
    commit_header = commit_message.splitlines()[0].strip()

    if len(commit_header) > 100:
        print("Subject must not be longer than 100 chars, current length is ", len(commit_header))
        return True
    return False

def subject_case(commit_message):
    """
    Assert subject is in case lower.
    Example:
      echo "fix(SCOPE): Some message" # fails
      echo "fix(SCOPE): Some Message" # fails
      echo "fix(SCOPE): SomeMessage" # fails
      echo "fix(SCOPE): SOMEMESSAGE" # fails
      echo "fix(scope): some message" # passes
      echo "fix(scope): some Message" # passes
    """
    commit_header = commit_message.splitlines()[0].strip()
    commit_subject = commit_header.split(":")[-1]

    if not commit_subject.islower():
        print("Subject must be lower case.")
        return True
    return False

def subject_full_stop(commit_message):
    """
    Assert that subject ends with alphabetic character.
    Example:
        echo "fix: some message." # fails
        echo "fix: some message" # passes
    """
    commit_header = commit_message.splitlines()[0].strip()

    if not commit_header[-1].isalpha():
        print("Subject must end with alphabetic character.")
        return True
    return False

def body_leading_blank(commit_message):
    """
    Assert that body have a leading blank line.
    Example:
        echo "fix: some message
        body" # warning

        echo "fix: some message

        body" # passes
    """
    count = 0

    for line in commit_message.splitlines():
        count += 1
        if count == 2 and line.strip() != "":
            print("Body should have a leading blank line.")
            return True

def body_max_length(commit_message):
    """
    Assert body each line has value or less characters.
    Example:
        echo "fix: some message

        body with multiple lines
        has a message that is way too long and will break the line rule # fails

        echo "fix: some message

        body with multiple lines
        but still no line is too long" # passes
    """
    count = 0

    for line in commit_message.splitlines():
        count += 1
        if count > 2 and len(line) > 100:
            print("Body must not have lines longer than 100 chars.")
            return True

def main():
    """
    Call convention commit functions and count errors.
    Exit with none-zero return code if errors are found.
    """
    error_count = 0
    last_commit = commit_msg(sys.argv[1])

    if header_type(last_commit):
        error_count += 1
    if subject_empty(last_commit):
        error_count += 1
    if subject_length(commit_msg):
        error_count += 1
    if subject_case(commit_msg):
        error_count += 1
    if subject_full_stop(commit_msg):
        error_count += 1
    if body_leading_blank(commit_msg):
        error_count += 1
    if body_max_length(commit_msg):
        error_count += 1

    if error_count > 0:
        print("=========================")
        print(f"The commit message has {error_count} errors.")
        sys.exit(1)
    else:
        print("==============================")
        print("All commit messages are valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()
