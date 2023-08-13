import sys
from datetime import datetime

import questionary
import termcolor

import analyze
import dbbase as db
import habits as hb

print(termcolor.colored("\n_________________________________", "cyan"))
print(termcolor.colored("Your Habit Tracker", "white"))
print(termcolor.colored("Main Menu.", "yellow"))


hb = hb.Habit()
db = db.Database(test=False)
db.init_db()


def main():
    """
    This function is to open the main menu for the  application.
    It has all the functionalities for the application.
    It displays the data from the database.
    After the user is done with the application it gives an option to continue or quit.
    """
    action = questionary.select("\nWhat would you like to do?", choices=[
        {"name": "Add habit", "value": "add"},
        {"name": "Mark habit as complete", "value": "complete"},
        {"name": "Delete habit", "value": "delete"},
        {"name": "Current habits", "value": "todo"},
        {"name": "Analyze habits", "value": "analyze"},
        {"name": "Insert predefined habits", "value": "predefined"},
        {"name": "Quit", "value": "quit"}
    ]).ask()

    if action == 'add':
        name = questionary.text("What is your habit name?").ask()
        periodicity = questionary.select("What is the habit periodicity?", choices=[
            {"name": "Daily", "value": 1},
            {"name": "Weekly", "value": 7},
            {"name": "Monthly", "value": 30}
        ]).ask()
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hb.add_habit(name, periodicity, creation_date)
        ask_to_continue()

    elif action == 'complete':
        habits = db.get_habits()
        habit_list = []
        if len(habits) == 0:
            print(termcolor.colored("There are no habits to mark as complete!", "red"))
            ask_to_continue()
        for habit in habits:
            habit_list.append(f"{habit[0]}: {habit[1]}")
        habit_to_mark = questionary.select("Which habit would you like to mark?", choices=habit_list).ask()
        habit_id = habit_to_mark.split(":")[0].strip()
        completion_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hb.mark_habit_as_complete(habit_id, completion_date)
        ask_to_continue()

    elif action == 'delete':
        habits = db.get_habits()
        habit_list = []
        if len(habits) == 0:
            print(termcolor.colored("There are no habits to delete!", "red"))
            ask_to_continue()
        for habit in habits:
            habit_list.append(f"{habit[0]}: {habit[1]}")
        habit_list.append({"name": "Go back to main menu", "value": "back"})
        habit_to_delete = questionary.select("Which habit would you like to delete?", choices=habit_list).ask()
        if habit_to_delete == "back":
            return
        habit_id = habit_to_delete.split(":")[0].strip()
        hb.delete_habit(habit_id)
        ask_to_continue()

    elif action == 'todo':
        analyze.habits_todo()
        ask_to_continue()

    elif action == 'analyze':
        choices = [
            {"name": "Habits overview", "value": "overview"},
            {"name": "Single habit status", "value": "status"},
            {"name": "Streaks analysis", "value": "streak"},
            {"name": "All completions of a habit", "value": "all"},
            {"name": "Go back to main menu", "value": "back"}]

        action = questionary.select("\nWhat would you like to do?", choices=choices).ask()
        if action == 'overview':
            analyze.habits_overview()
            ask_to_continue()

        elif action == 'status':
            analyze.habit_status()
            ask_to_continue()

        elif action == 'streak':
            analyze.show_habit_streaks()
            ask_to_continue()

        elif action == 'all':
            habits = db.get_habits()
            habit_list = []
            if len(habits) == 0:
                print(termcolor.colored("There are no habits to show!", "red"))
                return
            for habit in habits:
                habit_list.append(f"{habit[0]}: {habit[1]}")
            habit_list.append({"name": "Go back to main menu", "value": "back"})
            selected_habit = questionary.select("Which habit would you like to select?", choices=habit_list).ask()
            if selected_habit == "back":
                return
            habit_id = selected_habit.split(":")[0].strip()
            analyze.show_habit_completions(habit_id)
            ask_to_continue()

        elif action == 'back':
            main()

    elif action == 'predefined':
        ask = questionary.confirm("Do you want to insert predefined habits into database?").ask()
        if ask is True:
            db.clear_database()
            db.insert_test_data()
            print(termcolor.colored("Predefined habits inserted successfully!", "green"))
            ask_to_continue()
        else:
            return main()

    elif action == 'quit':
        print(termcolor.colored("See you soon!!!\n\n", "blue"))
        sys.exit(0)

    else:
        print(termcolor.colored("Invalid option. Please try again!", "red"))


def ask_to_continue():
    """
    This function enables the user to continue with the application, if the user chooses to continue
    the application calls the main menu again, if the user chooses to quit the application will close.
    """
    continue_ = questionary.confirm("Would you like to continue?").ask()
    if continue_:
        main()
    else:
        print(termcolor.colored("See you soon!!!\n\n", "blue"))
        sys.exit(0)


if __name__ == "__main__":
    main()