from unittest.mock import patch

import dbbase as db
import habits as hb

# create a database object
db = db.Database(test=True)
db.init_db()

# create a habit object
hb = hb.Habit()


# test adding 6 predefined habits
def test_add_habit():
    hb.add_habit("Reducing Screen Time", 1, '2023-01-01 01:00:00', test=True)
    hb.add_habit("Workout", 1, '2023-01-05 01:00:00', test=True)
    hb.add_habit("Read a Book", 7, '2023-01-08 01:00:00', test=True)
    hb.add_habit("Learn a new Skill", 1, '2023-01-04 01:00:00', test=True)
    hb.add_habit("Eat Healthy", 30, '2023-01-02 01:00:00', test=True)
    assert db.get_habits() != [(1, "Reducing Screen Time", 1, '2023-01-01 01:00:00', None, 0),
                               (2, "Workout", 1, '2023-01-05 01:00:00', None, 0),
                               (3, "Read a Book", 7, '2023-01-08 01:00:00', None, 0),
                               (4, "Learn a new Skill", 1, '2023-01-04 01:00:00', None, 0),
                               (5, "Eat Healthy", 30, '2023-01-02 01:00:00', None, 0)]

# test deleting a habit
def test_delete_habit():
    hb.delete_habit(1, test=True)
    assert db.get_habit(1) is None

# test marking a daily habit as complete for 2 consecutive days
def test_mark_daily_as_complete_two_consecutive_days():
    hb.mark_habit_as_complete(1, '2023-01-02 01:00:00', test=True)
    hb.mark_habit_as_complete(1, '2023-01-03 01:00:00', test=True)
    assert db.get_habit_completions(1) == ['2023-01-02 01:00:00', '2023-01-03 01:00:00']


def test_mark_daily_as_complete_five_consecutive_days():
    hb.mark_habit_as_complete(2, '2023-02-02 01:00:00', test=True)
    hb.mark_habit_as_complete(2, '2023-02-03 01:00:00', test=True)
    hb.mark_habit_as_complete(2, '2023-02-04 01:00:00', test=True)
    hb.mark_habit_as_complete(2, '2023-02-05 01:00:00', test=True)
    hb.mark_habit_as_complete(2, '2023-02-06 01:00:00', test=True)
    assert db.get_habit_completions(2) == [('2023-02-02 01:00:00',), ('2023-02-03 01:00:00',), ('2023-02-04 01:00:00',),
                                           ('2023-02-05 01:00:00',), ('2023-02-06 01:00:00',)]


def test_mark_weekly_habit_as_complete():
    # Set up test data
    habit_id = 3
    completion_dates = ['2023-01-15 01:00:00', '2023-01-18 01:00:00', '2023-01-29 01:00:00', '2023-02-02 01:00:00',
                        '2023-02-08 01:00:00']

    # Use mock to simulate user input
    with patch('builtins.input', return_value='y'):
        # Mark habit as complete for each date
        for date in completion_dates:
            hb.mark_habit_as_complete(habit_id, date, test=True)

    assert db.get_habit_completions(habit_id) == [('2023-01-15 01:00:00',), ('2023-01-18 01:00:00',),
                                                  ('2023-01-29 01:00:00',), ('2023-02-02 01:00:00',),
                                                  ('2023-02-08 01:00:00',)]
    assert db.get_habit(3) == (3, "Swim", 7, '2023-01-08 01:00:00', '2023-02-08 01:00:00', 5)
    assert db.get_habit_periodicity(3) == 7
    assert db.get_last_completion_date(3) == '2023-02-08 01:00:00'
    assert db.get_streaks_for_habit(3) == (3, 3, 3, 3)
    db.reset_streak(3)
    assert db.get_streaks_for_habit(3) == (3, 3, 0, 3)


# test marking a daily habit as complete for 6 times which has current streak of 0 and longest streak of 4
def test_mark_habit_as_complete():
    hb.mark_habit_as_complete(4, "2023-01-08 01:00:00", test=True)
    hb.mark_habit_as_complete(4, "2023-01-09 02:00:00", test=True)
    hb.mark_habit_as_complete(4, "2023-01-10 03:00:00", test=True)
    hb.mark_habit_as_complete(4, "2023-01-11 04:00:00", test=True)
    hb.mark_habit_as_complete(4, "2023-01-13 05:00:00", test=True)
    hb.mark_habit_as_complete(4, "2023-01-14 06:00:00", test=True)
    assert db.get_updated_streaks(4) == (4, 4, 0, 4)


# test marking a monthly habit as complete for 2 times which has current streak of 0 and longest streak of 2
def test_mark_monthly_habit_as_complete():
    hb.mark_habit_as_complete(5, "2023-01-05 01:00:00", test=True)
    # Use mock to simulate user input
    with patch('builtins.input', return_value='y'):
        hb.mark_habit_as_complete(5, "2023-02-01 01:00:00", test=True)
    assert db.get_updated_streaks(5) != (5, 5, 0, 2)



