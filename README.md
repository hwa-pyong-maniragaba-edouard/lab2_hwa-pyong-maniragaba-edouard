# Lab 2: ALU Transcript Generator

This project works out a student's final standing from a CSV of course grades. A Python program validates the data, calculates the final grade and GPA, decides pass or fail, and lists which assignments can be resubmitted. A Bash script then archives the grades file so the next batch can start clean.

## What's in this repository

- grade-evaluator.py: the grade evaluator (Python)
- organizer.sh: the archiving script (Bash)
- grades.csv: the sample grades used for testing
- .gitignore: keeps the archive/ folder and organizer.log out of version control, since the organizer creates them

## Before you start

You need three things installed:

- Python 3.6 or newer. The program only uses the standard library (csv, os, sys), so there is nothing to pip install.
- Bash, to run organizer.sh. Linux and macOS have it built in. On Windows, use Git Bash or WSL.
- Git, to download the project.

You can check each one from a terminal:

    python3 --version
    bash --version
    git --version

Each command should print a version number. If one says "command not found", install that tool first. On Windows, Python is sometimes called python instead of python3, so use whichever one works for you.

## Getting the project

    git clone https://github.com/hwa-pyong-maniragaba-edouard/lab2_hwa-pyong-maniragaba-edouard.git
    cd lab2_hwa-pyong-maniragaba-edouard

Check that grades.csv is there and has data:

    ls
    cat grades.csv

You should see a header line followed by five rows. Do this before anything else, because organizer.sh empties grades.csv when it runs.

## Step 1: Run the grade evaluator

    python3 grade-evaluator.py

The program asks for a file name. Type:

    grades.csv

### What the input file looks like

The CSV needs these four columns in its first line:

    assignment,group,score,weight

- group is either Formative or Summative
- score is a number from 0 to 100
- weight is a number; all weights together must add up to 100, with Formative adding up to 60 and Summative adding up to 40

### Expected output for the sample data

    --- Processing Grades ---
    Score check passed.
    Weight check passed.
    Formative: 34.00/60
    Summative: 26.00/40
    Final grade: 60.00/100
    GPA: 3.00/5.0

    Final status: PASSED
    Eligible for resubmission (highest weight failed formative):
      - Group Exercise (score 40, weight 20)
      - Functions and Debugging Lab (score 45, weight 20)

### How the grading works

- Every score must be between 0 and 100.
- The final grade is the sum of each score multiplied by its weight, divided by 100.
- GPA = (Total Grade / 100) * 5.0
- A student passes only with at least 50% in both Formative and Summative. Otherwise the status is FAILED.
- Resubmission is for failed formative assignments (below 50) that carry the highest weight. If several share that weight, all of them are listed.

### If something goes wrong

The program stops with a message that says what to fix, for example when the file does not exist, a column is missing, a score or weight is not a number, a score is outside 0 to 100, the weights do not add up, or a group is not Formative or Summative.

## Step 2: Run the organizer

Once you are done with the evaluator, archive the grades:

    chmod +x organizer.sh
    ./organizer.sh

The script will:

1. Check that grades.csv exists, and stop with an error if it does not.
2. Create an archive/ folder if there isn't one yet.
3. Rename grades.csv with a timestamp and move it into archive/, for example archive/grades_20261112-153859.csv.
4. Create a new, empty grades.csv, ready for the next batch.
5. Add a line to organizer.log with the timestamp, the original file name and the archived file name. The log keeps growing with every run.

Running it leaves you with an empty grades.csv. To get your data back for another test, copy the archived file back:

    cp archive/grades_<timestamp>.csv grades.csv

Or, if you cloned the repository with git, restore it with:

    git checkout grades.csv
