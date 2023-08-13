Habit Tracking App - README
====================================================================================    
**Through the Object-Oriented and Functional Programming module, a backend for a Habit Tracking Application has been 
created using Python Programming language through PyCharm.**

## Installation
**To be able to run this code please install Python 3.7**

*For the installation of Python follow this [link](https://www.python.org/downloads/) and follow the instructions.*


### Install Habit Tracking Application

- Download the latest version of IU habit tracker from
[here][(https://github.com/ChristopherMasukume/Habit-Tracking-Application/archive/refs/heads/main.zip)]
- unzip the file and go to the "IU-habit-tracker-master" directory
- Create a python virtual environment

``` sh
python -m venv HTenv
```

- Activate your environment

``` sh
.\HTenv\Scripts\activate
```

- Install the requirements

``` sh
pip install -r requirements.txt
```

## Testing

- On the parent directory of project, Run pytest

``` sh
pytest -v
```

You should see something like this if all the tests are successful:


---
## Usage

### Run habit tracker

- On the parent folder "Habit Tracking Application", Run main.py

``` sh
python main.py
```

- You should see the main menu like picture below, and you can navigate through the options using the arrow keys and press enter to select an option.



 
### Add habit
- Enter a habit name and the habit period.


### Mark habit as complete
- Select the habit name to be able to mark it as complete.


### Delete habits
- Select the habit name to be able to delete it from the habit list.


### Insert predefined data
- You can insert predefined data by selecting this option from the main menu.
- It will insert 5 predefined habits with different periods.


### Habits to do
- This displays the habits that have to be done.


### Analytics
- This option uses analyze module to show users the details of their habits.
- "Habits overview" option will show an overview of the habits that user has entered based on their period.
- "Single habit status" will show you the list of all habits, and you can select one of them to see the details of that habit.
- "Streaks analysis" will show you a table of all habits and their current and longest streaks.
- "All completions of a habit" will show you a list of all habits, and you can select one of them to see all the dates that you have marked that habit as done.

---

## Author

👤 **Christopher Masukume**

* Github: [@ChristopherMasukume](https://github.com/ChristopherMasukume)
* email: christopher.masukume@iu-study.org 

---
## Contribution
This project is for educational purposes only.
