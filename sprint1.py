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

def show_all_habits(data, guided_mode=True):
    if not data:
        print("No habits yet.")
        return
    if guided_mode:
        choice = input("Would you like to see your current habits? (y/n): ").strip().lower()
        if choice != 'y':
            return
    print("Current habits:")
    for habit in data:
        print(f"- {habit}")

def add_habit(data, guided_mode):
    if guided_mode:
        print("Step-by-step: To add a new habit, you'll be shown existing habits first. Then you can type the name of a new habit or cancel.")
        print("Tip: Type the habit name and press Enter. Or type 'cancel' to return without adding anything.")
    show_all_habits(data, guided_mode)
    while True:
        name = input("Enter new habit name (or type 'cancel' to return): ").strip()
        if name.lower() == 'cancel':
            if guided_mode:
                print("Action cancelled. No habit was added.")
            return
        if name in data:
            print("Habit already exists.")
        else:
            data[name] = {'dates': []}
            save_data(data)
            print(f"Added habit: {name}")
            return

def remove_habit(data, guided_mode):
    if guided_mode:
        print("Step-by-step: You'll see your habits. Then enter the name of the habit you want to delete.")
        print("Warning: Deleting a habit is permanent and cannot be undone.")
    show_all_habits(data, guided_mode)
    while True:
        name = input("Enter habit name to remove (or type 'cancel' to return): ").strip()
        if name.lower() == 'cancel':
            if guided_mode:
                print("Action cancelled. No habit was deleted.")
            return
        if name not in data:
            print("Habit not found.")
        else:
            confirm = input(f"Are you sure you want to delete '{name}'? This cannot be undone. (y/n): ").strip().lower()
            if confirm == 'y':
                del data[name]
                save_data(data)
                print(f"Removed habit: {name}")
            else:
                print("Cancelled. No changes were made.")
            return

def mark_done(data, guided_mode):
    if guided_mode:
        print("Step-by-step: You'll be shown your habits, then type the name of the habit you want to mark as done for today.")
    today = str(datetime.date.today())
    show_all_habits(data, guided_mode)
    while True:
        name = input("Enter habit name to mark as done (or type 'cancel' to return): ").strip()
        if name.lower() == 'cancel':
            if guided_mode:
                print("Action cancelled. No habit was marked.")
            return
        if name not in data:
            print("Habit not found.")
        else:
            if today in data[name]['dates']:
                print("Already marked as done today.")
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

def editing_mode(data, guided_mode):
    if guided_mode:
        print("Entering Editing Mode. You can choose to add, remove, or mark multiple habits.")
        print("Type 'done' at any point to return to the main menu.\n")
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
            if guided_mode:
                print("You chose to add multiple habits. You'll be shown current habits, then can add new ones. Type 'done' when finished.")
            show_all_habits(data, guided_mode)
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
            if guided_mode:
                print("You chose to remove multiple habits. Type 'done' when finished.")
            show_all_habits(data, guided_mode)
            while True:
                name = input("Remove habit (or 'done' to finish): ").strip()
                if name.lower() == 'done':
                    break
                if name in data:
                    confirm = input(f"Delete '{name}'? This cannot be undone. (y/n): ").strip().lower()
                    if confirm == 'y':
                        del data[name]
                        print(f"Removed: {name}")
                    else:
                        print("Cancelled.")
                else:
                    print("Habit not found.")
            save_data(data)
        elif choice == '3':
            today = str(datetime.date.today())
            if guided_mode:
                print("You chose to mark multiple habits as done. Type 'done' when finished.")
            show_all_habits(data, guided_mode)
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
    guided_mode = True

    def toggle_guided_mode():
        nonlocal guided_mode
        guided_mode = not guided_mode
        state = "ON" if guided_mode else "OFF"
        print(f"\nGuided Mode is now {state}.\n")

    actions = {
        '1': lambda: add_habit(data, guided_mode),
        '2': lambda: remove_habit(data, guided_mode),
        '3': lambda: mark_done(data, guided_mode),
        '4': lambda: list_habits(data),
        '5': lambda: editing_mode(data, guided_mode),
        '7': toggle_guided_mode
    }

    while True:
        print(f"""
=== Habit Tracker CLI ===
Build better habits, one day at a time!
Guided Mode: {'ON' if guided_mode else 'OFF'}

1. Add Habit
2. Remove Habit
3. Mark Habit as Done Today
4. List Habits
5. Editing Mode (Add/Remove/Mark Multiple)
6. Exit
7. Toggle Guided Mode (on/off)
""")
        choice = input("Choose an action: ").strip()
        if choice == '6':
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
