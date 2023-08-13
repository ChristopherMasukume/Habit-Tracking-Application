import termcolor
from datetime import datetime
import dbbase

def get_db(test):
    """
    This function returns a database object.
    :param test: Whether the database is a test database.
    :return: A database object.
    """
    return dbbase.Database(test=test)


class Habit:
    """
    This class represents a habit. It contains methods to add a habit to the database, mark a habit as complete, and
    delete a habit from the database.
    """
    def __init__(self, habit_id=None, name=None, periodicity=None, creation_date=None, completion_date=None):
        """
        This method initializes the habit object.
        :param habit_id: The ID of the habit.
        :param name: The name of the habit.
        :param periodicity: The periodicity of the habit.
        :param creation_date: The date and time the habit was created.
        :param completion_date: The date and time the habit was completed.
        """
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completion_date = completion_date

    def add_habit(self, name, periodicity, creation_date, test=False):
        """
        The function adds habits to the database and if the habit exists a notification will be displayed, but if it
        does not exist it will then be added to the database. A notification will be displayed if successful.
        the following parameters are explained;
        name: The name of the habit.
        periodicity: The periodicity of the habit.
        creation_date: The date and time the habit was created.
        test: Whether the database is a test database.
        return: None
        """
        if test:
            db = get_db(test=True)
        else:
            db = get_db(test=False)
        # Check if habit already exists
        db.cur.execute("SELECT * FROM habits WHERE habit_name=?", (name,))
        row = db.cur.fetchone()
        if row:
            print(termcolor.colored("Habit already exists!", "red"))
            return
        # Add habit to database
        db.cur.execute("INSERT INTO habits (habit_name, periodicity, creation_date) VALUES (?, ?, ?)",
                       (name, periodicity, creation_date))
        self.habit_id = db.cur.lastrowid
        # Add habit to streaks table
        db.cur.execute("INSERT INTO streaks (habit_id, current_streak, longest_streak) VALUES (?, ?, ?)",
                       (self.habit_id, 0, 0))
        db.commit()
        db.close()
        print(termcolor.colored("Habit added successfully!", "green"))

    def mark_habit_as_complete(self, habit_id, completion_date, test=False):
        """
        this method marks a habit as complete it the user have completed it. The user will be asked to to mark the
        habit as complete. If the habit is completed within a period then a streak will be reset and the last
        completion date and the number of completion will be updated.
        The following parameters are explained;
        habit_id: The ID of the habit.
        completion_date: The date and time the habit was completed.
        test: Whether the database is a test database.
        return: None
        """
        if test:
            db = get_db(test=True)
        else:
            db = get_db(test=False)
        self.habit_id = habit_id
        self.completion_date = datetime.strptime(completion_date, '%Y-%m-%d %H:%M:%S')
        last_completion_date = db.get_last_completion_date(self.habit_id)
        periodicity = db.get_habit_periodicity(self.habit_id)
        # Check if habit has been completed within the period and ask user if they want to mark it as complete anyway
        if last_completion_date:
            last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d %H:%M:%S')
            if (self.completion_date - last_completion_date).days < periodicity:
                print(termcolor.colored("Habit has already been completed within the period. Mark it as complete "
                                        "anyway?",
                                        "red"))
                answer = input("y/n: ")
                if answer.lower() != "y":
                    return

        # Add completion to database
        db.cur.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
                       (self.habit_id, self.completion_date))
        # Update habit's last completion date and number of completions
        db.cur.execute(
            "UPDATE habits SET last_completion_date=?, number_of_completions=number_of_completions+1 WHERE id=?",
            (self.completion_date, self.habit_id))
        db.commit()

        # Check if habit has previous completions
        db.cur.execute("SELECT last_completion_date FROM habits WHERE id=?", (self.habit_id,))
        row = db.cur.fetchone()
        if not row[0]:
            return

        # Calculate current streak and longest streak
        db.cur.execute("SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date DESC LIMIT 2",
                       (self.habit_id,))
        rows = db.cur.fetchall()
        completion_list = []
        # Convert completion dates to datetime objects
        for row in rows:
            completion_list.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').date())
        current_streak = db.get_streaks_for_habit(self.habit_id)[2]
        longest_streak = db.get_streaks_for_habit(self.habit_id)[3]
        # Check if habit has been completed for the first time
        if len(completion_list) == 1:
            current_streak = 1
            longest_streak = 1
        # Check if habit has been completed more than once
        else:
            prev_date = completion_list[1]
            current_date = completion_list[0]
            # Check if habit has been completed within the period
            if (current_date - prev_date).days <= periodicity:
                current_streak += 1
                # Check if current streak is the longest streak
                if current_streak > longest_streak:
                    longest_streak = current_streak
            # Habit has not been completed within the period
            else:
                current_streak = 1

        # Update streaks table
        db.cur.execute("UPDATE streaks SET current_streak=?, longest_streak=? WHERE habit_id=?",
                       (current_streak, longest_streak, self.habit_id))
        db.commit()
        db.close()
        print(termcolor.colored("Habit has been marked as complete!", "green"))

    def delete_habit(self, habit_id, test=False):
        """
        This method deletes a habit from the database. The streaks and completion date will also be deleted.
        the parameters are explained;
        """
        if test:
            db = get_db(test=True)
        else:
            db = get_db(test=False)
        self.habit_id = habit_id

        # Delete habit from habits table
        db.cur.execute("""DELETE FROM habits WHERE id = ?""", (self.habit_id,))
        # Delete habit from streaks table
        db.cur.execute("""DELETE FROM streaks WHERE habit_id = ?""", (self.habit_id,))
        # Delete habit from completions table
        db.cur.execute("""DELETE FROM completions WHERE habit_id = ?""", (self.habit_id,))
        db.commit()
        db.close()
        print(termcolor.colored("Habit deleted!", "red"))