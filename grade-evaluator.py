import csv
import os
import sys


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append(
                    {
                        "assignment": row["assignment"],
                        "group": row["group"],
                        "score": float(row["score"]),
                        "weight": float(row["weight"]),
                    }
                )
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    # a) Check if all scores are percentage based (0-100)
    for item in data:
        if item["score"] < 0 or item["score"] > 100:
            print(
                f"Error: invalid score {item['score']:g} for '{item['assignment']}'. Scores must be 0-100."
            )
            return
    print("Score check passed.")

    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    total_weight = 0
    formative_weight = 0
    summative_weight = 0
    for item in data:
        group = item["group"].strip().lower()
        total_weight += item["weight"]
        if group == "formative":
            formative_weight += item["weight"]
        elif group == "summative":
            summative_weight += item["weight"]
        else:
            print(f"Error: unknown group '{item['group']}' for '{item['assignment']}'.")
            return
    if total_weight != 100 or formative_weight != 60 or summative_weight != 40:
        print(
            f"Error: weights must be total 100, formative 60, summative 40 "
            f"(got {total_weight:g}, {formative_weight:g}, {summative_weight:g})."
        )
        return
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
    gpa = total_grade / 100 * 5.0
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

        highest_weight = 0
        for item in failed:
            if item["weight"] > highest_weight:
                highest_weight = item["weight"]

        resubmit = []
        for item in failed:
            if item["weight"] == highest_weight:
                resubmit.append(item)
    #          and determine which one(s) have the highest weight for resubmission.
    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
