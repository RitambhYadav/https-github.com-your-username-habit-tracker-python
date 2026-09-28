import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("habits.json")


def load_habits():
    """Load saved habits, or start with an empty list."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read habits.json. Starting with an empty habit list.")
        return []


def save_habits(habits):
    """Save habits to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(habits, file, indent=4)


def add_habit(habits):
    name = input("Enter the habit you want to track: ").strip()

    if not name:
        print("Habit name cannot be empty.")
        return

    if any(habit["name"].lower() == name.lower() for habit in habits):
        print("That habit is already in your tracker.")
        return

    habits.append({"name": name, "completed_dates": []})
    save_habits(habits)
    print(f"Added habit: {name}")


def show_habits(habits):
    if not habits:
        print("You have not added any habits yet.")
        return

    today = date.today().isoformat()
    print("\nYour habits:")
    for number, habit in enumerate(habits, start=1):
        status = "Done today" if today in habit["completed_dates"] else "Not done today"
        print(f"{number}. {habit['name']} — {status}")


def complete_habit(habits):
    if not habits:
        print("Add a habit before marking one complete.")
        return

    show_habits(habits)

    try:
        choice = int(input("Enter the number of the habit you completed: "))
        if choice < 1 or choice > len(habits):
            print("Please enter a number from the list.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    habit = habits[choice - 1]
    today = date.today().isoformat()

    if today in habit["completed_dates"]:
        print(f"You already marked '{habit['name']}' complete today.")
    else:
        habit["completed_dates"].append(today)
        save_habits(habits)
        print(f"Great job! '{habit['name']}' is complete for today.")


def show_history(habits):
    if not habits:
        print("You have not added any habits yet.")
        return

    print("\nHabit history:")
    for habit in habits:
        dates = habit["completed_dates"]
        print(f"\n{habit['name']}: {len(dates)} completed day(s)")
        if dates:
            for completed_date in dates:
                print(f"  - {completed_date}")
        else:
            print("  No completions recorded yet.")


def main():
    habits = load_habits()

    while True:
        print("\n=== Habit Tracker ===")
        print("1. Add a habit")
        print("2. View habits")
        print("3. Mark a habit complete")
        print("4. View completion history")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_habit(habits)
        elif choice == "2":
            show_habits(habits)
        elif choice == "3":
            complete_habit(habits)
        elif choice == "4":
            show_history(habits)
        elif choice == "5":
            print("Goodbye! Keep building good habits.")
            break
        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()