from datetime import date, datetime
import questionary
import tabulate as tb
import termcolor
import dbbase as db, habits as hb


db = db.Database(test=False)
hb = hb.Habit()


def habits_todo():
    """
    This method prints the habits that need to be completed today.
    """
    habits = db.get_habits()
    headers = ["ID", "Habit Name", "Periodicity", "Last Completion"]
    habit_list = []
    today = date.today()
    for habit in habits:
        habit_id = habit[0]
        habit_name = habit[1]
        periodicity = habit[2]
        last_completion_date = habit[4]
        # If the habit has never been completed, add it to the list
        if last_completion_date is None:
            habit_list.append([habit_id, habit_name, periodicity, "Never"])
            continue
        last_completion_date_str = last_completion_date.split(" ")[0]
        last_completion_date = datetime.strptime(last_completion_date_str, '%Y-%m-%d').date()
        # If the habit has been completed today, skip it
        if (today - last_completion_date).days >= periodicity:
            habit_list.append([habit_id, habit_name, periodicity, last_completion_date])
    # If there are no habits to do today, print a message and return
    if not habit_list:
        print(termcolor.colored("You don't have any habits to do today!", "red"))
        return
    print(tb.tabulate(habit_list, headers, tablefmt="fancy_grid"))


def habits_overview():
    """
    This method prints the habits overview of all habits based on their periodicity.
    """
    choice = questionary.select("What would you like to see?", choices=[
        {"name": "All habits", "value": "all"},
        {"name": "Daily habits", "value": "daily"},
        {"name": "Weekly habits", "value": "weekly"},
        {"name": "Monthly habits", "value": "monthly"}
    ]).ask()
    if choice == "all":
        habits = db.get_habits()
        headers = ["ID", "Habit Name", "Periodicity", "Creation Date", "Last Completion Date", "Number of Completions"]
        print(tb.tabulate(habits, headers, tablefmt="fancy_grid"))
    elif choice == "daily":
        habits = db.get_habits()
        headers = ["ID", "Habit Name", "Periodicity", "Creation Date", "Last Completion Date", "Number of Completions"]
        habit_list = []
        for habit in habits:
            if habit[2] == 1:
                habit_list.append(habit)
        print(tb.tabulate(habit_list, headers, tablefmt="fancy_grid"))
    elif choice == "weekly":
        habits = db.get_habits()
        headers = ["ID", "Habit Name", "Periodicity", "Creation Date", "Last Completion Date", "Number of Completions"]
        habit_list = []
        for habit in habits:
            if habit[2] == 7:
                habit_list.append(habit)
        print(tb.tabulate(habit_list, headers, tablefmt="fancy_grid"))
    elif choice == "monthly":
        habits = db.get_habits()
        headers = ["ID", "Habit Name", "Periodicity", "Creation Date", "Last Completion Date", "Number of Completions"]
        habit_list = []
        for habit in habits:
            if habit[2] == 30:
                habit_list.append(habit)
        print(tb.tabulate(habit_list, headers, tablefmt="fancy_grid"))


def habit_status():
    """
    This function prints the habit status.
    """
    habits = db.get_habits()
    habit_list = []

    # If there are no habits, print a message and return
    if len(habits) == 0:
        print(termcolor.colored("You don't have any habits yet!", "red"))
        return

    # If there are habits, add them to the habit list
    for habit in habits:
        habit_list.append(f"{habit[0]}: {habit[1]}")
    habit_to_mark = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
    habit_id = habit_to_mark.split(":")[0].strip()

    # Get the habit from the database
    habit = db.get_habit(habit_id)
    habit_name = habit[1]
    period = habit[2]
    last_completion_date = habit[4]
    number_of_completions = habit[5]
    streaks = db.get_updated_streaks(habit_id)
    current_streak = streaks[2]
    max_streak = streaks[3]

    # Check if the habit has been completed within the period
    days_since_last_completion = 0
    if last_completion_date is not None:
        last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d %H:%M:%S')
        days_since_last_completion = (datetime.now() - last_completion_date).days

        # If the habit has been completed within the period, print a message and return
        if period == 1 and days_since_last_completion > 0:
            print(termcolor.colored("\nYou have broken the habit '{}' since it has been {} days since the last "
                                    "completion.".format(habit_name, days_since_last_completion), "red"))
            pass
        elif period == 7 and days_since_last_completion > 7:
            print(termcolor.colored("\nYou have broken the habit '{}' since it has been {} days since the last "
                                    "completion.".format(habit_name, days_since_last_completion), "red"))
            pass
        elif period == 30 and days_since_last_completion > 30:
            print(termcolor.colored("\nYou have broken the habit '{}' since it has been {} days since the last "
                                    "completion.".format(habit_name, days_since_last_completion), "red"))
            pass
        else:
            print(termcolor.colored("\nYou have completed your habit within it's period. It's great, keep going!",
                  "green"))

    # If the habit has not been completed yet, print a message
    else:
        print(termcolor.colored(f"\nHabit *{habit_name}* has not been completed yet.", "red"))

    # Convert the periodicity to a string
    periodicity = ""
    if period == 1:
        period = "Day"
        periodicity = "daily"
    elif period == 7:
        period = "Week"
        periodicity = "weekly"
    elif period == 30:
        period = "Month"
        periodicity = "monthly"

    # Convert the last completion date to a string if it is None
    if last_completion_date is None:
        last_completion_date = "Not completed yet"

    current_streak = f"{current_streak} {period.lower()}(s) of streaks"
    max_streak = f"{max_streak} {period.lower()}(s) in a row"

    # print habit data in tabulate format
    headers = ["Habit Name", "Periodicity", "Last completion", "Number of Completions", ]
    data = [habit_name, periodicity, last_completion_date, f"{number_of_completions} time(s)"]
    print(tb.tabulate([data], headers=headers, tablefmt="fancy_grid"))

    # print habit data in tabulate format
    headers = ["Days Since Last Completion", "Current Streak", "Max Streak"]
    data = [f"{days_since_last_completion} day(s)", current_streak, max_streak]
    print(tb.tabulate([data], headers=headers, tablefmt="fancy_grid"))


def show_habit_streaks():
    """
    This function prints the habits streaks.
    """
    habits = db.get_habits()
    streaks = db.get_streaks()
    for streak in streaks:
        habit_id = streak[1]
        db.update_streak(habit_id)
    streaks = db.get_streaks()
    headers = ["Habit ID", "Habit Name", "Periodicity", "Current Streak", "Max Streak"]
    show_list = []
    streak_list = []

    for streak in streaks:
        habit_id = streak[1]
        current_streak = streak[2]
        max_streak = streak[3]
        streak_list.append([habit_id, current_streak, max_streak])

    for habit in habits:
        habit_id = habit[0]
        habit_name = habit[1]

        # Convert the periodicity to a string
        periodicity = habit[2]
        if periodicity == 1:
            periodicity = "daily"
        elif periodicity == 7:
            periodicity = "weekly"
        elif periodicity == 30:
            periodicity = "monthly"

        for streak in streak_list:
            if streak[0] == habit_id:
                show_list.append([habit_id, habit_name, periodicity, streak[1], streak[2]])
                break

    print(tb.tabulate(show_list, headers, tablefmt="fancy_grid"))

    # get the name of habit with the longest streak
    max_habit = ""
    max_streak = 0
    for habit in show_list:
        if habit[4] > max_streak:
            max_habit = habit[1]
            max_streak = habit[4]

    print(termcolor.colored(f"your longest habit streaks is: {max_habit}\n", "green"))


def show_habit_completions(habit_id):
    """
    This function prints the completions of a habit.
    The following parameters explained;
    habit_id: The ID of the habit.
    return: None
    """
    # get the habit completions from the database
    completions = db.get_habit_completions(habit_id)
    habit = db.get_habit(habit_id)
    habit_completions = []
    habit_name = habit[1]
    print(termcolor.colored(f"\nAll Completions of habit *{habit_name}*", "green"))

    # print the habit completions in last month in a table format using tabulate library
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S')
        habit_completions.append([completion_date])
    headers = ["date and time of habit completion(s)"]
    print(tb.tabulate(habit_completions, headers, tablefmt="fancy_grid"))

    # calculate the number of completions in the last 7 days
    completions_in_last_7_days = 0
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - completion_date).days <= 7:
            completions_in_last_7_days += 1
    print(termcolor.colored(f"Number of completions in the last 7 days: {completions_in_last_7_days}", "blue"))

    # calculate the number of completions in the last 30 days
    completions_in_last_30_days = 0
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - completion_date).days <= 30:
            completions_in_last_30_days += 1
    print(termcolor.colored(f"Number of completions in the last 30 days: {completions_in_last_30_days}\n", "blue"))