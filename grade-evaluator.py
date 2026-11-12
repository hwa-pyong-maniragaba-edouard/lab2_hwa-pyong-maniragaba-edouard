import csv
import os
import sys

REQUIRED_COLUMNS = ["assignment", "group", "score", "weight"]


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input(
        "Enter the name of the CSV file to process (e.g., grades.csv): "
    ).strip()

    if filename == "":
        print("Error: no file name entered. Example: grades.csv")
        sys.exit(1)

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # The header row must contain every column we need
            columns = reader.fieldnames or []
            missing = [name for name in REQUIRED_COLUMNS if name not in columns]
            if len(missing) > 0:
                print(
                    f"Error: '{filename}' is missing column(s): {', '.join(missing)}."
                )
                print(f"The first line must be: {','.join(REQUIRED_COLUMNS)}")
                sys.exit(1)

            # Row 1 is the header, so data starts on row 2
            for row_number, row in enumerate(reader, start=2):
                try:
                    # Convert numeric fields to floats for calculations
                    assignments.append(
                        {
                            "assignment": row["assignment"],
                            "group": row["group"],
                            "score": float(row["score"]),
                            "weight": float(row["weight"]),
                        }
                    )
                except (TypeError, ValueError):
                    print(
                        f"Error: row {row_number} of '{filename}' has a score or weight "
                        f"that is not a number (score='{row['score']}', weight='{row['weight']}')."
                    )
                    sys.exit(1)
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if len(assignments) == 0:
        print(f"Error: '{filename}' has no assignments to evaluate.")
        sys.exit(1)

    return assignments


def evaluate_grades(data):
    """
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    # a) Check if all scores are percentage based (0-100)
    invalid_scores = []
    for item in data:
        # "not 0 <= x <= 100" also catches nan, which "x < 0 or x > 100" would miss
        if not 0 <= item["score"] <= 100:
            invalid_scores.append(item)
    if len(invalid_scores) > 0:
        print("Error: scores must be between 0 and 100. Please fix:")
        for item in invalid_scores:
            print(f"  - {item['assignment']}: {item['score']:g}")
        sys.exit(1)
    print("Score check passed.")

    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    total_weight = 0
    formative_weight = 0
    summative_weight = 0
    for item in data:
        group = item["group"].strip().lower()
        if item["weight"] < 0:
            print(f"Error: negative weight for '{item['assignment']}'.")
            sys.exit(1)
        total_weight += item["weight"]
        if group == "formative":
            formative_weight += item["weight"]
        elif group == "summative":
            summative_weight += item["weight"]
        else:
            print(
                f"Error: unknown group '{item['group']}' for '{item['assignment']}'. "
                "Use 'Formative' or 'Summative'."
            )
            sys.exit(1)

    weight_errors = []
    if round(total_weight, 6) != 100:
        weight_errors.append(f"total weight is {total_weight:g}, it must be 100")
    if round(formative_weight, 6) != 60:
        weight_errors.append(f"formative weight is {formative_weight:g}, it must be 60")
    if round(summative_weight, 6) != 40:
        weight_errors.append(f"summative weight is {summative_weight:g}, it must be 40")
    if len(weight_errors) > 0:
        print("Error: invalid weights:")
        for message in weight_errors:
            print(f"  - {message}")
        sys.exit(1)
    print("Weight check passed.")

    # c) Calculate the Final Grade and GPA
    formative_earned = 0
    summative_earned = 0
    for item in data:
        points = item["score"] * item["weight"] / 100
        if item["group"].strip().lower() == "formative":
            formative_earned += points
        else:
            summative_earned += points
    total_grade = formative_earned + summative_earned
    gpa = (total_grade / 100) * 5.0
    print(f"Formative: {formative_earned:.2f}/60")
    print(f"Summative: {summative_earned:.2f}/40")
    print(f"Final grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}/5.0")

    # d) Determine Pass/Fail status (>= 50% in BOTH categories)
    formative_percent = formative_earned / formative_weight * 100
    summative_percent = summative_earned / summative_weight * 100
    if formative_percent >= 50 and summative_percent >= 50:
        status = "PASSED"
    else:
        status = "FAILED"

    # e) Check for failed formative assignments (< 50%)
    #    and determine which one(s) have the highest weight for resubmission.
    failed = []
    for item in data:
        if item["group"].strip().lower() == "formative" and item["score"] < 50:
            failed.append(item)

    highest_weight = max((item["weight"] for item in failed), default=0)

    resubmit = []
    for item in failed:
        if item["weight"] == highest_weight:
            resubmit.append(item)

    # f) Print the final decision (PASSED / FAILED) and resubmission options
    print(f"\nFinal status: {status}")
    if len(resubmit) > 0:
        print("Eligible for resubmission (highest weight failed formative):")
        for item in resubmit:
            print(
                f"  - {item['assignment']} (score {item['score']:g}, weight {item['weight']:g})"
            )
    else:
        print("No resubmission needed.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
