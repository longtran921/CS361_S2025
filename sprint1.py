import json
import datetime
import os

data_file = 'habits.json'

def load_data():
    if not os.path.exists(data_file):
        return {}
    with open(data_file, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

def show_all_habits(data):
    if not data:
        print("No habits yet.")
    else:
        print("Current habits:")
        for habit in data:
            print(f"- {habit}")

def add_habit(data):
    show_all_habits(data)
    while True:
        name = input("Enter new habit name (or type 'cancel' to return): ").strip()
        if name.lower() == 'cancel':
            print("Action cancelled.")
            return
        if name in data:
            print("Habit already exists.")
        else:
            data[name] = {'dates': []}
            save_data(data)
            print(f"Added habit: {name}")
            return

def remove_habit(data):
    show_all_habits(data)
    while True:
        name = input("Enter habit name to remove (or type 'cancel' to return): ").strip()
        if name.lower() == 'cancel':
            print("Action cancelled.")
            return
        if name not in data:
            print("Habit not found.")
        else:
            confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ")
            if confirm.lower() == 'y':
                del data[name]
                save_data(data)
                print(f"Removed habit: {name}")
            else:
                print("Cancelled.")
            return

def mark_done(data):
    show_all_habits(data)
    while True:
        name = input("Enter habit name to mark as done (or type 'cancel' to return): ").strip()
        if name.lower() == 'cancel':
            print("Action cancelled.")
            return
        today = str(datetime.date.today())
        if name not in data:
            print("Habit not found.")
        else:
            if today in data[name]['dates']:
                print("Already marked done today.")
            else:
                data[name]['dates'].append(today)
                save_data(data)
                print(f"Marked '{name}' as done for today.")
            return

def list_habits(data):
    if not data:
        print("No habits yet.")
        return
    today = str(datetime.date.today())
    for habit, info in data.items():
        done_today = today in info['dates']
        print(f"- {habit} ({'done' if done_today else 'not done'})")

def editing_mode(data):
    print("Entering Editing Mode. Type 'done' to finish.")
    while True:
        print("""
Editing Options:
1. Add multiple habits
2. Remove multiple habits
3. Mark multiple habits as done
4. Return to main menu
""")
        choice = input("Select an option: ").strip()
        if choice == '1':
            show_all_habits(data)
            while True:
                name = input("Add habit (or 'done' to finish): ").strip()
                if name.lower() == 'done':
                    break
                if name in data:
                    print("Habit already exists.")
                else:
                    data[name] = {'dates': []}
                    print(f"Added: {name}")
            save_data(data)
        elif choice == '2':
            show_all_habits(data)
            while True:
                name = input("Remove habit (or 'done' to finish): ").strip()
                if name.lower() == 'done':
                    break
                if name in data:
                    del data[name]
                    print(f"Removed: {name}")
                else:
                    print("Habit not found.")
            save_data(data)
        elif choice == '3':
            today = str(datetime.date.today())
            show_all_habits(data)
            while True:
                name = input("Mark habit as done (or 'done' to finish): ").strip()
                if name.lower() == 'done':
                    break
                if name in data:
                    if today not in data[name]['dates']:
                        data[name]['dates'].append(today)
                        print(f"Marked {name} as done.")
                    else:
                        print(f"{name} is already marked as done today.")
                else:
                    print("Habit not found.")
            save_data(data)
        elif choice == '4':
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    data = load_data()
    actions = {
        '1': add_habit,
        '2': remove_habit,
        '3': mark_done,
        '4': list_habits,
        '5': editing_mode
    }

    while True:
        print("""
=== Habit Tracker CLI ===
Build better habits, one day at a time!
1. Add Habit
2. Remove Habit
3. Mark Habit as Done Today
4. List Habits
5. Editing Mode (Add/Remove/Mark Multiple)
6. Exit
""")
        choice = input("Choose an action: ").strip()
        if choice == '6':
            break
        action = actions.get(choice)
        if action:
            action(data)
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
