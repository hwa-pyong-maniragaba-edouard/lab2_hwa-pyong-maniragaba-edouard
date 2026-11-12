#!/bin/bash
# organizer.sh for archiving the grades.csv with a timestamp, resets the workspace,
# and logs the operation to organizer.log

ARCHIVE_DIR="archive"
SOURCE_FILE="grades.csv"

# this code is to make sure grades.csv exists before doing anything
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' was not found in the current directory." >&2
    exit 1
fi

# this is to  create archives directory if it does not exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR"
fi
